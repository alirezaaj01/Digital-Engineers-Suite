"""
Professional Window Functions Toolbox
ابزار تحلیل و تولید توابع پنجره (Hamming, Hann, Blackman, ...) برای پردازش سیگنال
"""

import customtkinter as ctk
import numpy as np
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و موتورها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from engines.plot_engine import plot_engine
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class WindowFunctions(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- پارامترهای پنجره ---
        # طول پنجره (Window Length)
        ctk.CTkLabel(self, text="Window Length (L):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.length_entry = DarkEntry(self, placeholder="e.g. 64", validate_type="int")
        self.length_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.length_entry.insert(0, "64")

        # انتخاب نوع پنجره
        ctk.CTkLabel(self, text="Select Window:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.win_var = ctk.StringVar(value="Hamming")
        self.win_menu = ctk.CTkOptionMenu(
            self, values=["Hamming", "Hanning", "Blackman", "Bartlett", "Kaiser"],
            variable=self.win_var,
            fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"],
            button_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.win_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # دکمه تحلیل و رسم
        self.analyze_btn = ctk.CTkButton(
            self, text="Generate & Analyze", command=self._analyze_window,
            fg_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.analyze_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # نمایش پارامترهای تحلیلی (مثل عرض Main-lobe)
        self.info_res = ResultLabel(self, text="---", prefix="Main-lobe Width: ")
        self.info_res.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # دکمه کپی ضرایب برای استفاده در VHDL/Verilog
        self.copy_btn = HDLCopyButton(self, self._get_window_coeffs, data_type="constant", text="Copy Window Coeffs")
        self.copy_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # فضای نمایش نمودار
        self.plot_placeholder = ctk.CTkLabel(self, text="[Plot Area: Time & Frequency Domain]", 
                                            text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"])
        self.plot_placeholder.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

    def _analyze_window(self):
        """تولید پنجره و تحلیل مشخصات آن"""
        try:
            L = int(self.length_entry.get())
            win_type = self.win_var.get().lower()

            # تولید پنجره بر اساس نوع
            if win_type == "hamming": self.win_data = np.hamming(L)
            elif win_type == "hanning": self.win_data = np.hanning(L)
            elif win_type == "blackman": self.win_data = np.blackman(L)
            elif win_type == "bartlett": self.win_data = np.bartlett(L)
            elif win_type == "kaiser": self.win_data = np.kaiser(L, beta=14)
            
            # تحلیل تئوریک عرض لوب اصلی (تقریبی)
            widths = {"hamming": "8π/L", "hanning": "8π/L", "blackman": "12π/L", "bartlett": "8π/L", "kaiser": "Variable"}
            self.info_res.update_result(widths.get(win_type, "N/A"))
            
            # در اینجا plot_engine فراخوانی می‌شود تا نمودار را در UI آپدیت کند
            # فعلاً در کنسول لاگ می‌کنیم تا در main.py تجسم گرافیکی نهایی شود
            print(f"Window {win_type} generated with length {L}.")

        except Exception as e:
            self.info_res.update_result("Error in calculation")

    def _get_window_coeffs(self):
        """تبدیل ضرایب پنجره به رشته جهت کپی در کد HDL"""
        if not hasattr(self, 'win_data'): return None
        # تبدیل به فرمت ممیز شناور با دقت بالا
        coeffs_str = ", ".join([f"{val:.8f}" for val in self.win_data])
        return {"value": coeffs_str, "width": len(self.win_data)}
