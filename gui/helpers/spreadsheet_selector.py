import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Helpers 
from .validations import validate_spreadsheet

def build_spreadsheet_selector(parent, controller):
    """
    Adds the “2) Select spreadsheet…” header, entry, and Browse button.
    Returns spreadsheet_var.
    """
    # Header
    ss_header = ttk.Label(
        parent,
        text="Select spreadsheet to update"
    )
    ss_header.grid(row=3, column=0, columnspan=2, sticky="w",
                   padx=20, pady=(15,5))

    # Entry + Browse
    last_ss = getattr(controller, "last_spreadsheet", "")
    spreadsheet_var = tk.StringVar(value=last_ss)

    entry = ttk.Entry(
        parent, textvariable=spreadsheet_var,
        width=85
    )
    entry.grid(row=4, column=0, sticky="w",
               padx=20, pady=5)

    def browse():
        path = filedialog.askopenfilename(
            title="Choose spreadsheet",
            filetypes=[("Excel/CSV", "*.xlsx *.xls *.xlsm *.csv")]
        )
        if not path:
            return

        if not validate_spreadsheet(path):
            messagebox.showerror(
                "Invalid File",
                "Please select a .xlsx, .xls, .xlsm or .csv file."
            )
            spreadsheet_var.set("")
            return

        spreadsheet_var.set(path)

    btn = ttk.Button(
        parent, text="Browse…", style="Accent.TButton",
        command=browse
    )
    btn.grid(row=4, column=1, sticky="e",
             padx=20, pady=5)

    return spreadsheet_var