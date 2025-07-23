import tkinter as tk
from tkinter import ttk

def build_entry_fields(parent, row, existing=(None, None)):
    """
    Add blend & volume entry fields to `parent` at grid-row `row`.

    :param parent: Tkinter container using .grid layout.
    :param row: starting grid row for the blend label/entry.
    :param existing: tuple (blend, volume) to prefill.
    :returns: (blend_var, volume_var)
    """
    blend_val, volume_val = existing

    blend_var = tk.StringVar(value=blend_val or "")
    volume_var = tk.StringVar(value=volume_val or "")

    # Blend Name
    ttk.Label(
        parent,
        text="Blend Name:",
        style="Text.TLabel"
    ).pack(side="left", padx=(0,5), pady=(5,0))
    ttk.Entry(
        parent,
        textvariable=blend_var,
        width=40
    ).pack(side="left", padx=(0,5), pady=(5,0))

    # Volume
    ttk.Label(
        parent,
        text="Volume:",
        style="Text.TLabel"
    ).pack(side="left", padx=(0,5), pady=(5,0))
    ttk.Entry(
        parent,
        textvariable=volume_var,
        width=40
    ).pack(side="left", padx=(0,5), pady=(5,0))

    return blend_var, volume_var
