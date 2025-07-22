import os
import tkinter as tk
from tkinter import ttk

# Helpers
from core.blend_name_volume_extractor import extract_title_blocks

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # File counter / header
    header = ttk.Label(
        parent,
        text=f"Step 4 of 5: Parse Blend & Volume",
        style="Header.TLabel"
    )
    header.grid(row=0, column=0, columnspan=2, sticky="w",
                padx=20, pady=(20,10))

    # Frame for per-file content
    content = ttk.Frame(parent, style="Background.TFrame")
    content.grid(row=1, column=0, columnspan=2, sticky="nsew",
                 padx=20, pady=10)
    parent.grid_rowconfigure(1, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)

    # Preview of completed mappings so far
    preview = ttk.LabelFrame(parent, text="Completed so far", style="Background.TFrame")
    preview.grid(row=2, column=0, columnspan=2, sticky="nsew",
                 padx=20, pady=(0,10))
    preview.columnconfigure(0, weight=1)

    # Navigation buttons
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

    # State stored on controller
    if not hasattr(controller, "parse_index"):
        controller.parse_index     = 0
        controller.parse_mapping   = {}  # old_path -> new_filename

    def show_file():
        # Clear content & preview
        for w in content.winfo_children(): w.destroy()
        for w in preview.winfo_children(): w.destroy()

        idx  = controller.parse_index
        files = controller.tif_list
        total = len(files)
        path = files[idx]
        base = os.path.basename(path)

        # File label
        ttk.Label(content,
                  text=f"File {idx+1} of {total}: {base}",
                  style="Text.TLabel")\
          .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,10))

        # Title blocks display
        blocks = extract_title_blocks(controller.ocr_results[path])
        blk_frame = ttk.LabelFrame(content, text="Title Blocks", style="Background.TFrame")
        blk_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0,10))
        for i, b in enumerate(blocks, start=1):
            ttk.Label(blk_frame, text=f"{i}. {b}", style="Text.TLabel")\
               .pack(anchor="w")

        # Blend & Volume entries
        blend_var  = tk.StringVar()
        volume_var = tk.StringVar()
        # prefill if revisiting
        old_map = controller.parse_mapping.get(path)
        if old_map:
            blend_var.set(old_map[0])
            volume_var.set(old_map[1])

        ttk.Label(content, text="Blend Name:", style="Text.TLabel")\
           .grid(row=2, column=0, sticky="e", padx=(0,5))
        ttk.Entry(content, textvariable=blend_var, width=40)\
           .grid(row=2, column=1, sticky="w")

        ttk.Label(content, text="Volume:", style="Text.TLabel")\
           .grid(row=3, column=0, sticky="e", padx=(0,5), pady=(5,0))
        ttk.Entry(content, textvariable=volume_var, width=40)\
           .grid(row=3, column=1, sticky="w", pady=(5,0))

        # Populate preview of already‐done files
        ttk.Label(preview, text="Old Filename → New Filename", style="Text.TLabel")\
           .grid(row=0, column=0, sticky="w", pady=(0,5))
        for r, (old, new) in enumerate(controller.parse_mapping.items(), start=1):
            old_name = os.path.basename(old)
            ttk.Label(preview,
                      text=f"{old_name} → {new}",
                      style="Text.TLabel")\
               .grid(row=r, column=0, sticky="w")

        # Update buttons’ labels
        next_btn.config(text="Finish" if idx == total-1 else "Next")

        # Inner callbacks capture these vars
        nav.blend_var  = blend_var
        nav.volume_var = volume_var
        nav.current_path = path

    def on_next():
        # save entries
        blend  = nav.blend_var.get().strip()
        volume = nav.volume_var.get().strip()
        controller.parse_mapping[nav.current_path] = (blend, volume)

        # advance or finish
        if controller.parse_index < len(controller.tif_list)-1:
            controller.parse_index += 1
            show_file()
        else:
            # build final mapping: old_path→new_filename via parse_new_filename
            from core.text_parser import parse_new_filename
            final_map = {}
            for old, (b,v) in controller.parse_mapping.items():
                # reuse your doc‐numbers + equipment‐code logic
                txt = controller.ocr_results[old]
                # monkey‐patch prompt to return our (b,v)
                prompt_fn = lambda blocks, _b=b, _v=v: (_b, _v)
                new_name = parse_new_filename(txt, prompt_fn)
                final_map[old] = new_name
            controller.final_mapping = final_map
            controller.next()

    def on_back():
        if controller.parse_index > 0:
            # save current
            blend  = nav.blend_var.get().strip()
            volume = nav.volume_var.get().strip()
            controller.parse_mapping[nav.current_path] = (blend, volume)
            controller.parse_index -= 1
            show_file()
        else:
            controller.back()

    # kick it off
    show_file()
