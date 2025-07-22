from typing import Callable, Dict, List, Tuple
from .text_parser import parse_new_filename

def run_parse_pipeline(
    ocr_texts: Dict[str, str],
    prompt_meta: Callable[[List[str]], Tuple[str, str]]
) -> Dict[str, str]:
    """
    Given a mapping of filepath→OCR’d text, invoke parse_new_filename(text, prompt_meta)
    to get the final .tif filename, and return a mapping old_path→new_filename.
    """
    mapping: Dict[str, str] = {}
    for path, text in ocr_texts.items():
        # This will call your existing logic:
        #   extract numbers, extract title blocks, prompt via GUI, assemble parts.
        new_name = parse_new_filename(text, prompt_meta)
        mapping[path] = new_name
    return mapping
