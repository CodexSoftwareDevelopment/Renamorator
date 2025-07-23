import os
import tkinter as tk
from tkinter import ttk

# Helpers
from gui.helpers.font_manager import register_and_load_fonts
from gui.helpers.style_manager import apply_theme
from gui.wizard_config import PAGE_ORDER, PAGE_BUILDERS

# Color constants
BG_COLOR      = "#F5F5F5"  # off‑white background
PRIMARY_COLOR = "#8FAED0"  # slate‑blue accent
TEXT_COLOR    = "#333333"  # dark charcoal text

class Wizard(tk.Tk):
    """
    A paged wizard application for Namewise (formerly Renamorator).
    """
    def __init__(self):
        super().__init__()
        self.title("Namewise")
        self.configure(bg=BG_COLOR)

        # Load/register bundled fonts and apply our theme
        self.logo_font, self.header_font, self.text_font = register_and_load_fonts()
        style = ttk.Style(self)
        apply_theme(
            style,
            bg=BG_COLOR,
            primary=PRIMARY_COLOR,
            text=TEXT_COLOR,
            logo_font=self.logo_font,
            header_font=self.header_font,
            text_font=self.text_font
        )

        # Container for all pages
        container = ttk.Frame(self, style="Background.TFrame")
        container.pack(fill="both", expand=True)

        # Prepare each page but defer building
        self.pages    = {}
        self.builders = {}
        self.built    = {}
        for name in PAGE_ORDER:
            module_path, fn_name = PAGE_BUILDERS[name].split(":")
            mod = __import__(module_path, fromlist=[fn_name])
            builder = getattr(mod, fn_name)

            frame = ttk.Frame(container, style="Background.TFrame")
            self.pages[name]    = frame
            self.builders[name] = builder
            self.built[name]    = False

        # No current page yet; show the first page
        self.current = None
        self.show(PAGE_ORDER[0])

    def show(self, page_name: str):
        """Hide the current page, build if needed, and display the named one."""
        # Hide previous
        if self.current:
            self.pages[self.current].pack_forget()

        # Build on first display
        if not self.built.get(page_name, False):
            self.builders[page_name](
                self.pages[page_name],
                controller=self
            )
            self.built[page_name] = True

        # Show it
        frame = self.pages[page_name]
        frame.pack(fill="both", expand=True)
        self.current = page_name

    def next(self):
        """Advance to the next page in the wizard."""
        order = PAGE_ORDER
        idx = order.index(self.current)
        if idx < len(order) - 1:
            self.show(order[idx + 1])

    def back(self):
        """Return to the previous page in the wizard."""
        order = PAGE_ORDER
        idx = order.index(self.current)
        if idx > 0:
            self.show(order[idx - 1])

def run():
    app = Wizard()
    app.mainloop()
