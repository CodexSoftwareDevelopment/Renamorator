import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from rename_files.rename_engine import rename_files
from change_excel.excel_utils import update_spreadsheet
from gui_helpers.dialogs import show_unmatched_dialog
from gui_helpers.prompts import prompt_gui_for_meta
from gui_helpers.progress import OCRProgressUI

def run_gui():
    root = tk.Tk()
    root.title("Renamorator")
    root.geometry("1000x700")
    root.resizable(True, True)

    # Top controls
    frm_top = ttk.Frame(root)
    frm_top.pack(fill="x", pady=10, padx=10)

    ttk.Label(frm_top, text="1) Select folder with your .tif files:").pack(side="left")
    folder_var = tk.StringVar()
    ttk.Entry(frm_top, textvariable=folder_var, width=50).pack(side="left", padx=5)

    def get_tif_files(folder):
        return [os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(".tif")]

    current_file_list: list[str] = []

    def browse():
        folder = filedialog.askdirectory()
        if not folder:
            return
        folder_var.set(folder)
        tif_files = get_tif_files(folder)
        log(f"📂 Found {len(tif_files)} TIF files.")
        progress_ui.initialize_files(tif_files)
        current_file_list.clear()
        current_file_list.extend(tif_files)

    ttk.Button(frm_top, text="Browse…", command=browse).pack(side="left")
    start_btn = ttk.Button(frm_top, text="Start Processing")
    start_btn.pack(side="left", padx=10)

    # Progress UI
    progress_ui = OCRProgressUI(root)
    progress_ui.pack(fill="both", expand=True, padx=10, pady=(0,10))

    # Log area
    frm_logs = ttk.Frame(root)
    frm_logs.pack(fill="both", expand=True, padx=10, pady=(0,10))
    txt = tk.Text(frm_logs, wrap="none", state="disabled")
    txt.pack(side="left", fill="both", expand=True)
    vsb = ttk.Scrollbar(frm_logs, orient="vertical", command=txt.yview)
    vsb.pack(side="right", fill="y")
    txt.configure(yscrollcommand=vsb.set)

    def log(msg: str):
        txt.configure(state="normal")
        txt.insert("end", msg + "\n")
        txt.see("end")
        txt.configure(state="disabled")

    def on_start():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning("Pick a folder first", "Please select your TIFF folder.")
            return

        tif_files = get_tif_files(folder)
        if not tif_files:
            messagebox.showinfo("No Files", "No .tif files found.")
            return
        log(f"🔍 Found {len(tif_files)} TIF files.")
        progress_ui.initialize_files(tif_files)
        start_btn.config(state="disabled")

        def worker():
            try:
                mapping = rename_files(
                    tif_files,
                    log_function=lambda msg: root.after(0, log, msg),
                    prompt_fn=lambda blocks: prompt_gui_for_meta(root, blocks),
                    progress_fn=lambda count, total, fname: root.after(
                        0, progress_ui.update_overall_progress, count, total, fname
                    ),
                    status_fn={
                        "processing": lambda p: root.after(0, progress_ui.set_status_processing, p),
                        "progress":   lambda p, i, n: root.after(0, progress_ui.set_status_progress, p, i, n),
                        "ocr_done":   lambda p: root.after(0, progress_ui.set_status_ocr_done, p),
                        "done":       lambda p: root.after(0, progress_ui.set_status_done, p),
                        "error":      lambda p: root.after(0, progress_ui.set_status_error, p),
                    }
                )
                # finish on main thread
                def finish():
                    try:
                        ups, unmatched = update_spreadsheet(mapping)
                        log(f"\n📈 Spreadsheet: {ups} updated, {len(unmatched)} unmatched.")
                        show_unmatched_dialog(root, unmatched, mapping)
                    finally:
                        start_btn.config(state="normal")
                root.after(0, finish)
            except Exception as e:
                root.after(0, lambda: [
                    log(f"❌ Rename process failed: {e}"),
                    messagebox.showerror("Error", str(e)),
                    start_btn.config(state="normal")
                ])

        threading.Thread(target=worker, daemon=True).start()

    start_btn.config(command=on_start)
    root.mainloop()
