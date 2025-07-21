import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from rename_files.rename_engine import rename_files
from change_excel.excel_utils import update_spreadsheet
from gui_helpers.dialogs import show_unmatched_dialog
from gui_helpers.prompts import prompt_gui_for_meta

def run_gui():
    root = tk.Tk()
    root.title("Renamorator")
    root.geometry("800x600")
    root.resizable(True, True)

    frm_top = ttk.Frame(root)
    frm_top.pack(fill="x", pady=10, padx=10)

    lbl = ttk.Label(frm_top, text="1) Select folder with your .tif files:")
    lbl.pack(side="left")
    folder_var = tk.StringVar()
    ent = ttk.Entry(frm_top, textvariable=folder_var, width=50)
    ent.pack(side="left", padx=5)

    def browse():
        d = filedialog.askdirectory()
        if d:
            folder_var.set(d)
    ttk.Button(frm_top, text="Browse…", command=browse).pack(side="left")

    start_btn = ttk.Button(frm_top, text="Start Processing")
    start_btn.pack(side="left", padx=10)

    frm_logs = ttk.Frame(root)
    frm_logs.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    txt = tk.Text(frm_logs, wrap="none")
    txt.configure(state="disabled")
    txt.pack(side="left", fill="both", expand=True)

    vsb = ttk.Scrollbar(frm_logs, orient="vertical", command=txt.yview)
    vsb.pack(side="right", fill="y")
    txt.configure(yscrollcommand=vsb.set)

    def log(line: str):
        txt.configure(state="normal")
        txt.insert("end", line + "\n")
        txt.see("end")
        txt.configure(state="disabled")

    def on_start():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning("Pick a folder first", "Please select your TIFF folder.")
            return

        try:
            tif_files = [
                os.path.join(folder, f) for f in os.listdir(folder)
                if f.lower().endswith(".tif")
            ]
            if not tif_files:
                messagebox.showinfo("No Files", "No .tif files found in the selected folder.")
                return
            log(f"🔍 Found {len(tif_files)} TIF files.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            mapping = rename_files(
                tif_files,
                log_fn=log,
                prompt_fn=lambda blocks: prompt_gui_for_meta(root, blocks)
            )
        except Exception as e:
            log(f"❌ Rename process failed: {e}")
            messagebox.showerror("Rename Error", str(e))
            return

        try:
            updates, unmatched = update_spreadsheet(mapping)
            log(f"\n📈 Spreadsheet: {updates} updated, {len(unmatched)} unmatched.")
            show_unmatched_dialog(root, unmatched, mapping)
        except Exception as e:
            log(f"⚠️ Spreadsheet update failed: {e}")
            messagebox.showerror("Spreadsheet Error", str(e))

    start_btn.config(command=on_start)
    root.mainloop()
