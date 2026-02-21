"""
Custom HDL Copy Button Widget
ویجت اختصاصی برای کپی کردن نتایج به صورت کد VHDL/Verilog یا متن ساده
"""

import customtkinter as ctk
import sys
import os
from tkinter import messagebox

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و هسته اصلی
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.hdl_snippet_generator import snippet_generator

class HDLCopyButton(ctk.CTkButton):
    def __init__(self, master, get_data_func, data_type="constant", **kwargs):
        """
        master: پنجره یا فریم والد
        get_data_func: تابعی که دیتای فعلی را برای کپی کردن برمی‌گرداند
        data_type: نوع دیتا (constant, rgb, fixed_point, etc.)
        """
        # تنظیمات ظاهری از فایل config
        accent_color = config.UI_THEME["COLORS"]["ACCENT"]
        hover_color = config.UI_THEME["COLORS"]["ACCENT_HOVER"]
        
        super().__init__(
            master, 
            text="Copy as HDL", 
            fg_color=accent_color,
            hover_color=hover_color,
            width=120,
            command=self._copy_action,
            **kwargs
        )
        
        self.get_data_func = get_data_func
        self.data_type = data_type

    def _copy_action(self):
        """عملیات اصلی کپی کردن در کلیپ‌بورد"""
        try:
            # دریافت داده از ویجت یا تابع مربوطه
            raw_data = self.get_data_func()
            
            if not raw_data:
                return

            # تولید کد بر اساس نوع داده تعریف شده
            hdl_code = ""
            if self.data_type == "constant":
                hdl_code = snippet_generator.generate_constant(
                    name="DATA_OUT", 
                    value=raw_data["value"], 
                    bit_width=raw_data.get("width")
                )
            elif self.data_type == "fixed_point":
                hdl_code = snippet_generator.generate_fixed_point_coeff(
                    name="COEFF",
                    hex_value=raw_data["hex"],
                    bit_width=raw_data["width"]
                )
            elif self.data_type == "rgb":
                hdl_code = snippet_generator.generate_rgb_color(
                    name="COLOR_CONST",
                    hex_color=raw_data["hex"]
                )
            
            # کپی در کلیپ‌بورد سیستم
            self.master.clipboard_clear()
            self.master.clipboard_append(hdl_code)
            self.master.update() # کلیپ‌بورد را در سیستم ثبت می‌کند
            
            # تغییر موقت متن دکمه برای بازخورد به کاربر
            old_text = self.cget("text")
            self.configure(text="✅ Copied!", fg_color=config.UI_THEME["COLORS"]["SUCCESS"])
            self.after(1500, lambda: self.configure(text=old_text, fg_color=config.UI_THEME["COLORS"]["ACCENT"]))
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not generate HDL snippet: {str(e)}")

    def update_type(self, new_type):
        """تغییر نوع داده در زمان اجرا (مثلاً تغییر از حالت ثابت به ممیز ثابت)"""
        self.data_type = new_type
