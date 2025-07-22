import tkinter as tk
from tkinter import ttk

def prompt_gui_for_meta(parent, blocks):
    dlg = tk.Toplevel(parent)
    dlg.title("Specify Blend & Volume")
    dlg.grab_set()

    # Display each title block with numbering
    txtblk = tk.Text(dlg, height=10, width=60, wrap="word")
    for idx, b in enumerate(blocks, start=1):
        txtblk.insert("end", f"Title Block {idx}:\n")
        txtblk.insert("end", b + "\n")
        txtblk.insert("end", "—" * 40 + "\n")
    txtblk.configure(state="disabled")
    txtblk.pack(padx=10, pady=5)

    frm = ttk.Frame(dlg)
    frm.pack(pady=5, padx=10)
    ttk.Label(frm, text="Blend:").grid(row=0, column=0)
    blend_var = tk.StringVar()
    ttk.Entry(frm, textvariable=blend_var, width=30).grid(row=0, column=1)

    ttk.Label(frm, text="Volume:").grid(row=1, column=0)
    vol_var = tk.StringVar()
    ttk.Entry(frm, textvariable=vol_var, width=30).grid(row=1, column=1)

    def on_ok():
        dlg.destroy()
    ttk.Button(dlg, text="OK", command=on_ok).pack(pady=5)

    parent.wait_window(dlg)
    return blend_var.get() or None, vol_var.get() or None