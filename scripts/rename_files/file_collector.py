import os

def _extend_windows_path(path: str) -> str:
    """
    On Windows, prefix "\\\\?\\" to bypass the 260‑char MAX_PATH limit.
    Otherwise just return the absolute path.
    """
    abs_path = os.path.abspath(path)
    # On NT, if not already extended, add the \\?\ prefix
    if os.name == "nt" and not abs_path.startswith("\\\\?\\"):
        return "\\\\?\\" + abs_path
    return abs_path

def collect_tif_files(folder_path: str) -> list[str]:
    """
    Return a list of full paths for every .tif file in the given folder,
    handling long filenames on Windows.

    :param folder_path: str — path to the folder containing your .tif files
    :return: list of file paths
    :raises FileNotFoundError: if folder_path doesn’t exist
    """
    # 1) Normalize/extend the folder path
    folder = _extend_windows_path(folder_path)

    # 2) Verify it exists
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    # 3) Show exactly what’s in the directory
    names = os.listdir(folder)
    print("DEBUG raw names in folder:")
    for n in names:
        print("   ", repr(n))

    # 4) Collect only real .tif files
    tif_paths: list[str] = []
    for name in names:
        clean_name = name.strip()
        if clean_name.lower().endswith('.tif'):
            candidate = _extend_windows_path(os.path.join(folder, clean_name))
            if os.path.isfile(candidate):
                tif_paths.append(candidate)
            else:
                print(f"⚠️ Skipping (not a file or inaccessible): {candidate}")

    return tif_paths