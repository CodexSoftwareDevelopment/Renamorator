import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .validations import validate_folder

def build_folder_selector(parent):
    """
    Adds the “1) Select your .tif folder” header, entry box, and Browse button.
    Returns the StringVar holding the chosen folder path.
    """
    # Header
    header = ttk.Label(
        parent,
        text="1) Select your .tif folder",
        style="Header.TLabel"
    )
    header.grid(row=1, column=0, columnspan=2, sticky="w",
                padx=20, pady=(10,5))

    # Entry + Browse
    folder_var = tk.StringVar()
    entry = ttk.Entry(
        parent, textvariable=folder_var,
        style="Text.TLabel", width=50
    )
    entry.grid(row=2, column=0, sticky="w",
               padx=20, pady=5)

    def browse():
        path = filedialog.askdirectory(
            title="Choose folder with .tif files"
        )
        if not path:
            return

        if not validate_folder(path):
            messagebox.showerror(
                "Invalid Folder",
                "Folder must exist and contain at least one .tif file."
            )
            folder_var.set("")
            return

        # only set if it passes validation
        folder_var.set(path)

    btn = ttk.Button(
        parent, text="Browse…", style="Accent.TButton",
        command=browse
    )
    btn.grid(row=2, column=1, sticky="e",
             padx=20, pady=5)

    return folder_var
