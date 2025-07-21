import os
from .file_collector import _extend_windows_path
from .ocr_utils import extract_text_from_tiff
from .text_parser import parse_new_filename


def rename_files(tif_paths: list[str]) -> dict[str, str]:
    """
    Rename each TIFF in `tif_paths` by extracting its new name via OCR and parsing.
    Returns a mapping of old_path -> new_path for successful renames.
    """
    mapping: dict[str, str] = {}
    rename_failures = 0
    total = len(tif_paths)

    for index, old_path in enumerate(tif_paths, start=1):
        # Separator and count for readability
        print(f"\n=== Processing file {index}/{total} ===")

        # Display old path (unprefixed for readability on Windows)
        display_old = old_path
        if os.name == "nt" and old_path.startswith("\\\\?\\"):
            display_old = old_path[len("\\\\?\\"):]
        print(f"📂 Old file: {display_old}")

        # 1) OCR
        try:
            text = extract_text_from_tiff(old_path)
            print(f"🔍 OCR extracted text length: {len(text):,}")
        except Exception as e:
            print(f"⚠️ OCR failed for '{display_old}': {e}")
            continue

        # 2) Parse new filename
        new_name = parse_new_filename(text)
        print(f"✏️ Parsed new filename: '{new_name}'")

        # 3) Build and extend new path
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        new_path = _extend_windows_path(new_path)
        display_new = new_path
        if os.name == "nt" and new_path.startswith("\\\\?\\"):
            display_new = new_path[len("\\\\?\\"):]

        # 4) Attempt rename
        try:
            os.rename(old_path, new_path)
            print(f"✅ Renamed -> {display_new}")
            mapping[old_path] = new_path
        except OSError as e:
            print(f"⚠️ Failed to rename '{display_old}' -> '{display_new}': {e}")
            rename_failures += 1
            continue

    # Summary (only counting actual rename attempts that errored)
    success = len(mapping)
    print(f"\n📈 Rename summary: {success} succeeded, {rename_failures} failed.")
    return mapping