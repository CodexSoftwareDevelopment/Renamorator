import os
import tkinter as tk
from tkinter import ttk

# Helpers
from core.blend_name_volume_extractor import extract_title_blocks

def build_file_view(parent, idx, total, path, ocr_text):
    """
    Render the current file’s name and its title blocks in a scrollable,
    selectable Text widget so users can copy/paste.
    """
    basename = os.path.basename(path)

    # 1) File counter
    lbl = ttk.Label(
        parent,
        text=f"File {idx} of {total}: {basename}",
        style="Text.TLabel"
    )
    lbl.pack(anchor="w", pady=(0, 10))

    # 2) Pull out all the title‐block strings
    blocks = extract_title_blocks(ocr_text)

    # 3) Wrap them in a labelled frame
    blk_frame = ttk.LabelFrame(
        parent,
        text="Title Blocks",
        style="Background.TFrame"
    )
    blk_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # 4) Inside that frame, make a Text + Scrollbar
    text_widget = tk.Text(
        blk_frame,
        wrap="word",
        height=10,
        padx=5,
        pady=5,
        borderwidth=1,
        relief="solid"
    )
    vsb = ttk.Scrollbar(
        blk_frame, orient="vertical", command=text_widget.yview
    )
    text_widget.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)

    # 5) Dump in all the blocks (with numbering)
    for i, block in enumerate(blocks, start=1):
        text_widget.insert("end", f"{i}. {block}\n\n")

    # 6) Make read‐only but still allow selection
    text_widget.configure(state="disabled")
