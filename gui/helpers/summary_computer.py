# gui/helpers/summary_computer.py

# Helpers
from core.excel_utils import update_spreadsheet

def compute_summary(mapping: dict,
                    spreadsheet: str,
                   rename_successes: list = None):
    """
    Runs the spreadsheet update and returns:
      - num_files: total files successfully renamed on disk
      - num_updates: number of rows updated in the sheet
      - unmatched: list of file‐stem(s) that couldn't be matched
    """
    # use actual successes count if provided
    num_files = len(rename_successes) if rename_successes is not None else len(mapping)

    num_updates, unmatched = update_spreadsheet(mapping, spreadsheet)

    return num_files, num_updates, unmatched
