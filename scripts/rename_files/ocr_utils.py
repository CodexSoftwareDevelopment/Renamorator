from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
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
    def ocr_page(page_num):
        with Image.open(file_path) as page_img:
            page_img.seek(page_num)
            return pytesseract.image_to_string(page_img)
        
    # 3) Spin up one thread per CPU core (or fallback to 2)
    workers = os.cpu_count() or 2
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(ocr_page, i) for i in range(n_pages)]
        pages_text = []
        for fut in tqdm(as_completed(futures),
                        total=n_pages,
                        desc=f"OCR {os.path.basename(file_path)}"):
            pages_text.append(fut.result())


    # 4) Join all the page‑texts into one big string
    return "\n".join(pages_text)