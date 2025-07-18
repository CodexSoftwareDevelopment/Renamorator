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
      # ——— CVP variants —————————————
    r"|CVP\.\d{3}\.\d{2}[A-Z]"
    r"|CVP\d{3}\.\d{3}"
    r")\b"
)

# pattern to pull the prefix from the Document# header
_HEADER_PREFIX_PATTERN = re.compile(r"\bDocument#\s*(C?VP\d{3,5})\b")

def extract_document_numbers(text: str) -> list[str]:
    """
    Returns all full VP/CVP codes in the title block **and**
    whose prefix appears at least once in a 'Document# <prefix>' header.
    """
    # 1) find all prefixes in headers
    header_prefixes = {m.group(1) for m in _HEADER_PREFIX_PATTERN.finditer(text)}

    # 2) scan for full codes, but only keep those whose prefix is in header_prefixes
    seen = set()
    result = []
    for code in _DOC_NUM_PATTERN.findall(text):
        prefix = code.split(".", 1)[0]
        if prefix in header_prefixes and code not in seen:
            seen.add(code)
            result.append(code)

    return result
