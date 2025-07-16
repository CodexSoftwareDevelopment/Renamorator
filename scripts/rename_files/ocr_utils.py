from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DeidreClay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_tiff(file_path):
    """
    Parallel OCR: splits a multipage TIFF into pages,
    then runs OCR on each page concurrently.
    """

     # 1) Figure out how many pages are in this TIFF
    with Image.open(file_path) as img:
       n_pages = getattr(img, "n_frames", 1)

    # 2) Define a mini‐task that OCRs a single page
    def ocr_page(page_num, total=n_pages, fname=os.path.basename(file_path)):
        print(f"  ↳ OCR page {page_num+1}/{total} of {fname}")
        with Image.open(file_path) as page_img:
            page_img.seek(page_num)
            return pytesseract.image_to_string(page_img)
        
    # 3) Spin up one thread per CPU core (or fallback to 2)
    workers = os.cpu_count() or 2
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pages_text = list(pool.map(ocr_page, range(n_pages)))

    # 4) Join all the page‑texts into one big string
    return "\n".join(pages_text)