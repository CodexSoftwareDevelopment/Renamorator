import os, re

def validate_folder(path: str) -> bool:
    """
    Returns True if path is an existing directory containing at least one .tif file.
    """
    if not os.path.isdir(path):
        return False
    try:
        entries = os.listdir(path)
    except Exception:
        return False
    return any(fname.lower().endswith('.tif') for fname in entries)

def validate_spreadsheet(path: str) -> bool:
    """
    Returns True if path is an existing file ending in .xlsx, .xls, or .csv.
    """
    if not os.path.isfile(path):
        return False
    return path.lower().endswith(('.xlsx', '.xls', '.xlsm', '.csv'))

def validate_blend_name(name: str) -> bool:
    """
    Empty is OK. Otherwise must not contain any forbidden characters for filenames:
      < > : " / \ | ? * ;
    """
    if not name:
        return True

    forbidden = set('<>:"/\\|?*;')
    return not any(ch in forbidden for ch in name)

def validate_volume(vol: str) -> bool:
    """
    Empty is OK. Otherwise must be: number[.number]? + optional space + letters.
    Examples: "2 oz", "50gal", "10.5kg"
    """
    if not vol:
        return True
    pattern = r"^\d+(\.\d+)?\s*[A-Za-z]+$"
    return bool(re.fullmatch(pattern, vol))

