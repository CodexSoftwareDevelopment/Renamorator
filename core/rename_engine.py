from typing import Callable, Dict, List, Tuple

from .ocr_pipeline    import run_ocr_pipeline
from .parse_pipeline  import run_parse_pipeline
from .file_renamer    import run_rename_pipeline

def rename_files(
    tif_files: List[str],
    prompt_meta: Callable[[List[str]], Tuple[str, str]],
    status_fn: Dict[str, Callable] = None,
    progress_fn: Callable[[int,int,str], None] = None,
    log_function: Callable[[str], None] = print
) -> Tuple[Dict[str,str], Dict[str,str]]:
    """
    Conductor that runs:
      1) OCR → ocr_texts
      2) Prompt & parse → mapping old→new
      3) Physically rename on disk → (successes, failures)
    """

    # Phase 1: OCR
    ocr_texts = run_ocr_pipeline(
        tif_files,
        status_fn=status_fn,
        progress_fn=progress_fn,
        log_function=log_function,
    )

    # Phase 2: Prompt & Parse new filenames
    mapping = run_parse_pipeline(ocr_texts, prompt_meta)

    # Phase 3: Rename on disk
    successes, failures = run_rename_pipeline(mapping, log_function=log_function)

    return successes, failures
