import cv2
import pytesseract
import os
import numpy as np
from typing import Callable, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageSequence

# Configure Tesseract executable (adjust path if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DeidreClay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Preprocess image: ensure grayscale, resize if large, threshold for binary
def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    # If already single-channel, skip conversion
    if img.ndim == 2:
        gray = img
    elif img.ndim == 3 and img.shape[2] == 1:
        gray = img[:, :, 0]
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize large images
    h, w = gray.shape
    max_dim = 2000
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# OCR a single page, return (index, text)
def ocr_page_from_array(page_index: int, img_array: np.ndarray) -> Tuple[int, str]:
    processed = preprocess_for_ocr(img_array)
    text = pytesseract.image_to_string(processed, config="-l eng --oem 1 --psm 3")
    return page_index, text.strip()

# Extract text from a multi-page TIFF
def extract_text_from_tiff(
    file_path: str,
    page_callback: Callable[[int, int], None] = None
) -> str:
    """
    Reads every page of a (possibly multipage) TIFF and runs OCR on each.
    """
    # Use PIL to read every frame
    try:
        pil = Image.open(file_path)
        pages = [np.array(frame.convert('RGB')) for frame in ImageSequence.Iterator(pil)]
    except Exception as e:
        # Fallback to OpenCV for single‐page or non‐PIL‐readable files
        pil_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if pil_img is None:
            raise RuntimeError(f"Could not open image for OCR: {file_path}") from e
        pages = [pil_img]

    n_pages = len(pages)
    results = [None] * n_pages

    # Parallel OCR across CPU cores
    workers = max(1, (os.cpu_count() or 2) - 1)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(ocr_page_from_array, idx, pages[idx]): idx
            for idx in range(n_pages)
        }
        for fut in as_completed(futures):
            idx, page_text = fut.result()
            results[idx] = page_text
            if page_callback:
                page_callback(idx + 1, n_pages)

    return "\n".join(results) or ""