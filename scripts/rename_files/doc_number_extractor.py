import re

# 1) One pattern to match every VP/CVP/AVP variant, longest‑first
_DOC_NUM_PATTERN = re.compile(
    r"\b(?:"
    # ——— AVP variants —————————————
    r"AVP\d{5}\.\d{3}"
    r"|AVP\d{4}\.\d{3}"
    r"|AVP\d{3}\.\d{2}"
    r"|AVP\d{3}\.\d{3}"
    # ——— VP variants —————————————
    r"|VP\d{5}\.\d{3}"
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

# 2) Very forgiving Document# header matcher to catch VP, AVP, CVP prefixes
_HEADER_PREFIX_PATTERN = re.compile(
    r"\bDocument\s*#\s*[:\-\|\s]*?([AC]?VP-?\d{3,5})\b",
    flags=re.IGNORECASE
)

def extract_document_numbers(text: str) -> list[str]:
    """
    Returns all full VP/CVP/AVP codes whose prefix appears
    at least once in a 'Document# <prefix>' header.
    Includes debug output of OCR text to diagnose parsing issues.
    """
    # 1) find all prefixes in headers
    header_prefixes = {
    # normalize by stripping hyphens so 'VP-0001' → 'VP0001'
    m.group(1).upper().replace('-', '')
    for m in _HEADER_PREFIX_PATTERN.finditer(text)
    }
    print("DBG: header_prefixes →", header_prefixes)

    # 2) scan for full codes, but only keep those whose prefix matched above
    seen = set()
    result = []
    for code in _DOC_NUM_PATTERN.findall(text):
        prefix = code.split(".", 1)[0].upper()
        if prefix in header_prefixes and code not in seen:
            seen.add(code)
            result.append(code)

    if not result:
        print("DBG: No document numbers extracted, result is empty list.")
    else:
        print("DBG: extract_document_numbers result →", result)

    return result
