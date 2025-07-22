import tkinter as tk
from tkinter import ttk

from gui.helpers.folder_selector import build_folder_selector
from gui.helpers.spreadsheet_selector import build_spreadsheet_selector

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # --- Logo & Step Indicator (Row 0) ---
    logo = ttk.Label(parent, text="Namewise", style="Logo.TLabel")
    logo.grid(row=0, column=0, sticky="w", padx=20, pady=(20,5))

    step = ttk.Label(parent, text="Step 1 of 4", style="Text.TLabel")
    step.grid(row=0, column=1, sticky="e", padx=20, pady=(20,5))

    # --- Folder selector (Rows 1–2) ---
    folder_var = build_folder_selector(parent)

    # --- Spreadsheet selector (Rows 3–5) ---
    spreadsheet_var, same_var = build_spreadsheet_selector(parent, controller)

    # --- Spacer to push button to bottom ---
    parent.grid_rowconfigure(6, weight=1)

    # --- Process button (Row 7) ---
    def on_process():
        # Save to controller for later pages
        controller.tif_folder = folder_var.get().strip()
        if same_var.get() and getattr(controller, "last_spreadsheet", ""):
            controller.spreadsheet = controller.last_spreadsheet
        else:
            controller.spreadsheet = spreadsheet_var.get().strip()
        controller.last_spreadsheet = controller.spreadsheet

        controller.next()

    btn = ttk.Button(
        parent,
        text="Process",
        style="Accent.TButton",
        command=on_process
    )
    btn.grid(row=7, column=1, sticky="e", padx=20, pady=20)

    # --- Column weight config ---
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=0)
