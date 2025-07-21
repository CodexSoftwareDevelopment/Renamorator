import os
from PIL import Image
from typing import Callable, Dict, List, Tuple

from .file_collector import _extend_windows_path
from .text_parser import parse_new_filename
from .ocr_utils import extract_text_from_tiff

def rename_files(
    tif_files: List[str],
    log_function: Callable[[str], None] = print,
    prompt_fn: Callable[[List[str]], Tuple[str, str]] = None,
    progress_fn: Callable[[int, int, str], None] = None,
    status_fn: Dict[str, Callable] = None
) -> Dict[str, str]:
    """
    Two‑phase pipeline:
      1) OCR PASS: OCR every file (pages in parallel), reporting per‑page & overall progress
      2) PROMPT & RENAME PASS: once all OCR is done, prompt+rename each file

    status_fn keys:
      'processing' – OCR start
      'progress'   – each page
      'ocr_done'   – OCR finish (stop timer)
      'done'       – rename success
      'error'      – any failure
    """
    # 1) Pre-scan pages for total count
    pages_per_file: Dict[str,int] = {}
    total_pages = 0
    for path in tif_files:
        with Image.open(path) as img:
            try:
                n = img.n_frames
            except AttributeError:
                n = 0
                while True:
                    try:
                        img.seek(n)
                        n += 1
                    except EOFError:
                        break
        pages_per_file[path] = n
        total_pages += n

    # initialize overall
    if progress_fn:
        progress_fn(0, total_pages, "")

    ocr_texts: Dict[str,str] = {}
    global_page = 0

    # Phase 1: OCR each file one at a time
    for idx, path in enumerate(tif_files, start=1):
        fname = os.path.basename(path)
        per_file_done = 0
        n_pages = pages_per_file[path]

        # File start
        if status_fn and "processing" in status_fn:
            status_fn["processing"](path)
        if progress_fn:
            progress_fn(global_page, total_pages, fname)
        log_function(f"\n=== OCR File {idx}/{len(tif_files)}: {fname} ===")

        def page_cb(page_idx: int, _n: int, fp=path):
            # monotonic counters
            nonlocal global_page, per_file_done
            per_file_done += 1
            global_page     += 1
            if status_fn and "progress" in status_fn:
                status_fn["progress"](fp, per_file_done, n_pages)
            if progress_fn:
                progress_fn(global_page, total_pages, fname)

        # Run OCR
        try:
            text = extract_text_from_tiff(path, page_callback=page_cb)
            log_function(f"🔍 OCR complete ({len(text)} chars): {fname}")
            ocr_texts[path] = text
            # **Stop the timer now that OCR is done**
            if status_fn and "ocr_done" in status_fn:
                status_fn["ocr_done"](path)
        except Exception as e:
            log_function(f"❌ OCR failed for {fname}: {e}")
            if status_fn and "error" in status_fn:
                status_fn["error"](path)
            continue

    # Phase 2: Prompt & rename
    mapping: Dict[str,str] = {}
    failures = 0

    for idx, path in enumerate(tif_files, start=1):
        if path not in ocr_texts:
            continue

        fname = os.path.basename(path)
        text  = ocr_texts[path]
        log_function(f"\n=== Prompt & Rename {idx}/{len(ocr_texts)}: {fname} ===")

        # Prompt & parse
        try:
            new_name = parse_new_filename(text, prompt_meta=prompt_fn)
            log_function(f"✏️ Parsed new filename: {new_name}")
        except Exception as e:
            log_function(f"⚠️ Prompt/parse failed for {fname}: {e}")
            if status_fn and "error" in status_fn:
                status_fn["error"](path)
            continue

        # Rename
        new_path = os.path.join(os.path.dirname(path), new_name)
        new_path = _extend_windows_path(new_path)
        try:
            os.rename(path, new_path)
            log_function(f"✅ Renamed → {new_name}")
            mapping[path] = new_path
            if status_fn and "done" in status_fn:
                status_fn["done"](path)
        except Exception as e:
            log_function(f"❌ Rename failed for {fname}: {e}")
            failures += 1
            if status_fn and "error" in status_fn:
                status_fn["error"](path)

    log_function(f"\n📈 Finished: {len(mapping)} succeeded, {failures} failed.")
    return mapping
