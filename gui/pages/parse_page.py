import os
import datetime
from tkinter import ttk, messagebox

from core.text_parser import parse_new_filename
from gui.helpers.file_viewer     import build_file_view
from gui.helpers.entry_fields    import build_entry_fields
from gui.helpers.frame_previewer import build_preview_frame
from gui.helpers.validations     import validate_blend_name, validate_volume

def build_page(parent, controller):
    controller.geometry("1400x700")

    # --- Layout Grid ---
    parent.grid_columnconfigure(0, weight=3, minsize=900)
    parent.grid_columnconfigure(1, weight=2, minsize=350)
    for i in range(5):  # allow for more flexible rows
        parent.grid_rowconfigure(i, weight=0)
    parent.grid_rowconfigure(1, weight=1)

    # --- Header (Centered) ---
    header = ttk.Label(parent, text="Step 4 of 5: Parse Blend & Volume", anchor="center", font=("Segoe UI", 14, "bold"))
    header.grid(row=0, column=0, columnspan=2, pady=(20,10), sticky="ew")

    # --- LEFT: Old/New Filename Mapping ---
    left_frame = ttk.Frame(parent, style="Background.TFrame")
    left_frame.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=(20,10), pady=(0,10))

    map_list = ttk.Treeview(
        left_frame,
        columns=("old", "new"),
        show="headings",
        height=20
    )

    map_list.heading("old", text="Old Filename", anchor="center")
    map_list.heading("new", text="New Filename", anchor="center")

    map_list.column("old", anchor="w", stretch=True)
    map_list.column("new", anchor="w", stretch=True)

    vsb = ttk.Scrollbar(left_frame, orient="vertical", command=map_list.yview)
    map_list.configure(yscrollcommand=vsb.set)

    map_list.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # --- RIGHT: Content Frame ---
    content = ttk.Frame(parent, style="Background.TFrame")
    content.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=(0,5))
    content.grid_columnconfigure(0, weight=1)

    # --- Preview Frame (below content) ---
    preview = ttk.Frame(parent, style="Background.TFrame")
    preview.grid(row=2, column=1, sticky="nsew", padx=(0, 20), pady=(0,5))
    preview.grid_columnconfigure(0, weight=1)

    # --- Entry Fields (now below preview) ---
    entry_fields = ttk.Frame(parent, style="Background.TFrame")
    entry_fields.grid(row=3, column=1, sticky="ew", padx=(0, 20), pady=(0,10))
    entry_fields.grid_columnconfigure(1, weight=1)

    # --- Navigation Buttons ---
    nav = ttk.Frame(parent, style="Background.TFrame")
    nav.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
    nav.grid_columnconfigure(0, weight=1)
    nav.grid_columnconfigure(2, weight=1)

    back_btn = ttk.Button(nav, text="Back", command=lambda: on_back())
    back_btn.grid(row=0, column=0, sticky="w")
    next_btn = ttk.Button(nav, text="Next", style="Accent.TButton", command=lambda: on_next())
    next_btn.grid(row=0, column=2, sticky="e")

    # --- Controller Init ---
    if not hasattr(controller, "parse_index"):
        controller.parse_index = 0
        controller.parse_mapping = {}

    def refresh_map_list():
        map_list.delete(*map_list.get_children())
        for old_path, (b_val, v_val) in controller.parse_mapping.items():
            new_name = parse_new_filename(
                controller.ocr_results[old_path],
                lambda blocks, blend=b_val, volume=v_val: (blend, volume)
            )
            disp_new = new_name.replace("\n", " ")
            map_list.insert("", "end", values=(os.path.basename(old_path), disp_new))

    def show_file():
        refresh_map_list()

        for w in content.winfo_children(): w.destroy()
        for w in preview.winfo_children(): w.destroy()
        for w in entry_fields.winfo_children(): w.destroy()

        idx = controller.parse_index
        files = controller.tif_list
        path = files[idx]
        text = controller.ocr_results[path]

        build_file_view(content, idx+1, len(files), path, text)

        b_exist, v_exist = controller.parse_mapping.get(path, ("", ""))
        blend_var, volume_var = build_entry_fields(entry_fields, existing={"blend": b_exist, "volume": v_exist})

        nav.blend_var = blend_var
        nav.volume_var = volume_var
        nav.current_path = path

        if controller.parse_mapping:
            summary = {
                old: parse_new_filename(
                    controller.ocr_results[old],
                    lambda blocks, blend=b, volume=v: (blend, volume)
                )
                for old, (b, v) in controller.parse_mapping.items()
            }
            build_preview_frame(preview, summary)

    def on_next():
        blend = nav.blend_var.get().strip()
        volume = nav.volume_var.get().strip()

        if not validate_blend_name(blend):
            messagebox.showerror("Invalid Blend Name", "No ‘|’ or ‘;’ allowed.")
            return
        if not validate_volume(volume):
            messagebox.showerror("Invalid Volume", "Must be empty or like ‘2 oz’.")
            return

        controller.parse_mapping[nav.current_path] = (blend, volume)

        if controller.parse_index < len(controller.tif_list) - 1:
            controller.parse_index += 1
            show_file()
        else:
            final = {
                old: parse_new_filename(
                    controller.ocr_results[old],
                    lambda blocks, blend=b_val, volume=v_val: (blend, volume)
                )
                for old, (b_val, v_val) in controller.parse_mapping.items()
            }
            controller.final_mapping = final

            from core.file_renamer import run_rename_pipeline
            successes, failures = run_rename_pipeline(final, log_function=lambda m: print(m))
            controller.rename_successes = successes
            controller.rename_failures = failures
            controller.rename_timestamps = {old: datetime.datetime.now() for old in successes}
            controller.next()

    def on_back():
        blend = nav.blend_var.get().strip()
        volume = nav.volume_var.get().strip()
        controller.parse_mapping[nav.current_path] = (blend, volume)
        if controller.parse_index > 0:
            controller.parse_index -= 1
            show_file()
        else:
            controller.back()

    show_file()