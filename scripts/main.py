import os
from rename_files.file_collector import collect_tif_files
from rename_files.rename_engine import rename_files
from change_excel.excel_utils import update_spreadsheet

def main():
    # 1) Gather your TIFFs
    try:
        files = collect_tif_files('assets/test_files')
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    if not files:
        print("⚠️  No TIFF files found; please check the folder path.")
        return

    # 2) Run the renaming pipeline
    result = rename_files(files)

    # 3) Report what got renamed
    for old, new in result.items():
        print(f"{os.path.basename(old)} → {os.path.basename(new)}")

    # 4) Update the Excel spreadsheet
    try:
        update_spreadsheet(result)
        print("✅ Spreadsheet updated.")
    except FileNotFoundError as e:
        print(f"❌ Spreadsheet not found: {e}")
    except ValueError as e:
        print(f"❌ Spreadsheet format error: {e}")
    except Exception as e:
        print(f"⚠️ Failed to update spreadsheet: {e}")

if __name__ == '__main__':
    main()