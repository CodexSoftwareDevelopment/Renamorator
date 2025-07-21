import os
import tkinter as tk
from tkinter import ttk

def show_unmatched_dialog(parent, unmatched, mapping):
    dlg = tk.Toplevel(parent)
    dlg.title(f"Unmatched Files ({len(unmatched)})")
    tree = ttk.Treeview(dlg, columns=("Old", "New"), show="headings")
    for col, w in [("Old", 200), ("New", 200)]:
        tree.heading(col, text=col)
        tree.column(col, width=w)
    tree.pack(fill="both", expand=True)

    for old in unmatched:
        stem = os.path.splitext(os.path.basename(old))[0]
        new_stem = os.path.splitext(os.path.basename(mapping.get(old, "")))[0]
        tree.insert("", "end", values=(stem, new_stem))

    ttk.Button(dlg, text="Close", command=dlg.destroy).pack(pady=5)
