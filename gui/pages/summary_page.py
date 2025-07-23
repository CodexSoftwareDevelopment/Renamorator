import datetime, os
from tkinter import ttk

# Helpers
from gui.helpers.summary_computer import compute_summary
from gui.helpers.summary_text     import build_summary_text
from gui.helpers.lists            import build_lists
from gui.helpers.summary_buttons  import build_button_bar

def build_page(parent, controller):
    parent.configure(style="Background.TFrame")

    # Header
    header = ttk.Label(
        parent,
        text="Step 5 of 5: Summary & Finish",
        style="Header.TLabel"
    )
    header.pack(anchor="w", padx=20, pady=(20,10))

    # Compute summary
    mapping     = getattr(controller, "final_mapping", {})
    successes   = getattr(controller, "rename_successes", list(mapping.keys()))
    failures    = getattr(controller, "rename_failures", [])
    spreadsheet = getattr(controller, "spreadsheet", "")

    num_files, num_updates, unmatched = compute_summary(
        mapping,
        spreadsheet,
        rename_successes=successes
    )

    ts_sheet = datetime.datetime.now()
    controller.sheet_updated     = {}
    controller.sheet_not_updated = {}
    for old in mapping:
        stem = os.path.splitext(os.path.basename(old))[0]
        if stem in unmatched:
            controller.sheet_not_updated[old] = ts_sheet
        else:
            controller.sheet_updated[old]     = ts_sheet

    # Build summary text
    build_summary_text(parent,
                        num_files,
                        len(failures),
                        num_updates,
                        unmatched)


    # Build lists
    lists_container = ttk.Frame(parent, style="Background.TFrame")
    lists_container.pack(fill="both", expand=True, padx=20)
    build_lists(lists_container, mapping, unmatched)

    # Build buttons
    buttons_container = ttk.Frame(parent, style="Background.TFrame")
    buttons_container.pack(fill="x", padx=20, pady=20)
    build_button_bar(buttons_container, controller)
