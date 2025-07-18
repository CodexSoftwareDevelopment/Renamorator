import re
from .doc_number_extractor import extract_document_numbers
from .blend_name_volume_extractor import extract_title_blocks, prompt_for_blend_and_volume
from .equipment_code_extractor import extract_equipment_codes

def parse_new_filename(ocr_text: str) -> str:
    """
    Build a single new filename by:
      1) Extracting VP/CVP codes for the doc identifier
      2) Showing all title blocks at once and prompting for blend & volume
      3) Combining these pieces with ' - ' and appending .tif
    """
    # 1) Doc number segment
    try:
        codes = extract_document_numbers(ocr_text)
    except re.error as e:
        print(f"⚠️ Document‐number regex failed: {e}")
        codes = []

    doc_part = " ".join(codes) + " - " if codes else "UNKNOWN - "

    # 2) Title blocks and single prompt
    try:
        blocks = extract_title_blocks(ocr_text)
    except re.error as e:
        print(f"⚠️ Document‐number regex failed: {e}")
        blocks = []

    meta = prompt_for_blend_and_volume(blocks)

    # 3) Assemble base parts: doc_part, volume, blend
    parts = [doc_part.rstrip(" -")]
    if meta.get("blend"):
        parts.append(meta["blend"])
    if meta.get("volume"):
        parts.append(meta["volume"])

    # 4) Equipment codes: only from the same title blocks
    try:
        equip_codes = extract_equipment_codes(blocks)
    except re.error as e:
        print(f"⚠️ Document‐number regex failed: {e}")
        equip_codes = []
        
    if equip_codes:
        parts.append(" ".join(equip_codes))

    # Final filename
    return " - ".join(parts) + ".tif"
