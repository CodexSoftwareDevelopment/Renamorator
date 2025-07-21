import os
import csv
from tkinter import filedialog

def export_csv(unmatched, mapping):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save unmatched file list"
    )
    if not save_path:
        return

    with open(save_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Original Filename", "Proposed New Filename"])
        for old in unmatched:
            stem = os.path.splitext(os.path.basename(old))[0]
            new_stem = os.path.splitext(os.path.basename(mapping.get(old, "")))[0]
            writer.writerow([stem, new_stem])
