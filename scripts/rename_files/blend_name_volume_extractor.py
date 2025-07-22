from typing import List, Dict
from .doc_number_extractor import _DOC_NUM_PATTERN

def extract_title_blocks(text: str, context_lines: int = 20) -> List[str]:
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