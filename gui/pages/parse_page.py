import os
import tkinter as tk
from tkinter import ttk

from core.text_parser import parse_new_filename
from gui.helpers.file_viewer    import build_file_view
from gui.helpers.entry_fields   import build_entry_fields
from gui.helpers.frame_previewer import build_preview_frame

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # --- Header ---
    header = ttk.Label(
        parent,
        text="Step 4 of 5: Parse Blend & Volume",
        style="Header.TLabel"
    )
    header.grid(row=0, column=0, columnspan=2, sticky="w",
                padx=20, pady=(20,10))

    # --- Content frame for current file ---
    content = ttk.Frame(parent, style="Background.TFrame")
    content.grid(row=1, column=0, columnspan=2, sticky="nsew",
                 padx=20, pady=10)
    parent.rowconfigure(1, weight=1)
    parent.columnconfigure(0, weight=1)
    parent.columnconfigure(1, weight=1)

    # --- Preview frame for completed mappings ---
    preview = ttk.Frame(parent, style="Background.TFrame")
    preview.grid(row=2, column=0, columnspan=2, sticky="nsew",
                 padx=20, pady=(0,10))
    preview.columnconfigure(0, weight=1)

    # --- Navigation bar ---
    nav = ttk.Frame(parent, style="Background.TFrame")
    nav.grid(row=3, column=0, columnspan=2, sticky="ew",
             padx=20, pady=20)
    nav.columnconfigure(0, weight=1)
    nav.columnconfigure(1, weight=1)
    nav.columnconfigure(2, weight=1)

    back_btn = ttk.Button(nav, text="Back", style="Accent.TButton",
                          command=lambda: on_back())
    back_btn.grid(row=0, column=0, sticky="w")

    next_btn = ttk.Button(nav, text="Next", style="Accent.TButton",
                          command=lambda: on_next())
    next_btn.grid(row=0, column=2, sticky="e")

    # --- Initialize parse state ---
    if not hasattr(controller, "parse_index"):
        controller.parse_index   = 0
        controller.parse_mapping = {}  # old_path -> (blend, volume)

    def show_file():
        # clear previous widgets
        for w in content.winfo_children(): w.destroy()
        for w in preview.winfo_children(): w.destroy()

        idx   = controller.parse_index
        files = controller.tif_list
        total = len(files)
        path  = files[idx]
        text  = controller.ocr_results[path]

        # build file view (counter + title blocks)
        build_file_view(content, idx+1, total, path, text)

        # prefill existing values if revisiting
        existing = controller.parse_mapping.get(path, (None, None))
        blend_var, volume_var = build_entry_fields(content, row=2, existing=existing)

        # build preview of past mappings
        build_preview_frame(preview, {p: nm for p, (b, nm) in [
            (old, (b, parse_new_filename(controller.ocr_results[old], 
                (lambda blocks, _b=b, _v=v: (_b, _v)))))
            for old, (b, v) in controller.parse_mapping.items()
        ]}) if controller.parse_mapping else None
        if controller.parse_mapping:
            # simpler: preview only shows old->new strings
            # mapping: old_path -> new_filename via parse_new_filename
            mapping = {}
            for old, (b, v) in controller.parse_mapping.items():
                prompt_fn = lambda blocks, _b=b, _v=v: (_b, _v)
                mapping[old] = parse_new_filename(controller.ocr_results[old], prompt_fn)
            build_preview_frame(preview, mapping)

        # update Next button text
        next_btn.config(text="Finish" if idx == total-1 else "Next")

        # attach current inputs to nav
        nav.blend_var    = blend_var
        nav.volume_var   = volume_var
        nav.current_path = path

    def on_next():
        # save current blend & volume
        b = nav.blend_var.get().strip()
        v = nav.volume_var.get().strip()
        controller.parse_mapping[nav.current_path] = (b, v)

        if controller.parse_index < len(controller.tif_list) - 1:
            controller.parse_index += 1
            show_file()
        else:
            # build final mapping: old_path -> new_filename
            final = {}
            for old, (b, v) in controller.parse_mapping.items():
                prompt_fn = lambda blocks, _b=b, _v=v: (_b, _v)
                final[old] = parse_new_filename(controller.ocr_results[old], prompt_fn)
            controller.final_mapping = final
            controller.next()

    def on_back():
        # save current state, then go back or to previous page
        b = nav.blend_var.get().strip()
        v = nav.volume_var.get().strip()
        controller.parse_mapping[nav.current_path] = (b, v)
        if controller.parse_index > 0:
            controller.parse_index -= 1
            show_file()
        else:
            controller.back()

    # display the first (or resumed) file
    show_file()
