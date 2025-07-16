from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DeidreClay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_tiff(file_path):
    """
    Given a multipage .tif file path, open each page,
    run OCR on it, and return the concatenated text.
    """

     # Open the TIFF as a PIL Image object
    img = Image.open(file_path)
    n_pages = getattr(img, "n_frames", 1)

    # Prepare a list to collect text from each page
    pages_text = []

    # Iterate over each frame (page) in the TIFF
    for i in range(n_pages):
        print(f"  ↳ OCR page {i+1}/{n_pages} of {os.path.basename(file_path)}")
        img.seek(i)
        pages_text.append(pytesseract.image_to_string(img))

    # Join all pages into one big string and return
    return "\n".join(pages_text)