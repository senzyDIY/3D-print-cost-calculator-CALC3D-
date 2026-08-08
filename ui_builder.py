import customtkinter as ctk

class UI:
    THEMES = {
        "dark": {
            "BG_DARK": "#121216",
            "CARD_BG": "#1A1A22",
            "BORDER_COLOR": "#2B2D42",
            "ACCENT": "#7B2CBF",
            "ACCENT_HOVER": "#9D4EDD",
            "CYAN": "#00F5D4",
            "TEXT_MAIN": "#F8F9FA",
            "TEXT_MUTED": "#8D99AE",
            "MODE": "Dark"
        },
        "light": {
            "BG_DARK": "#EAEAEA",
            "CARD_BG": "#FFFFFF",
            "BORDER_COLOR": "#D0D0D0",
            "ACCENT": "#5A189A",
            "ACCENT_HOVER": "#7B2CBF",
            "CYAN": "#009688",
            "TEXT_MAIN": "#212529",
            "TEXT_MUTED": "#6C757D",
            "MODE": "Light"
        },
        "ficsit": {
            "BG_DARK": "#262422",
            "CARD_BG": "#23221F",
            "BORDER_COLOR": "#2C3540",
            "ACCENT": "#FF9900", # Корпоративный оранжевый FICSIT
            "ACCENT_HOVER": "#FFB333",
            "CYAN": "#0ED4EE",
            "TEXT_MAIN": "#FFFFFF",
            "TEXT_MUTED": "#FF8C00",
            "MODE": "Dark"
        }
    }

    current_theme = "dark"

    @classmethod
    def get_colors(cls):
        return cls.THEMES[cls.current_theme]

    @classmethod
    def set_theme(cls, theme_name):
        if theme_name in cls.THEMES:
            cls.current_theme = theme_name
            ctk.set_appearance_mode(cls.THEMES[theme_name]["MODE"])

    @classmethod
    def setup(cls):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

    @classmethod
    def title(cls, parent, text, **kwargs):
        c = cls.get_colors()
        return ctk.CTkLabel(
            parent, text=text, 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), 
            text_color=c["TEXT_MAIN"], **kwargs
        )

    @classmethod
    def text(cls, parent, text, muted=False, font=None, text_color=None, **kwargs):
        c = cls.get_colors()
        if font is None:
            font = ctk.CTkFont(family="Segoe UI", size=13)
        
        if text_color is None:
            text_color = c["TEXT_MUTED"] if muted else c["TEXT_MAIN"]
            
        return ctk.CTkLabel(
            parent, text=text, font=font, text_color=text_color, **kwargs
        )

    @classmethod
    def card(cls, parent, **kwargs):
        c = cls.get_colors()
        return ctk.CTkFrame(
            parent, fg_color=c["CARD_BG"], corner_radius=14, 
            border_width=1, border_color=c["BORDER_COLOR"], **kwargs
        )

    @classmethod
    def button(cls, parent, text, command=None, accent=False, width=200, height=42, **kwargs):
        c = cls.get_colors()
        fg = c["ACCENT"] if accent else c["BORDER_COLOR"]
        hover = c["ACCENT_HOVER"] if accent else c["CARD_BG"]
        return ctk.CTkButton(
            parent, text=text, command=command, width=width, height=height,
            corner_radius=10, fg_color=fg, hover_color=hover, 
            text_color=c["TEXT_MAIN"], 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), **kwargs
        )

    @classmethod
    def entry(cls, parent, placeholder="", width=350, **kwargs):
        c = cls.get_colors()
        return ctk.CTkEntry(
            parent, placeholder_text=placeholder, width=width, height=40,
            corner_radius=8, fg_color=c["BG_DARK"], border_color=c["BORDER_COLOR"],
            border_width=1, text_color=c["TEXT_MAIN"], 
            placeholder_text_color=c["TEXT_MUTED"],
            font=ctk.CTkFont(family="Segoe UI", size=13), **kwargs
        )

    @classmethod
    def price(cls, parent, text, **kwargs):
        c = cls.get_colors()
        return ctk.CTkLabel(
            parent, text=text, 
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"), 
            text_color=c["CYAN"], **kwargs
        )