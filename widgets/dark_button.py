"""
Custom Dark Button Widget
"""
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class DarkButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, is_accent=True, **kwargs):
        
        # انتخاب رنگ دکمه (دکمه‌های اصلی آبی، دکمه‌های فرعی خاکستری تاریک)
        if is_accent:
            fg_color = config.UI_THEME["COLORS"]["ACCENT"]
            hover_color = config.UI_THEME["COLORS"]["ACCENT_HOVER"]
        else:
            fg_color = config.UI_THEME["COLORS"]["BG_SIDEBAR"]
            hover_color = config.UI_THEME["COLORS"]["TEXT_SECONDARY"]

        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            font=config.UI_THEME["FONTS"]["GUI_BASE"],
            corner_radius=6,
            **kwargs
        )
