from tkinter import ttk

def build_summary_text(parent, num_files: int, num_updates: int, unmatched: list):
    """
    Displays the high‑level summary text:
      “X files renamed…, Y rows updated…, Z unmatched…”
    """
    summary = (
        f"{num_files} files renamed on disk.\n"
        f"{num_updates} row(s) updated in spreadsheet.\n"
        f"{len(unmatched)} file(s) unmatched in sheet."
    )
    lbl = ttk.Label(
        parent,
        text=summary,
        style="Text.TLabel",
        justify="left"
    )
    lbl.pack(fill="x", padx=20, pady=(0,10))
