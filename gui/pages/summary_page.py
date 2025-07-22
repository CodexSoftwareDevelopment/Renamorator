import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.excel_utils import update_spreadsheet

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # Header
    header = ttk.Label(
        parent,
        text="Step 5 of 5: Summary & Finish",
        style="Header.TLabel"
    )
    header.pack(anchor="w", padx=20, pady=(20,10))

    # Perform spreadsheet update
    mapping    = getattr(controller, "final_mapping", {})
    spreadsheet = getattr(controller, "spreadsheet", "")
    try:
        updates, unmatched = update_spreadsheet(mapping, spreadsheet)
    except Exception as e:
        messagebox.showerror("Spreadsheet Error", str(e))
        updates = 0
        unmatched = list(mapping.keys())

    # Summary text
    summary_text = (
        f"{len(mapping)} files renamed on disk.\n"
        f"{updates} row(s) updated in spreadsheet.\n"
        f"{len(unmatched)} file(s) unmatched in sheet."
    )
    ttk.Label(
        parent,
        text=summary_text,
        style="Text.TLabel",
        justify="left"
    ).pack(fill="x", padx=20, pady=(0,10))

    # Lists container
    lists = ttk.Frame(parent, style="Background.TFrame")
    lists.pack(fill="both", expand=True, padx=20)

    # Updated list
    updated_frame = ttk.LabelFrame(lists, text="✅ Spreadsheet Updated", style="Background.TFrame")
    updated_frame.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)
    for old, new in mapping.items():
        stem = os.path.splitext(os.path.basename(old))[0]
        if stem not in unmatched:
            ttk.Label(
                updated_frame,
                text=f"{os.path.basename(old)} → {os.path.basename(new)}",
                style="Text.TLabel"
            ).pack(anchor="w", pady=2)

    # Unmatched list
    unmatched_frame = ttk.LabelFrame(lists, text="⚠️ Unmatched Files", style="Background.TFrame")
    unmatched_frame.pack(side="right", fill="both", expand=True, padx=(10,0), pady=10)
    for stem in unmatched:
        ttk.Label(
            unmatched_frame,
            text=stem,
            style="Text.TLabel"
        ).pack(anchor="w", pady=2)

    # Button bar
    btns = ttk.Frame(parent, style="Background.TFrame")
    btns.pack(fill="x", padx=20, pady=20)

    # Close
    close_btn = ttk.Button(
        btns, text="Close",
        style="Accent.TButton",
        command=controller.destroy
    )
    close_btn.pack(side="left")

    # Download CSV
    def on_download():
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files","*.csv")]
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Old Filename","New Filename"])
                for old, new in mapping.items():
                    writer.writerow([os.path.basename(old), os.path.basename(new)])
            messagebox.showinfo("CSV Saved", f"Saved summary to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    download_btn = ttk.Button(
        btns, text="Download CSV",
        style="Accent.TButton",
        command=on_download
    )
    download_btn.pack(side="left", padx=20)

    # Process More Files
    def on_more():
        # reset any per‐run state if needed
        controller.parse_index     = 0
        controller.parse_mapping   = {}
        controller.final_mapping   = {}
        controller.ocr_results     = {}
        controller.tif_list        = []
        controller.show("folder_page")

    more_btn = ttk.Button(
        btns, text="Process More Files",
        style="Accent.TButton",
        command=on_more
    )
    more_btn.pack(side="right")
