from PIL import Image
import pytesseract

def extract_text_from_tiff(file_path):
    """
    Given a multipage .tif file path, open each page,
    run OCR on it, and return the concatenated text.
    """