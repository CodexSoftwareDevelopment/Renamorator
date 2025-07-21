from typing import Callable, List, Tuple
import re
from .doc_number_extractor import extract_document_numbers
from .blend_name_volume_extractor import extract_title_blocks
from .equipment_code_extractor import extract_equipment_codes

def parse_new_filename(
    ocr_text: str,
    prompt_meta: Callable[[List[str]], Tuple[str, str]]
) -> str:
    """
    Build a new filename by extracting metadata and prompting the user (GUI or CLI).

    Arguments:
        - ocr_text: OCR'd full document text
        - prompt_meta: function to prompt user for blend/volume, given blocks

    Returns:
        New .tif filename
    """
    # 1) Document numbers
    try:
        codes = extract_document_numbers(ocr_text)
    except re.error as e:
        print(f"⚠️ Document‐number regex failed: {e}")
        codes = []

    doc_part = " ".join(codes) + " - " if codes else "UNKNOWN - "

    # 2) Title blocks and prompt for blend/volume
    try:
        blocks = extract_title_blocks(ocr_text)
    except re.error as e:
        print(f"⚠️ Title-block regex failed: {e}")
        blocks = []

    blend, volume = prompt_meta(blocks)

    # 3) Assemble parts
    parts = [doc_part.rstrip(" -")]
    if blend:
        parts.append(blend)
    if volume:
        parts.append(volume)

    try:
        equip_codes = extract_equipment_codes(blocks)
        if equip_codes:
            parts.append(" ".join(equip_codes))
    except Exception as e:
        print(f"⚠️ Equipment-code parsing failed: {e}")

    return " - ".join(parts) + ".tif"
