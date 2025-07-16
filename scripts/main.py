import os                                    
from scripts.rename_files.file_collector import collect_tif_files
from scripts.rename_files.rename_engine import rename_files

def main():
    """
    Orchestrator: collect .tif files, then hand them off to the renamer.
    """

    if __name__ == '__main__':
        tif_files = collect_tif_files('assets/test_files')
        print(f"Dispatching {len(tif_files)} files to renamer…")
        rename_files(tif_files)
        print(f"{len(tif_files)} files sent to renamer.")
