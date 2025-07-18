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
    Displays all title blocks together, then prompts once for blend & volume.
    Returns a single dict {"blend":…, "volume":…}.
    """
    # If there are no blocks, return empties immediately
    if not blocks:
        return {"blend": None, "volume": None}

    # 1) Show every block
    print("\n── Official Title Blocks ──")
    for i, block in enumerate(blocks, start=1):
        print(f"\nBlock #{i}:\n{block}")

    # 2) Prompt once
    blend  = input("\nBlend name (or leave blank): ").strip() or None
    volume = input("Volume (or leave blank): ").strip() or None

    return {"blend": blend, "volume": volume}