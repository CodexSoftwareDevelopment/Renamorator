import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Helpers 
from .validations import validate_spreadsheet

def build_spreadsheet_selector(parent, controller):
    """
    Adds the “2) Select spreadsheet…” header, entry, Browse button,
    and “Same spreadsheet as last session” checkbox.
    Returns (spreadsheet_var, same_checkbox_var).
    """
    # Header
    ss_header = ttk.Label(
        parent,
        text="2) Select spreadsheet to update",
        style="Header.TLabel"
    )
    ss_header.grid(row=3, column=0, columnspan=2, sticky="w",
                   padx=20, pady=(15,5))

    # Entry + Browse
    last_ss = getattr(controller, "last_spreadsheet", "")
    spreadsheet_var = tk.StringVar(value=last_ss)

    entry = ttk.Entry(
        parent, textvariable=spreadsheet_var,
        style="Text.TLabel", width=50
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

    # Checkbox: same as last session
    same_var = tk.BooleanVar(value=bool(last_ss))

    def toggle():
        if same_var.get():
            entry.state(["disabled"])
            btn.state(["disabled"])
        else:
            entry.state(["!disabled"])
            btn.state(["!disabled"])
            # on re‑enable, re‑validate whatever’s in the box
            if spreadsheet_var.get() and not validate_spreadsheet(spreadsheet_var.get()):
                messagebox.showerror(
                    "Invalid File",
                    "Please select a .xlsx, .xls, .xlsm or .csv file."
                )
                spreadsheet_var.set("")

    cb = ttk.Checkbutton(
        parent,
        text="Same spreadsheet as last session",
        variable=same_var,
        style="Text.TLabel",
        command=toggle
    )
    cb.grid(row=5, column=0, columnspan=2, sticky="w",
            padx=20, pady=(5,10))

    # initialize disabled if reusing
    if last_ss:
        entry.state(["disabled"])
        btn.state(["disabled"])

    return spreadsheet_var, same_var