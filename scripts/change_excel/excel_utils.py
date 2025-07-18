import os
from typing import Dict
from openpyxl import load_workbook

def update_spreadsheet(
                        mapping: Dict[str, str],
                        spreadsheet_path: str = 'data/Archived Protocol Status.xlsx',
                        sheet_name: str = 'Document Scanning Tracker',
                        doc_col_header: str = 'Document Name',
                        header_search_depth: int = 10
                    ) -> int:
    """
    For each old→new filename in `mapping`, find the old basename
    (extension‑agnostic) in column `doc_col_header` and overwrite
    it with the new basename. Returns the number of rows updated.
    """
    abs_path = os.path.abspath(spreadsheet_path)
    print(f"Loading workbook: {abs_path}")
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Spreadsheet not found: {abs_path}")

    wb = load_workbook(abs_path)
    print("Available sheets:", wb.sheetnames)
    ws = wb[sheet_name] if sheet_name else wb.active
    print("Using sheet:", ws.title)

    # 1) Find the header row and column
    doc_col_idx = None
    header_row_idx = None
    for r in range(1, header_search_depth + 1):
        for c_idx, cell in enumerate(ws[r], start=1):
            if str(cell.value).strip() == doc_col_header:
                doc_col_idx = c_idx
                header_row_idx = r
                break
        if doc_col_idx:
            break
    if doc_col_idx is None:
        raise ValueError(f"Header '{doc_col_header}' not found in rows 1–{header_search_depth}.")

    print(f"Found '{doc_col_header}' in column {doc_col_idx}, row {header_row_idx}")

    # 2) Build a stem→new‑basename map (strip extensions)
    stem_map = {}
    for old, new in mapping.items():
        stem = os.path.splitext(os.path.basename(old))[0]
        new_stem = os.path.splitext(os.path.basename(new))[0]
        stem_map[stem] = new_stem
    print("Mapping stems to new names:", stem_map)

    # 3) Iterate the first 65 rows below the header, update exact matches
    updated_count = 0

    # Show what old stems we're matching against
    old_stems = list(stem_map.keys())
    print(f"DEBUG: old filename stems to match: {old_stems}")

    for row_idx, row in enumerate(
        ws.iter_rows(min_row=header_row_idx + 1),
        start=header_row_idx + 1
    ):

        cell = row[doc_col_idx - 1]
        sheet_text = str(cell.value).strip() if cell.value else ""

        # only replace if the sheet_text exactly matches one of your old_filename stems
        if sheet_text in stem_map:
            new_stem = stem_map[sheet_text]
            print(f"  MATCH on row {row_idx}!  '{sheet_text}' → '{new_stem}'")
            cell.value = new_stem
            updated_count += 1

    # 4) Save & close
    if updated_count:
        wb.save(abs_path)
        print(f"Saved {updated_count} updates to {abs_path}")
    else:
        print("No matching rows found; no changes made.")
    wb.close()

    return updated_count