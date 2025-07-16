import os

from rename_files.ocr_utils import extract_text_from_tiff
from rename_files.file_collector import collect_tif_files

if __name__ == '__main__':
    assets_folder = os.path.join('assets', 'test_files')

    try:
        tif_paths = collect_tif_files(assets_folder)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        exit(1)

    print(f"🔍 Found {len(tif_paths)} TIFF files. Running OCR...\n")

    for path in tif_paths:
        name = os.path.basename(path)
        print(f"── OCR output for {name} ──")
        full_text = extract_text_from_tiff(path)
        preview = full_text.replace('\n', ' ')[:300]
        more = "..." if len(full_text) > 300 else ""
        print(preview + more + "\n")