import os
from tkinter import ttk

# Helpers
from gui.helpers.folder_selector import build_folder_selector
from gui.helpers.spreadsheet_selector import build_spreadsheet_selector
from gui.helpers.validations import validate_spreadsheet

def build_page(parent, controller):
    controller.geometry("600x200")
    controller.minsize(500, 200)

    # Folder selector → returns folder_var
    folder_var = build_folder_selector(parent)

    # Spreadsheet selector → returns spreadsheet_var
    spreadsheet_var = build_spreadsheet_selector(parent, controller)

    # Spacer
    parent.grid_rowconfigure(6, weight=1)

    # Back button
    ttk.Button(parent, text="Back", style="Accent.TButton",
               command=controller.back)\
       .grid(row=7, column=0, sticky="w", padx=20, pady=20)

    # Process button: start disabled
    process_btn = ttk.Button(
        parent,
        text="Process",
        style="Accent.TButton",
        state="disabled",
        command=lambda: _on_process(controller, folder_var, spreadsheet_var)
    )
    process_btn.grid(row=7, column=1, sticky="e", padx=20, pady=20)

    # Enable Process only when folder and spreadsheet are valid
    def update_process_state(*_):
        folder_path = folder_var.get().strip()
        ss_path = spreadsheet_var.get().strip()
        # Validate folder exists and spreadsheet file
        folder_ok = os.path.isdir(folder_path)
        ss_ok = validate_spreadsheet(ss_path)
        if folder_ok and ss_ok:
            process_btn.state(["!disabled"])
        else:
            process_btn.state(["disabled"])

    # watch all three vars
    folder_var.trace_add("write", update_process_state)
    spreadsheet_var.trace_add("write", update_process_state)

    # **INITIAL STATE** – make sure the button reflects any pre‑filled values
    update_process_state()

    # Column weights
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=0)

def _on_process(controller, folder_var, spreadsheet_var):
    controller.tif_folder = folder_var.get().strip()
    controller.spreadsheet = spreadsheet_var.get().strip()
    controller.last_spreadsheet = controller.spreadsheet
    controller.next()
