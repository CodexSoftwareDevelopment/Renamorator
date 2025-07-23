def apply_theme(style, bg, primary, text, logo_font, header_font, text_font):
    style.theme_use("default")
    style.configure("Background.TFrame", background=bg)
    style.configure("Logo.TLabel",   background=bg, foreground=primary, font=logo_font)
    style.configure("Header.TLabel", background=bg, foreground=text,    font=header_font)
    style.configure("Text.TLabel",   background=bg, foreground=text,    font=text_font)
    style.configure("Accent.TButton",
                    background=primary, foreground=text, font=header_font)
    style.map("Accent.TButton",
              background=[('active', primary)],
              foreground=[('active', text)])
