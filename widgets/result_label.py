"""
Click-to-Copy Result Label Widget
نمایشگر نتایج با قابلیت کپی سریع در کلیپ‌بورد و بازخورد بصری
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class ResultLabel(ctk.CTkLabel):
    def __init__(self, master, text="---", prefix="", **kwargs):
        """
        prefix: متنی که همیشه قبل از نتیجه نمایش داده می‌شود (مثلا "Hex: ")
        """
        self.prefix = prefix
        self.actual_value = text
        
        super().__init__(
            master,
            text=f"{self.prefix}{text}",
            font=config.UI_THEME["FONTS"]["CODE_EDITOR"],
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            cursor="hand2", # تغییر شکل موس به دست برای نشان دادن قابلیت کلیک
            **kwargs
        )
        
        # رویدادهای کلیک و هاور
        self.bind("<Button-1>", self._copy_to_clipboard)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

    def update_result(self, new_value):
        """به‌روزرسانی مقدار نمایش داده شده"""
        self.actual_value = str(new_value)
        self.configure(text=f"{self.prefix}{self.actual_value}", text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"])

    def _copy_to_clipboard(self, event=None):
        """کپی کردن مقدار واقعی در کلیپ‌بورد"""
        if not self.actual_value or self.actual_value == "---":
            return
            
        self.master.clipboard_clear()
        self.master.clipboard_append(self.actual_value)
        self.master.update()
        
        # بازخورد بصری موقت
        original_text = self.cget("text")
        self.configure(text="Copied to Clipboard!", text_color=config.UI_THEME["COLORS"]["SUCCESS"])
        self.after(1000, lambda: self.configure(text=original_text, text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"]))

    def _on_hover(self, event=None):
        """تغییر رنگ در هنگام عبور موس"""
        if self.actual_value != "---":
            self.configure(text_color=config.UI_THEME["COLORS"]["ACCENT"])

    def _on_leave(self, event=None):
        """بازگشت به رنگ اصلی"""
        self.configure(text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"])
