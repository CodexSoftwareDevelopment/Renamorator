import os 
from .ocr_utils import extract_text_from_tiff
from .text_parser import parse_new_filename

def rename_files(tif_paths: list[str]) -> dict[str, str]:
    """
    For each TIFF:
      • OCR → full_text
      • parse_new_filename → [new_fname1, new_fname2, …]
      • os.rename for each new_fname (you may want to copy or suffix if multiple)
      • record mapping old_path → [new_paths]
    """
    mapping: dict[str, str] = {}

    for old_path in tif_paths:
        print(f"\n----\nProcessing: {os.path.basename(old_path)}")
        try:
            full_text = extract_text_from_tiff(old_path)
        except Exception as e:
            print(f"⚠️ OCR failed for {old_path!r}: {e}")
            continue

        try:
            new_name = parse_new_filename(full_text)
            print(f"  → New filename will be: '{new_name}'")
        except Exception as e:
            print(f"⚠️ Filename parsing failed for {old_path!r}: {e}")
            continue
        
        new_path = os.path.join(os.path.dirname(old_path), new_name)

        try:
            os.rename(old_path, new_path)
            print(f"✅ Renamed to: '{new_name}'")
            mapping[old_path] = new_path
        except OSError as e:
            print(f"⚠️ Failed to rename {old_path!r} → {new_path!r}: {e}")

    return mapping