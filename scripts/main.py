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
    
    print("🔍  Found TIF files to process:")
    for f in files:
        print("   ", f)
    print(f"   (total {len(files)})\n")

    if not files:
        print("⚠️  No TIF files found; please check the folder path.")
        return

    # 2) Run the renaming pipeline
    result = rename_files(files)

    # 3) Report what got renamed
    for old, new in result.items():
        print(f"{os.path.basename(old)} → {os.path.basename(new)}")

    # 4) Update the Excel spreadsheet
    try:
        updated_count = update_spreadsheet(result)
        if updated_count:
            print("✅ Spreadsheet updated.")
        else:
            print("⚠️ No matching rows; nothing updated.")
    except FileNotFoundError as e:
        print(f"❌ Spreadsheet not found: {e}")
    except ValueError as e:
        print(f"❌ Spreadsheet format error: {e}")
    except Exception as e:
        print(f"⚠️ Failed to update spreadsheet: {e}")

if __name__ == '__main__':
    main()