import os

from rename_files.ocr_utils import extract_text_from_tiff
from rename_files.file_collector import collect_tif_files
from rename_files.doc_number_extractor import extract_document_numbers
from rename_files.text_parser import parse_new_filename

def main():
    """
    Test script to:
      1) Collect TIFF files
      2) Run OCR on each
      3) Extract VP/CVP document numbers
      4) Show full parsed filename stub
    """
    # 1) Gather all TIFF files
    tif_paths = collect_tif_files('assets/test_files')
    print(f"🔍 Found {len(tif_paths)} TIFF files. Running OCR + extraction...\n")

    # 2) Loop and test
    for path in tif_paths:
        name = os.path.basename(path)
        print(f"── {name} ──")

        # a) OCR
        full_text = extract_text_from_tiff(path)

        # b) Extract raw document numbers
        docs = extract_document_numbers(full_text)
        print("📄 Document numbers found:", docs or ["<none>"])

        # c) Show full parsed filename stub
        stub = parse_new_filename(full_text)
        print("🗂 Parsed document number:   ", stub, "\n")

if __name__ == '__main__':
    main()