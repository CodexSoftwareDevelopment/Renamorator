import re

# 1) One pattern to match every VPxxx case, longest-first:
_DOC_NUM_PATTERN = re.compile(
    r"\b(?:"
      # ——— VP variants —————————————
      r"VP\d{5}\.\d{3}"
    r"|VP\d{5}\.\d{2}[A-Z]"
    r"|VP\d{4}[A-Z]\.\d{3}"
    r"|VP\d{4}\.\d{2}[A-Z]"
    r"|VP\d{4}\.\d{3}"
    r"|VP\d{3}[A-Z]\.\d{3}"
    r"|VP\d{3}\.\d{2}[A-Z]"
    r"|VP\d{3}\.\d{3}"
    r"|VP\d{3}"
      # ——— CVP variants —————————————
    r"|CVP\.\d{3}\.\d{2}[A-Z]"
    r"|CVP\d{3}\.\d{3}"
    r"|CVP\d{3}"
    r")\b"
)

def extract_document_numbers(text: str) -> list[str]:
    """
    Scan `text` for all VP‑codes matching your nine formats,
    return each unique one in the order found.
    """
    raw = _DOC_NUM_PATTERN.findall(text)
    seen = set()
    unique = []
    for code in raw:
        if code not in seen:
            seen.add(code)
            unique.append(code)
    return unique
