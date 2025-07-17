import re
from .doc_number_extractor import extract_document_numbers
from .blend_name_volume_extractor import extract_title_blocks, prompt_for_blend_and_volume

def parse_new_filename(ocr_text: str) -> str:
    """
    Build a single new filename by:
      1) Extracting VP/CVP codes for the doc identifier
      2) Showing all title blocks at once and prompting for blend & volume
      3) Combining these pieces with ' - ' and appending .tif
    """
    # 1) Doc number segment
    codes = extract_document_numbers(ocr_text)
    doc_part = " ".join(codes) + " - " if codes else "UNKNOWN - "

    # 2) Title blocks and single prompt
    blocks = extract_title_blocks(ocr_text)
    meta = prompt_for_blend_and_volume(blocks)

    # 3) Build filenames
    parts = [doc_part.rstrip(" -")]
    if meta.get("volume"):
        parts.append(meta["volume"])
    if meta.get("blend"):
        parts.append(meta["blend"])

    return " - ".join(parts) + ".tif"
