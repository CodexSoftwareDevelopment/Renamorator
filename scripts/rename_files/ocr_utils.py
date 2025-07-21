from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pytesseract
import os
import cv2
import numpy as np

# Point pytesseract at your local tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DeidreClay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def preprocess_header(img: np.ndarray) -> np.ndarray:
    """
    Crop out the top portion of the page (where your header lives),
    convert to grayscale, threshold, denoise, and deskew.
    Returns a clean B&W image ready for Tesseract.
    """
    # 1) Crop to top 25%
    h, w = img.shape[:2]
    header = img[0:int(h * 0.25), :]

    # 2) Grayscale -> blur -> adaptive threshold (invert for white text on black)
    gray = cv2.cvtColor(header, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    th = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # 3) Morphological opening to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

    # 4) Deskew based on minAreaRect of white pixels
    coords = np.column_stack(np.where(opening > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    M = cv2.getRotationMatrix2D((w / 2, h * 0.125), angle, 1.0)
    deskewed = cv2.warpAffine(
        opening, M, (w, int(h * 0.25)),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    # 5) Invert back to black-on-white
    return cv2.bitwise_not(deskewed)


def extract_text_from_tiff(file_path: str) -> str:
    """
    Parallel OCR of a multi-page TIFF, with a special header pass for cleaner Document# detection.
    Returns combined text (header_text + full_text) for each page.
    """
    # 1) Load image and count pages
    with Image.open(file_path) as img:
        try:
            n_pages = img.n_frames
        except AttributeError:
            # fallback if PIL version doesn't support n_frames
            n_pages = 0
            while True:
                try:
                    img.seek(n_pages)
                    n_pages += 1
                except EOFError:
                    break

    def ocr_page(page_index: int) -> str:
        # Load and convert to RGB
        with Image.open(file_path) as img:
            img.seek(page_index)
            page_rgb = img.convert('RGB')

        # Full-page OCR (looser config)
        full_text = pytesseract.image_to_string(page_rgb)

        # Header-only OCR (preprocessed + whitelist)
        bgr = cv2.cvtColor(np.array(page_rgb), cv2.COLOR_RGB2BGR)
        hdr_img = preprocess_header(bgr)
        hdr_cfg = (
            "--oem 1 --psm 6 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ#.0123456789"
        )
        header_text = pytesseract.image_to_string(hdr_img, config=hdr_cfg)

        # Combine header first to ensure parser sees it
        return header_text + "\n" + full_text

    # 2) Run pages in parallel
    workers = os.cpu_count() or 2
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(ocr_page, i) for i in range(n_pages)]
        pages = []
        for fut in tqdm(as_completed(futures), total=n_pages, desc=f"OCR {os.path.basename(file_path)}"):
            pages.append(fut.result())

    # 3) Return text of all pages
    return "\n".join(pages)
