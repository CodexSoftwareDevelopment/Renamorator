import os

from rename_files.file_collector import collect_tif_files
from rename_files.rename_engine import rename_files

def main():
    files = collect_tif_files('assets/test_files')
    result = rename_files(files)
    for old, new in result.items():
        print(f"{os.path.basename(old)} → {os.path.basename(new)}")

if __name__ == '__main__':
    main()