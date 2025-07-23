import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image

class OCRProgressUI:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="OCR Progress", padding=10)
        self.current_file_var = tk.StringVar(value="Waiting…")
        ttk.Label(self.frame, textvariable=self.current_file_var).pack(anchor="w")

        # overall progress
        self.overall = ttk.Progressbar(self.frame, length=500, mode="determinate")
        self.overall.pack(fill="x", pady=(0,10))

        # scrollable list for per-file progress
        self.canvas = tk.Canvas(self.frame)
        self.scroll_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # maps normalized absolute path -> (lbl, pb, pages, timer, icon)
        self.file_widgets = {}
        self._start_times = {}
        self._timer_jobs = {}

    def pack(self, **kw):
        self.frame.pack(**kw)

    def _normalize_key(self, file_path: str) -> str:
        """
        Normalize file paths by:
          1. Stripping Windows extended-length prefix (\\\\?\\)
          2. Collapsing redundant separators/up-level references
          3. Converting to absolute path
          4. Lower-casing for case-insensitive matching
        """
        p = file_path
        # strip extended-length prefix
        if p.startswith("\\\\?\\"):
            p = p[4:]
        # normalize separators and up-levels
        p = os.path.normpath(p)
        # convert to absolute path
        p = os.path.abspath(p)
        return p.lower()

    def initialize_files(self, file_paths):
        # clear existing widgets and timers
        for w in self.inner.winfo_children():
            w.destroy()
        self.file_widgets.clear()
        for job in list(self._timer_jobs.values()):
            self.frame.after_cancel(job)
        self._timer_jobs.clear()
        self._start_times.clear()

        # reset overall progressbar
        self.overall["value"] = 0
        self.overall["maximum"] = 0
        self.current_file_var.set(f"Ready to process {len(file_paths)} files.")

        # populate per-file rows
        for p in file_paths:
            row = ttk.Frame(self.inner)
            name = os.path.basename(p)
            lbl = ttk.Label(row, text=name, width=40, anchor="w")
            pb = ttk.Progressbar(row, length=180, mode="determinate")
            # determine total pages
            try:
                img = Image.open(p)
                total_pages = getattr(img, "n_frames", 1)
            except Exception:
                total_pages = 0
            pb["maximum"] = total_pages
            pages = ttk.Label(row, text=f"0/{total_pages} pages", width=12)
            timer = ttk.Label(row, text="00:00", width=8)
            icon = ttk.Label(row, text="", width=2)

            # layout
            lbl.pack(side="left", padx=(0,5))
            pb.pack(side="left", padx=(0,5))
            pages.pack(side="left", padx=(0,5))
            timer.pack(side="left", padx=(0,5))
            icon.pack(side="left")
            row.pack(fill="x", pady=2)

            # store widgets under normalized absolute key
            key = self._normalize_key(p)
            self.file_widgets[key] = (lbl, pb, pages, timer, icon)

    def update_overall_progress(self, count, total, filename):
        self.overall["maximum"] = total
        self.overall["value"] = count
        self.current_file_var.set(f"Processing {filename} ({count}/{total} files)")

    def set_status_processing(self, file_path):
        key = self._normalize_key(file_path)
        lbl, pb, pages, timer, icon = self.file_widgets[key]
        # reset progress for new file
        pb["value"] = 0
        pages.config(text=f"0/{int(pb['maximum'])} pages")
        icon.config(text="")
        # start timer
        self._start_times[key] = datetime.now()
        def tick():
            start = self._start_times.get(key)
            if not start:
                return
            elapsed = datetime.now() - start
            m, s = divmod(int(elapsed.total_seconds()), 60)
            timer.config(text=f"{m:02d}:{s:02d}")
            self._timer_jobs[key] = self.frame.after(1000, tick)
        tick()

    def set_status_progress(self, file_path, page_idx, total_pages):
        key = self._normalize_key(file_path)
        if key not in self.file_widgets:
            raise KeyError(f"No widget found for: {file_path}")
        lbl, pb, pages, timer, icon = self.file_widgets[key]
        pb["maximum"] = total_pages
        pb["value"] = page_idx
        pages.config(text=f"{page_idx}/{total_pages} pages")

    def set_status_ocr_done(self, file_path):
        key = self._normalize_key(file_path)
        job = self._timer_jobs.pop(key, None)
        if job:
            self.frame.after_cancel(job)

    def set_status_done(self, file_path):
        key = self._normalize_key(file_path)
        lbl, pb, pages, timer, icon = self.file_widgets[key]
        pb["value"] = pb["maximum"]
        pages.config(text=f"{int(pb['maximum'])}/{int(pb['maximum'])} pages")
        job = self._timer_jobs.pop(key, None)
        if job:
            self.frame.after_cancel(job)
        icon.config(text="✔️")

    def set_status_error(self, file_path):
        key = self._normalize_key(file_path)
        job = self._timer_jobs.pop(key, None)
        if job:
            self.frame.after_cancel(job)
        _, _, _, _, icon = self.file_widgets[key]
        icon.config(text="❌")