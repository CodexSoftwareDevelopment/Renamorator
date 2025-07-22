from typing import List

# Helpers
from .doc_number_extractor import _DOC_NUM_PATTERN


def _is_coherent(line: str) -> bool:
    """
    Heuristic to filter out incoherent lines: must be at least 5 chars,
    contain at least 3 letters, and letters must form at least 30% of the line.
    Exception: any line containing a VP/CVP document number pattern is always kept.
    """
    stripped = line.strip()
    # exception: keep lines that include a doc-number pattern
    if _DOC_NUM_PATTERN.search(stripped):
        return True
    if len(stripped) < 5:
        return False
    letters = sum(c.isalpha() for c in stripped)
    if letters < 3 or (letters / len(stripped)) < 0.3:
        return False
    return True


def extract_title_blocks(text: str, context_lines: int = 20) -> List[str]:
    """
    Find every line containing a VP/CVP code, and grab the preceding
    `context_lines` lines as the "official title block", then filter
    out incoherent lines (random strings of numbers/letters).
    Lines matching the doc-number pattern are preserved regardless of coherence rules.

    :param text: Full OCR'd text
    :param context_lines: How many lines before the doc-number to include
    :returns: List of filtered title blocks (one per code match)
    """
    lines = text.splitlines()
    blocks: List[str] = []

    for idx, line in enumerate(lines):
        if _DOC_NUM_PATTERN.search(line):
            start = max(0, idx - context_lines)
            raw_block = lines[start:idx]
            # keep coherent lines or any that match the doc-number pattern
            filtered = [ln for ln in raw_block if _is_coherent(ln)]
            block = "\n".join(filtered)
            if block:
                blocks.append(block)
    return blocks
