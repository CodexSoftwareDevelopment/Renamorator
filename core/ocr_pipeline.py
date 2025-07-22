import os
from typing import Callable, Dict, List
from PIL import Image

# Helpers
from .ocr_utils import extract_text_from_tiff

def run_ocr_pipeline(
    tif_files: List[str],
    status_fn: Dict[str, Callable[[str], None]] = None,
    progress_fn: Callable[[int, int, str], None]   = None,
    log_function: Callable[[str], None]            = print
) -> Dict[str, str]:
    """
    Runs OCR on each TIFF in tif_files, invoking callbacks and returning a
    mapping of file_path -> OCR'd text.

    :param tif_files: list of file paths to .tif images
    :param status_fn: optional dict of callbacks:
                      'processing': file started,
                      'progress':   (file, page_idx, page_total),
                      'ocr_done':   file OCR complete,
                      'error':      file OCR error
    :param progress_fn: optional callback(global_page_count, total_pages, filename)
    :param log_function: optional callable to receive log messages
    :returns: dict mapping filepath to extracted text
    """
    # 1) Pre-scan all files to count pages
    pages_per_file: Dict[str, int] = {}
    total_pages = 0
    for path in tif_files:
        try:
            with Image.open(path) as img:
                n = getattr(img, "n_frames", 1)
        except Exception:
            n = 1
        pages_per_file[path] = n
        total_pages += n

    # initialize overall progress
    if progress_fn:
        progress_fn(0, total_pages, "")

    ocr_texts: Dict[str, str] = {}
    global_page = 0

    # 2) OCR each file
    for path in tif_files:
        fname = os.path.basename(path)
        per_file_done = 0
        n_pages = pages_per_file.get(path, 1)

        # signal file start
        if status_fn and "processing" in status_fn:
            status_fn["processing"](path)
        if progress_fn:
            progress_fn(global_page, total_pages, fname)
        log_function(f"\n=== OCR File: {fname} ({n_pages} pages) ===")

        def page_callback(page_idx: int, _total: int, fp=path):
            nonlocal global_page, per_file_done
            per_file_done += 1
            global_page     += 1
            if status_fn and "progress" in status_fn:
                status_fn["progress"](fp, per_file_done, n_pages)
            if progress_fn:
                progress_fn(global_page, total_pages, fname)

        try:
            text = extract_text_from_tiff(path, page_callback)
            log_function(f"🔍 OCR complete: {fname}")
            ocr_texts[path] = text
            if status_fn and "ocr_done" in status_fn:
                status_fn["ocr_done"](path)
        except Exception as e:
            log_function(f"❌ OCR failed for {fname}: {e}")
            if status_fn and "error" in status_fn:
                status_fn["error"](path)
            # skip to next file
            continue

    return ocr_texts
