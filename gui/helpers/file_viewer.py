import os
from tkinter import ttk

# Helpers
from core.blend_name_volume_extractor import extract_title_blocks

def build_file_view(parent, idx, total, path, ocr_text):
    """
    Render the current file’s name and its title blocks.

    :param parent: Tkinter container to pack into.
    :param idx: 1-based index of the current file.
    :param total: total number of files.
    :param path: full path to the TIFF file.
    :param ocr_text: OCR’d text for this file.
    """
    basename = os.path.basename(path)
    # File counter label
    lbl = ttk.Label(
        parent,
        text=f"File {idx} of {total}: {basename}",
        style="Text.TLabel"
    )
    lbl.pack(anchor="w", pady=(0, 10))

    # Title blocks
    blocks = extract_title_blocks(ocr_text)
    blk_frame = ttk.LabelFrame(
        parent,
        text="Title Blocks",
        style="Background.TFrame"
    )
    blk_frame.pack(fill="x", pady=(0, 10))

    for i, block in enumerate(blocks, start=1):
        ttk.Label(
            blk_frame,
            text=f"{i}. {block}",
            style="Text.TLabel",
            wraplength=500,
            justify="left"
        ).pack(anchor="w", pady=2)
