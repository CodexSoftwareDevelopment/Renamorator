import re

# 1) One pattern to match every VP/CVP variant, longest‑first
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

# 2) Very forgiving Document# header matcher
_HEADER_PREFIX_PATTERN = re.compile(
    r"\bDocument\s*#\s*[:\-\|\s]*?(C?VP\d{3,5})\b",
    flags=re.IGNORECASE
)

def extract_document_numbers(text: str) -> list[str]:
    """
    Returns all full VP/CVP codes whose prefix appears
    at least once in a 'Document# <prefix>' header.
    """

    print("\n=== First 100 lines of OCR’d text ===")
    for i, line in enumerate(text.splitlines()[:100]):
        print(f"[{i:03d}]", repr(line))
    print("====================================\n")

    # ——— DEBUG: dump every OCR'd "Document" line ———
    print("\n=== OCR’d lines containing 'Document' ===")
    for i, line in enumerate(text.splitlines()):
        if "Document" in line:
            print(f"[line {i:03d}]: {line!r}")
    print("============================================\n")

    # 1) find all prefixes in headers
    header_prefixes = {m.group(1) for m in _HEADER_PREFIX_PATTERN.finditer(text)}
    print("DBG: header_prefixes →", header_prefixes)

    # 2) scan for full codes, but only keep those whose prefix matched above
    seen = set()
    result = []
    for code in _DOC_NUM_PATTERN.findall(text):
        prefix = code.split(".", 1)[0]
        if prefix in header_prefixes and code not in seen:
            seen.add(code)
            result.append(code)

    # 3) return either the matched codes or empty list (UNKNOWN fallback happens upstream)
    return result