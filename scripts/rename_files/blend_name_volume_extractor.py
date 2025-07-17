import re
from typing import List, Dict
from .doc_number_extractor import _DOC_NUM_PATTERN

def extract_title_blocks(text: str, context_lines: int = 8) -> List[str]:
    """
    Find every line containing a VP/CVP code, and grab the preceding
    `context_lines` lines as the "official title block."

    :param text: Full OCR'd text
    :param context_lines: How many lines before the doc-number to include
    :returns: List of title blocks (one per code match)
    """
    lines = text.splitlines()
    blocks: List[str] = []

    for idx, line in enumerate(lines):
        if _DOC_NUM_PATTERN.search(line):
            start = max(0, idx - context_lines)
            block = "\n".join(lines[start:idx])
            blocks.append(block)
    return blocks

def prompt_for_blend_and_volume(blocks: List[str]) -> List[Dict[str, str]]:
    """
    For each title block, display it and ask the user to copy/paste or confirm
    the blend name and volume. Returns a list of metadata dicts:
    [{"blend": ..., "volume": ...}, ...]
    """
    results: List[Dict[str, str]] = []
    for i, block in enumerate(blocks, start=1):
        print(f"\n── Title Block #{i} ──")
        print(block)
        blend = input("Blend name (or leave blank): ").strip() or None
        volume = input("Volume (or leave blank): ").strip() or None
        results.append({"blend": blend, "volume": volume})
    return results