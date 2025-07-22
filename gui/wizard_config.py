# gui/wizard_config.py
PAGE_ORDER = [
    "folder_page",
    "progress_page",
    "parse_page",
    "summary_page",
]

PAGE_BUILDERS = {
    "folder_page":   "gui.pages.folder_page:build_page",
    "progress_page": "gui.pages.progress_page:build_page",
    "parse_page":    "gui.pages.parse_page:build_page",
    "summary_page":  "gui.pages.summary_page:build_page",
}
