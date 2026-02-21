"""
Professional Base Converter Subtab - FIXED
مبدل آنی مبناهای دهدهی، شانزده‌دهی و باینری با قابلیت اعتبارسنجی
"""

import customtkinter as ctk
import sys
import os

# رفتن به ۴ پوشه بالاتر برای رسیدن به ریشه پروژه (Root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel

class BaseConverter(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- بخش ورودی دهدهی (Decimal) ---
        ctk.CTkLabel(self, text="Decimal:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dec_entry = DarkEntry(self, placeholder="e.g. 255", validate_type="float") # استفاده از اعتبارسنجی اعداد
        self.dec_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.dec_entry.bind("<KeyRelease>", lambda e: self._convert_from("dec"))

        # --- بخش ورودی شانزده‌دهی (Hexadecimal) ---
        ctk.CTkLabel(self, text="Hexadecimal:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.hex_entry = DarkEntry(self, placeholder="e.g. FF", validate_type="hex")
        self.hex_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.hex_entry.bind("<KeyRelease>", lambda e: self._convert_from("hex"))

        # --- بخش ورودی باینری (Binary) ---
        ctk.CTkLabel(self, text="Binary:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.bin_entry = DarkEntry(self, placeholder="e.g. 11111111", validate_type="bin")
        self.bin_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.bin_entry.bind("<KeyRelease>", lambda e: self._convert_from("bin"))

        # --- بخش نمایش وضعیت ---
        self.info_label = ResultLabel(self, text="Enter a value to convert", prefix="Status: ")
        self.info_label.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def _convert_from(self, source):
        """الگوریتم تبدیل متقابل مبناها در لحظه"""
        try:
            val_str = ""
            base = 10
            
            if source == "dec":
                val_str = self.dec_entry.get().strip()
                base = 10
            elif source == "hex":
                val_str = self.hex_entry.get().strip()
                base = 16
            elif source == "bin":
                val_str = self.bin_entry.get().strip()
                base = 2

            if not val_str:
                self._clear_all_except(source)
                return

            # تبدیل به عدد صحیح (مدیریت هگز با حذف 0x احتمالی)
            clean_val = val_str.replace("0x", "").replace("0X", "")
            value = int(clean_val, base)

            # به‌روزرسانی سایر فیلدها بدون تداخل با تایپ کاربر
            if source != "dec":
                self.dec_entry.delete(0, ctk.END)
                self.dec_entry.insert(0, str(value))
            
            if source != "hex":
                self.hex_entry.delete(0, ctk.END)
                self.hex_entry.insert(0, hex(value)[2:].upper())
            
            if source != "bin":
                self.bin_entry.delete(0, ctk.END)
                self.bin_entry.insert(0, bin(value)[2:])
            
            self.info_label.update_result("Success")
            
        except ValueError:
