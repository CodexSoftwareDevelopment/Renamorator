import tkinter as tk
from tkinter import ttk, messagebox

# Helpers
from gui.helpers.validations import validate_blend_name, validate_volume

def build_entry_fields(parent, row=2, existing=None):
    """
    Creates a small sub-frame inside `parent`, packs it,
    then grids two rows of Blend/Volume widgets into it.
    Returns (blend_var, volume_var).
    """
    # 1) Make a little container frame and pack it
    container = tk.Frame(parent)
    container.pack(fill="x", padx=(10, 0), pady=(5, 5))

    # 2) Prepare the StringVars with any pre-existing values
    existing = existing or {}
    blend_var = tk.StringVar(value=existing.get("blend", ""))
    volume_var = tk.StringVar(value=existing.get("volume", ""))

    # Keep a “last good” copy so we can revert on invalid input
    last = {"blend": blend_var.get(), "volume": volume_var.get()}

    def on_blend_change(*_):
        v = blend_var.get()
        if not validate_blend_name(v):
            messagebox.showwarning(
                "Invalid Blend Name",
                'Blend name can’t contain any of: < > : / \\ | ? * "'
            )
            blend_var.set(last["blend"])
        else:
            last["blend"] = v

    def on_volume_change(*_):
        v = volume_var.get()
        if not validate_volume(v):
            messagebox.showwarning(
                "Invalid Volume",
                'Volume must be empty or like "2 oz" / "50gal".'
            )
            volume_var.set(last["volume"])
        else:
            last["volume"] = v

    blend_var.trace_add("write", on_blend_change)
    volume_var.trace_add("write", on_volume_change)

    # 3) Grid the labels + entries INTO the container
    ttk.Label(container, text="Blend Name:", style="Text.TLabel") \
        .grid(row=0, column=0, sticky="w", padx=(0,5), pady=(5,0))
    ttk.Entry(container, textvariable=blend_var, width=59) \
        .grid(row=0, column=1, sticky="w", pady=(5,0))

    ttk.Label(container, text="Volume:", style="Text.TLabel") \
        .grid(row=1, column=0, sticky="w", padx=(0,5), pady=(5,0))
    ttk.Entry(container, textvariable=volume_var, width=59) \
        .grid(row=1, column=1, sticky="w", pady=(5,0))

    return blend_var, volume_var
