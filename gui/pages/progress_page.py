import threading
from tkinter import ttk
from tkinter.font import Font as tkfont

# Helpers
from core.file_collector  import collect_tif_files
from core.ocr_pipeline    import run_ocr_pipeline
from gui.helpers.progress import OCRProgressUI

def build_page(parent, controller):
    controller.geometry("900x700")
    controller.minsize(500, 200)

    # — Header —
    header_font = tkfont(size=14, weight="bold")

    header = ttk.Label(
        parent,
        text="Step 2 of 5: OCRing TIF files",
        font=header_font
    )
    header.pack(anchor="w", padx=20, pady=(20,10))

    # — Progress UI —
    progress_ui = OCRProgressUI(parent)
    progress_ui.pack(fill="both", expand=True, padx=20, pady=10)

    # — Navigation buttons container —
    nav = ttk.Frame(parent, style="Background.TFrame")
    nav.pack(fill="x", padx=20, pady=(0,20))

    back_btn = ttk.Button(
        nav, text="Back",
        style="Accent.TButton",
        command=controller.back
    )
    back_btn.pack(side="left")

    next_btn = ttk.Button(
        nav, text="Next",
        style="Accent.TButton",
        command=controller.next
    )
    next_btn.pack(side="right")
    next_btn["state"] = "disabled"

    tif_list = collect_tif_files(controller.tif_folder)
    progress_ui.initialize_files(tif_list)
    controller.tif_list = tif_list

    def worker():

        # 2) run the OCR pipeline with UI callbacks
        texts = run_ocr_pipeline(
            tif_list,
            status_fn={
                "processing": lambda p: parent.after(0, progress_ui.set_status_processing, p),
                "progress":   lambda p,i,n: parent.after(0, progress_ui.set_status_progress, p, i, n),
                "ocr_done":   lambda p: parent.after(0, progress_ui.set_status_ocr_done, p),
                "error":      lambda p: parent.after(0, progress_ui.set_status_error, p),
            },
            progress_fn=lambda count, total, fname: parent.after(
                0, progress_ui.update_overall_progress, count, total, fname
            ),
            log_function=lambda msg: None  # or hook into a log console if desired
        )
        controller.ocr_results = texts

        # 3) enable Next button once OCR is finished
        parent.after(0, lambda: next_btn.config(state="normal"))

    # 4) start in background so UI stays responsive
    threading.Thread(target=worker, daemon=True).start()
