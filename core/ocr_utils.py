from PIL import Image
import pytesseract
import cv2
import numpy as np
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from header_processor import preprocess_header

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DeidreClay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_tiff(
    file_path: str,
    page_callback: Callable[[int, int], None] = None
) -> str:
    """
    OCR a multi-page TIFF in parallel across pages.
    Calls page_callback(completed_page_index, total_pages) after each page.
    """

    # 1) Count pages
    with Image.open(file_path) as img:
        try:
            n_pages = img.n_frames
        except AttributeError:
            n_pages = 0
            while True:
                try:
                    img.seek(n_pages)
                    n_pages += 1
                except EOFError:
                    break

    # 2) Define per-page OCR
    def ocr_page(page_index: int) -> tuple[int,str]:
        with Image.open(file_path) as img:
            img.seek(page_index)
            rgb = img.convert('RGB')
        full_text = pytesseract.image_to_string(rgb)
        bgr = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)
        hdr_img = preprocess_header(bgr)
        hdr_cfg = (
            "--oem 1 --psm 6 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ#.0123456789"
        )
        header_text = pytesseract.image_to_string(hdr_img, config=hdr_cfg)
        return page_index, header_text + "\n" + full_text

    # 3) Run pages in parallel
    pages = ["" for _ in range(n_pages)]
    workers = os.cpu_count() or 2
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(ocr_page, i): i for i in range(n_pages)}
        for fut in as_completed(futures):
            idx, text = fut.result()
            pages[idx] = text
            if page_callback:
                # report 1-based page count to the UI
                page_callback(idx + 1, n_pages)

    return "\n".join(pages)
