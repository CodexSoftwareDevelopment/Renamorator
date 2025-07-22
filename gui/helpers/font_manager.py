# gui/helpers/font_manager.py
import os, ctypes
from tkinter import font as tkfont

FR_PRIVATE = 0x10
FONT_DIR   = os.path.join(os.path.dirname(__file__), "..", "fonts")

def register_and_load_fonts():
    # Register TTF/OTF privately for this process
    for fname in ("Blenda Script.otf", "Inter-VariableFont_opsz,wght.ttf"):
        ctypes.windll.gdi32.AddFontResourceExW(
            os.path.join(FONT_DIR, fname),
            FR_PRIVATE, 0
        )

    # Return Font objects
    return (
        tkfont.Font(family="Blenda Script", size=32),        # logo_font
        tkfont.Font(family="Inter",        size=16, weight="bold"),  # header_font
        tkfont.Font(family="Inter",        size=11)           # text_font
    )
