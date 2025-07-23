from tkinter import ttk

# Helpers
from gui.helpers.folder_selector import build_folder_selector
from gui.helpers.spreadsheet_selector import build_spreadsheet_selector
from gui.helpers.validations import validate_folder, validate_spreadsheet

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # Logo & Step Indicator (Row 0)
    ttk.Label(parent, text="Namewise", style="Logo.TLabel")\
       .grid(row=0, column=0, sticky="w", padx=20, pady=(20,5))
    ttk.Label(parent, text="Step 1 of 5", style="Text.TLabel")\
       .grid(row=0, column=1, sticky="e", padx=20, pady=(20,5))

    # Folder selector → returns folder_var
    folder_var = build_folder_selector(parent)

    # Spreadsheet selector → returns spreadsheet_var, same_var
    spreadsheet_var, same_var = build_spreadsheet_selector(parent, controller)

    # Spacer
    parent.grid_rowconfigure(6, weight=1)

    # Back button
    ttk.Button(parent, text="Back", style="Accent.TButton",
               command=controller.back)\
       .grid(row=7, column=0, sticky="w", padx=20, pady=20)

    # Process button: start disabled
    process_btn = ttk.Button(
        parent,
        text="Process",
        style="Accent.TButton",
        state="disabled",
        command=lambda: _on_process(controller, folder_var, spreadsheet_var, same_var)
    )
    process_btn.grid(row=7, column=1, sticky="e", padx=20, pady=20)

    # Enable Process only when folder and spreadsheet are valid
    def update_process_state(*_):
        f_ok = validate_folder(folder_var.get().strip())

        if same_var.get():
            ss_path = getattr(controller, "last_spreadsheet", "")
            ss_ok = bool(ss_path) and validate_spreadsheet(ss_path)
        else:
            ss_ok = validate_spreadsheet(spreadsheet_var.get().strip())

        process_btn.config(state="normal" if (f_ok and ss_ok) else "disabled")

    # watch all three vars
    folder_var.trace_add("write", update_process_state)
    spreadsheet_var.trace_add("write", update_process_state)
    same_var.trace_add("write", update_process_state)

    # **INITIAL STATE** – make sure the button reflects any pre‑filled values
    update_process_state()

    # Column weights
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=0)


def _on_process(controller, folder_var, spreadsheet_var, same_var):
    controller.tif_folder = folder_var.get().strip()
    if same_var.get() and getattr(controller, "last_spreadsheet", ""):
        controller.spreadsheet = controller.last_spreadsheet
    else:
        controller.spreadsheet = spreadsheet_var.get().strip()
    controller.last_spreadsheet = controller.spreadsheet
    controller.next()
