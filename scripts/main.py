import os                                    
from scripts.rename_files.file_collector import collect_tif_files
from scripts.rename_files.rename_engine import rename_files
from scripts.change_excel.excel_utils import update_spreadsheet

def main():
    """
    Orchestrator:

+    1) collect .tif files  
+    2) rename them (via OCR + logic) → returns old→new map  
+    3) update spreadsheet with that map
    """

    # 1) Gather all your TIFFs
    tif_files = collect_tif_files('assets/test_files')
    print(f"Dispatching {len(tif_files)} files to renamer…")

    # 2) Rename & map
    mapping = rename_files(tif_files)
    print(f"✅ Renamed {len(mapping)} files.")

    # 3) Push that map into your spreadsheet
    update_spreadsheet(mapping)
    print("✅ Spreadsheet updated with new file names.")

if __name__ == '__main__':
    main()