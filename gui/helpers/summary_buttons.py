import os
import csv
from tkinter import filedialog, messagebox
from tkinter import ttk

def build_button_bar(parent, controller):
    """
    Creates Close, Download CSV, and Process More Files buttons.
    """
    # Close
    close_btn = ttk.Button(
        parent,
        text="Close",
        style="Accent.TButton",
        command=controller.destroy
    )
    close_btn.pack(side="left")

    # Download CSV
    def on_download():
        mapping = getattr(controller, "final_mapping", {})
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
                    writer.writerow([
                        os.path.basename(old),
                        os.path.basename(new)
                    ])
            messagebox.showinfo("CSV Saved", f"Saved summary to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    download_btn = ttk.Button(
        parent,
        text="Download CSV",
        style="Accent.TButton",
        command=on_download
    )
    download_btn.pack(side="left", padx=20)

    # Process More Files
    def on_more():
        # Reset per‑run state on the controller
        for attr in ("parse_index", "parse_mapping", "final_mapping", "ocr_results", "tif_list"):
            if hasattr(controller, attr):
                setattr(controller, attr, {} if "mapping" in attr else [])
        # Go back to folder page
        controller.show("folder_page")

    more_btn = ttk.Button(
        parent,
        text="Process More Files",
        style="Accent.TButton",
        command=on_more
    )
    more_btn.pack(side="right")
