import os 
from concurrent.futures import ThreadPoolExecutor, as_completed
from .ocr_utils import extract_text_from_tiff
from .text_parser import parse_new_filename

def rename_files(tif_paths: list[str]) -> dict[str, str]:
    """
    :param tif_paths: list of full paths to .tif files
    :returns: mapping old_path → new_path
    """
    mapping: dict[str, str] = {}

    # 1) OCR all files in parallel
    with ThreadPoolExecutor() as exe:
        futures = {exe.submit(extract_text_from_tiff, p): p for p in tif_paths}
        for fut in as_completed(futures):
            old_path = futures[fut]
            text = fut.result()

            # 2) Ask the parser module for the new filename
            new_fname = parse_new_filename(text)
            dirpath = os.path.dirname(old_path)
            new_path = os.path.join(dirpath, new_fname)

            # 3) Rename on disk, record mapping
            os.rename(old_path, new_path)
            mapping[old_path] = new_path
    
    return mapping