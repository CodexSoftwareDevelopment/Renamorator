import os
from typing import Dict
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def update_spreadsheet(mapping: Dict[str,str],
                       spreadsheet_path: str = 'data/Archived Protocol Status.xlsx',
                       sheet_name: str = None,
                       doc_col_header: str = "Document Name",
                       header_search_depth: int    = 10) -> None:
    """
    For each old→new filename in `mapping`, find the old basename
    in column `doc_col` and overwrite it with the new basename in `new_col`.
    """
    if not os.path.isfile(spreadsheet_path):
        raise FileNotFoundError(f"Spreadsheet not found: {spreadsheet_path}")

    wb = load_workbook(spreadsheet_path)
    ws = wb[sheet_name] if sheet_name else wb.active

    # 1) Find the header row and column
    doc_col_idx = None
    header_row_idx = None

    for r in range(1, header_search_depth + 1):
        row = ws[r]
        for c_idx, cell in enumerate(row, start=1):
            if str(cell.value).strip() == doc_col_header:
                doc_col_idx    = c_idx
                header_row_idx = r
                break
        if doc_col_idx:
            break

    if doc_col_idx is None:
        raise ValueError(f"Header '{doc_col_header}' not found in rows 1–{header_search_depth}.")

    # 2) Build basename lookup
    basename_map = {
        os.path.basename(old): os.path.basename(new)
        for old, new in mapping.items()
    }

    # 3) Iterate rows *below* the header row
    for row in ws.iter_rows(min_row=header_row_idx + 1):
        cell = row[doc_col_idx - 1]
        val = cell.value
        if not val:
            continue
        old_name = os.path.basename(str(val).strip())
        if old_name in basename_map:
            cell.value = basename_map[old_name]

    # 4) Save changes
    wb.save(spreadsheet_path)
    
    wb.save(spreadsheet_path)