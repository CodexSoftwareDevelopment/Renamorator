import tkinter.font as tkfont
from tkinter import ttk


def build_page(parent, controller):
    """
    Construct the Start page with a compact layout:
      - Title and description at top
      - Buttons just below
      - Blank row at bottom absorbs extra space
    """
    controller.geometry("500x165")

    # Configure columns to center content, and a bottom row for spacing
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_rowconfigure(3, weight=1)  # spacer row

    # Title (bold, slightly larger)
    logo_font = tkfont.Font(size=18, weight="bold")
    logo = ttk.Label(parent, text="Namewise", font=logo_font)
    logo.grid(
        row=0, column=0, columnspan=2,
        pady=(10, 5), sticky="n"
    )

    # Description (wrapped, centered)
    desc = ttk.Label(
        parent,
        text=(
            "Namewise automates renaming of your TIFF files by extracting "
            "blend names and volumes via OCR, then updates your spreadsheet "
            "with the new filenames—all in one streamlined wizard!"
        ),
        wraplength=450,
        justify="center"
    )
    desc.grid(
        row=1, column=0, columnspan=2,
        padx=30, pady=(0, 10), sticky="n"
    )

    # Buttons container (compact)
    btn_frame = ttk.Frame(parent)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=(5, 10))

    close_btn = ttk.Button(
        btn_frame, text="Close", command=controller.destroy
    )
    close_btn.pack(side="left", padx=8)

    begin_btn = ttk.Button(
        btn_frame, text="Begin", command=controller.next
    )
    begin_btn.pack(side="left", padx=8)
