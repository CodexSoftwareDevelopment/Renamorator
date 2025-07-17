import re
from .doc_number_extractor import extract_document_numbers

def parse_new_filename(ocr_text: str) -> str:
    # Grab every unique VP-code
    doc_nums = extract_document_numbers(ocr_text)

    # Join them with spaces (or fallback to "UNKNOWN" if none found)
    doc_part = " ".join(doc_nums) if doc_nums else "UNKNOWN"

    # (…then you’d tack on your blend, volume, equipment parts…)
    return f"{doc_part}.tif"