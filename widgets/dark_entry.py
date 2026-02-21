"""
Smart Dark Entry Widget with Validation
ویجت ورودی متن پیشرفته با قابلیت اعتبارسنجی آنی و استایل تاریک
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ولیدیتورها
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.validators import validator

class DarkEntry(ctk.CTkEntry):
    def __init__(self, master, placeholder="", validate_type=None, **kwargs):
        """
        validate_type: می تواند 'hex', 'bin', 'float', 'int' یا None باشد
        """
        super().__init__(
            master,
            placeholder_text=placeholder,
            fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"],
            border_color=config.UI_THEME["COLORS"]["BG_SIDEBAR"],
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            placeholder_text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"],
            **kwargs
        )
        
        self.validate_type = validate_type
        # اتصال رویداد تایپ کردن به تابع اعتبارسنجی
        self.bind("<KeyRelease>", self._check_validation)

    def _check_validation(self, event=None):
        """بررسی صحت ورودی در هر بار تایپ کردن"""
        if not self.validate_type:
            return

        current_text = self.get().strip()
        if not current_text:
            self.configure(border_color=config.UI_THEME["COLORS"]["BG_SIDEBAR"])
            return

        is_valid = True
        if self.validate_type == "hex":
            is_valid = validator.is_valid_hex(current_text)
        elif self.validate_type == "bin":
            is_valid = validator.is_valid_binary(current_text)
        elif self.validate_type == "float":
            is_valid = validator.is_valid_float(current_text)
        
        # تغییر رنگ حاشیه بر اساس وضعیت اعتبار
        if is_valid:
            self.configure(border_color=config.UI_THEME["COLORS"]["SUCCESS"])
        else:
            self.configure(border_color=config.UI_THEME["COLORS"]["ERROR"])

    def get_value(self):
        """دریافت مقدار ورودی (پاکسازی شده)"""
        return self.get().strip()
