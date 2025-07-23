import os
from tkinter import ttk

def build_lists(parent, mapping: dict, unmatched: list):
    """
    Splits mappings into updated vs. unmatched and displays two lists side by side.
    """
    # Container frames
    updated_frame = ttk.LabelFrame(
        parent,
        text="✅ Spreadsheet Updated",
        style="Background.TFrame"
    )
    updated_frame.pack(
        side="left", fill="both", expand=True,
        padx=(0,10), pady=10
    )

    for old, new in mapping.items():
        stem = os.path.splitext(os.path.basename(old))[0]
        if stem not in unmatched:
            ttk.Label(
                updated_frame,
                text=f"{os.path.basename(old)} → {os.path.basename(new)}",
                style="Text.TLabel"
            ).pack(anchor="w", pady=2)

    unmatched_frame = ttk.LabelFrame(
        parent,
        text="⚠️ Unmatched Files",
        style="Background.TFrame"
    )
    unmatched_frame.pack(
        side="right", fill="both", expand=True,
        padx=(10,0), pady=10
    )

    for stem in unmatched:
        # unmatched list contains stems (or paths) as returned by compute_summary
        # if they’re full paths, basename() will trim them
        label_text = os.path.basename(stem) if os.path.isabs(stem) else stem
        ttk.Label(
            unmatched_frame,
            text=label_text,
            style="Text.TLabel"
        ).pack(anchor="w", pady=2)
