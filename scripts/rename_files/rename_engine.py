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
        full_text = extract_text_from_tiff(old_path)
        new_name = parse_new_filename(full_text)
        new_path = os.path.join(os.path.dirname(old_path), new_name)

        os.rename(old_path,new_path)
        mapping[old_path] = new_path

    return mapping