import re
from typing import List

# Matches 2–3 letters (excluding BWI), a dash, then 2 digits, e.g. MT-03 or FLD-12
_EQUIP_PATTERN = re.compile(r"\b(?!BWI-)[A-Z]{2,3}-\d{2}\b")

def extract_equipment_codes(blocks: List[str]) -> List[str]:
    """
    Given a list of title‑block strings, scan each for equipment codes
    matching YY-XX or YYY-XX (but not BWI-XX), dedupe in order, and return them.

    :param blocks: list of text blocks (from extract_title_blocks)
    :returns: unique list of equipment codes in the order found
    """
    seen = set()
    codes: List[str] = []
    for block in blocks:
        for match in _EQUIP_PATTERN.findall(block):
            if match not in seen:
                seen.add(match)
                codes.append(match)
    return codes
