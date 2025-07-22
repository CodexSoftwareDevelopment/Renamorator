from tkinter import ttk

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # Make 2 equal columns for button alignment
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    # Push buttons to bottom
    parent.grid_rowconfigure(2, weight=1)

    # Logo (big, centered at top)
    logo = ttk.Label(
        parent,
        text="Namewise",
        style="Logo.TLabel"
    )
    logo.grid(
        row=0, column=0, columnspan=2,
        pady=(40, 10),
        sticky="n"
    )

    # Description
    desc = ttk.Label(
        parent,
        text=(
            "Namewise automates renaming of your TIFF files by extracting "
            "blend names and volumes via OCR, then updates your spreadsheet "
            "with the new filenames—all in one streamlined wizard!"
        ),
        style="Text.TLabel",
        wraplength=600,
        justify="center"
    )
    desc.grid(
        row=1, column=0, columnspan=2,
        padx=100, pady=(0, 40),
        sticky="n"
    )

    # Close button (bottom‑left)
    close_btn = ttk.Button(
        parent,
        text="Close",
        style="Accent.TButton",
        command=controller.destroy
    )
    close_btn.grid(
        row=2, column=0,
        padx=20, pady=20,
        sticky="w"
    )

    # Begin button (bottom‑right)
    begin_btn = ttk.Button(
        parent,
        text="Begin",
        style="Accent.TButton",
        command=controller.next
    )
    begin_btn.grid(
        row=2, column=1,
        padx=20, pady=20,
        sticky="e"
    )
