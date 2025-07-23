import tkinter as tk
from tkinter import ttk, messagebox

# Helpers
from gui.helpers.validations import validate_blend_name, validate_volume

def build_entry_fields(parent, row, existing=(None, None)):
    blend_val, volume_val = existing
    blend_var = tk.StringVar(value=blend_val or "")
    volume_var = tk.StringVar(value=volume_val or "")

    # keep last-good so we can revert on bad input
    last = {"blend": blend_var.get(), "volume": volume_var.get()}

    def on_blend_change(*_):
        v = blend_var.get()
        if not validate_blend_name(v):
            messagebox.showwarning(
                "Invalid Blend Name",
                "Blend name can’t contain the following: < > : / \ | ? * \" "
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

    # ——— build the UI ———
    ttk.Label(parent, text="Blend Name:", style="Text.TLabel")\
       .grid(row=row, column=0, sticky="w", padx=(0,5), pady=(5,0))
    ttk.Entry(parent, textvariable=blend_var, width=40)\
       .grid(row=row, column=1, sticky="w", pady=(5,0))

    ttk.Label(parent, text="Volume:", style="Text.TLabel")\
       .grid(row=row+1, column=0, sticky="w", padx=(0,5), pady=(5,0))
    ttk.Entry(parent, textvariable=volume_var, width=40)\
       .grid(row=row+1, column=1, sticky="w", pady=(5,0))

    return blend_var, volume_var
