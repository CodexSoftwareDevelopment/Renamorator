import tkinter as tk
from tkinter import ttk

# Helpers
from gui.wizard_config import PAGE_ORDER, PAGE_BUILDERS

class Wizard(tk.Tk):
    """
    A paged wizard application for Namewise (formerly Renamorator).
    """
    def __init__(self):
        super().__init__()
        self.title("Namewise")

        # Container for all pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Prepare each page but defer building
        self.pages    = {}
        self.builders = {}
        self.built    = {}
        for name in PAGE_ORDER:
            module_path, fn_name = PAGE_BUILDERS[name].split(":")
            mod = __import__(module_path, fromlist=[fn_name])
            builder = getattr(mod, fn_name)

            frame = ttk.Frame(container)
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
