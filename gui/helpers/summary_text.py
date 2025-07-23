from tkinter import ttk

def build_summary_text(parent,
                       num_files: int,
                       num_failures: int,
                       num_updates: int,
                       unmatched: list):
    """
    Displays the high‑level summary text:
      “X files renamed…, Y failed to rename, Z rows updated…, W unmatched…”
    """
    lines = []
    lines.append(f"{num_files} file(s) successfully renamed on disk.")
    if num_failures:
        lines.append(f"{num_failures} file(s) failed to rename.")
    lines.append(f"{num_updates} row(s) updated in spreadsheet.")
    lines.append(f"{len(unmatched)} file(s) unmatched in sheet.")
    summary = "\n".join(lines)
    
    lbl = ttk.Label(
        parent,
        text=summary,
        style="Text.TLabel",
        justify="left"
    )
    lbl.pack(fill="x", padx=20, pady=(0,10))
