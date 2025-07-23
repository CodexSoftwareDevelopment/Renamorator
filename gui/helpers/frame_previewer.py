import os
from tkinter import ttk

def build_preview_frame(parent, mapping):
    """
    Populate `parent` with a list of past old→new filename mappings.

    :param parent: Tkinter container using .grid layout.
    :param mapping: dict of {old_path: new_filename}.
    """
    # Header row
    ttk.Label(
        parent,
        text="Old Filename → New Filename",
        style="Text.TLabel"
    ).grid(row=0, column=0, sticky="w", pady=(0,5))

    # Each mapping
    for r, (old, new) in enumerate(mapping.items(), start=1):
        old_name = os.path.basename(old)
        ttk.Label(
            parent,
            text=f"{old_name} → {new}",
            style="Text.TLabel"
        ).grid(row=r, column=0, sticky="w", pady=2)
