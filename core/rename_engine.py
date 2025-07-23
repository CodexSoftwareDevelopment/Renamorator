import os
from collections import defaultdict
from typing import Callable, Dict, List, Tuple

# Helpers
from .ocr_pipeline    import run_ocr_pipeline
from .parse_pipeline  import run_parse_pipeline
from .file_renamer    import run_rename_pipeline

def rename_files(
        tif_files: List[str],
        prompt_meta: Callable[[List[str]], Tuple[str, str]],
        status_fn: Dict[str, Callable] = None,
        progress_fn: Callable[[int, int], None] = None
):
    status_fn = status_fn or {}
    log    = status_fn.get('log', lambda msg: None)
    error  = status_fn.get('error', lambda msg: None)
    status = status_fn.get('status', lambda msg: None)

    renamed_files = []
    name_counts = defaultdict(int)
    base_name_map = defaultdict(list)

    for i, tif_file in enumerate(tif_files):
        try:
            if progress_fn: progress_fn(i, len(tif_files))
            status(f"OCR'ing {os.path.basename(tif_file)}")
            ocr_text = run_ocr_pipeline(tif_file)

            status("Parsing text")
            parsed = run_parse_pipeline(ocr_text)

            status("Waiting for user input")
            blend_name, volume = prompt_meta(parsed)

            status("Renaming file")
            new_name = run_rename_pipeline(tif_file, parsed, blend_name, volume)

            # Store base name for later suffixing and remove .tif for .xlsx listing
            name_counts[new_name] += 1
            base_name_map[new_name].append(tif_file)

            renamed_files.append((tif_file, new_name))

        except Exception as e:
            error(f"Error processing {tif_file}: {e}")

    # Apply suffixes for duplicates starting with (1), (2), ... including first
    final_renamed_files = []
    for base_name, files in base_name_map.items():
        for idx, original_file in enumerate(files, start=1):
            suffixed_name = f"{base_name} ({idx})"
            # Append back .tif for actual renaming, but strip it from .xlsx entries
            actual_file_name = f"{suffixed_name}.tif"
            final_renamed_files.append((original_file, actual_file_name))

    return [(src, dest.replace('.tif', '')) for src, dest in final_renamed_files]
