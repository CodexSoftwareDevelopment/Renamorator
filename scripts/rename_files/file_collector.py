import os

def collect_tif_files(folder_path):
    """
    Return a list of full paths for every .tif or .tiff file
    in the given folder.

    :param folder_path: str — path to the folder containing your .tif files
    :return: list of file paths
    :raises FileNotFoundError: if folder_path doesn’t exist
    """

    # Expand '~' to the user’s home directory
    folder = os.path.expanduser(folder_path)

    # Verify the folder exists
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    # Walk the folder and pick up only .tif files
    tif_paths = [
        os.path.join(folder, name)
        for name in os.listdir(folder)
        if name.lower().endswith(('.tif'))
            and os.path.isfile(os.path.join(folder, name))
    ]

    return tif_paths