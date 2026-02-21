"""
Professional Data Type Interpreter
مفسر انواع داده‌های باینری به صورت علامت‌دار و بدون علامت در عرض‌های بیتی مختلف
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel

class DataTypeConverter(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # ورودی مقدار خام (Raw Value)
        ctk.CTkLabel(self, text="Raw Value (Hex/Dec):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.raw_entry = DarkEntry(self, placeholder="e.g. 0xFFFF", validate_type=None)
        self.raw_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.raw_entry.bind("<KeyRelease>", self._interpret)

        # انتخاب عرض بیتی (Bit-Width)
        ctk.CTkLabel(self, text="Bit Width:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.bit_width_var = ctk.StringVar(value="16")
        self.bit_width_menu = ctk.CTkOptionMenu(
            self, values=["8", "16", "32", "64"], 
            variable=self.bit_width_var,
            command=self._interpret,
            fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"],
            button_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.bit_width_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # نمایش نتایج تفاسیر مختلف
        self.unsigned_res = ResultLabel(self, text="---", prefix="Unsigned: ")
        self.unsigned_res.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.signed_res = ResultLabel(self, text="---", prefix="Signed (2's Comp): ")
        self.signed_res.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.bin_res = ResultLabel(self, text="---", prefix="Binary Pattern: ")
        self.bin_res.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def _interpret(self, event=None):
        """الگوریتم تفسیر بیت‌ها بر اساس عرض انتخابی"""
        try:
            val_str = self.raw_entry.get().strip()
            if not val_str:
                self._clear_results()
                return

            # تشخیص مبنا (هگز یا دهدهی)
            if val_str.lower().startswith('0x') or any(c in 'abcdefABCDEF' for c in val_str):
                raw_val = int(val_str, 16)
            else:
                raw_val = int(val_str)

            width = int(self.bit_width_var.get())
            mask = (1 << width) - 1
            masked_val = raw_val & mask

            # ۱. تفسیر بدون علامت (Unsigned)
            unsigned_val = masked_val

            # ۲. تفسیر علامت‌دار (Signed - Two's Complement)
            if masked_val & (1 << (width - 1)):
                signed_val = masked_val - (1 << width)
            else:
                signed_val = masked_val

            # ۳. الگوی باینری
            bin_pattern = f"{masked_val:0{width}b}"
            
            # به‌روزرسانی نمایشگرها
            self.unsigned_res.update_result(str(unsigned_val))
            self.signed_res.update_result(str(signed_val))
            self.bin_res.update_result(bin_pattern)

        except ValueError:
            self._clear_results()

    def _clear_results(self):
        self.unsigned_res.update_result("---")
        self.signed_res.update_result("---")
        self.bin_res.update_result("---")
