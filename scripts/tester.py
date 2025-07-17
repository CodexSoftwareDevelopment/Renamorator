import os

from rename_files.ocr_utils import extract_text_from_tiff
from rename_files.file_collector import collect_tif_files
from rename_files.doc_number_extractor import extract_document_numbers
from rename_files.text_parser import parse_new_filename
from rename_files.blend_name_volume_extractor import (
    extract_title_blocks,
    prompt_for_blend_and_volume,
)

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

        # c) Show full parsed filename stub (without blend/volume)
        stub = parse_new_filename(full_text)
        print("🗂 Parsed filename stub:", stub)

        # d) Extract title blocks around each doc number
        blocks = extract_title_blocks(full_text)
        if blocks:
            # e) Prompt user to supply blend name/volume for each block
            metadata = prompt_for_blend_and_volume(blocks)
            for i, meta in enumerate(metadata, start=1):
                print(f"▶️ Block #{i} metadata:", meta)
        else:
            print("⚠️ No title blocks found to extract blend/volume.")

        print()  # blank line

if __name__ == '__main__':
    main()