"""
Professional IEEE-754 Floating Point Analyzer
تحلیل‌گر اعداد ممیز شناور و تجزیه به بیت‌های علامت، توان و مانتیس
"""

import customtkinter as ctk
import struct
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel

class IEEE754Analyzer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # ورودی عدد اعشاری
        ctk.CTkLabel(self, text="Float Value:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.float_entry = DarkEntry(self, placeholder="e.g. -12.625", validate_type="float")
        self.float_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.float_entry.bind("<KeyRelease>", self._analyze)

        # نمایش هگزادسیمال
        self.hex_res = ResultLabel(self, text="---", prefix="Hex (32-bit): ")
        self.hex_res.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # نمایش باینری کامل
        self.bin_res = ResultLabel(self, text="---", prefix="Binary: ")
        self.bin_res.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # تفکیک اجزاء (Sign, Exponent, Mantissa)
        self.parts_frame = ctk.CTkFrame(self, fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"])
        self.parts_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")
        self.parts_frame.columnconfigure((0,1,2), weight=1)

        self.sign_lbl = ctk.CTkLabel(self.parts_frame, text="Sign: -", text_color="#FFD700")
        self.sign_lbl.grid(row=0, column=0, pady=10)
        
        self.exp_lbl = ctk.CTkLabel(self.parts_frame, text="Exponent: -", text_color="#00FF7F")
        self.exp_lbl.grid(row=0, column=1, pady=10)
        
        self.man_lbl = ctk.CTkLabel(self.parts_frame, text="Mantissa: -", text_color="#00BFFF")
        self.man_lbl.grid(row=0, column=2, pady=10)

    def _analyze(self, event=None):
        """الگوریتم تجزیه عدد اعشاری به فرمت IEEE-754"""
        try:
            val_str = self.float_entry.get().strip()
            if not val_str:
                self._reset_labels()
                return

            f_val = float(val_str)
            # تبدیل به نمایش باینری ۳۲ بیتی (Single Precision)
            [packed] = struct.unpack('>I', struct.pack('>f', f_val))
            bin_str = f"{packed:032b}"
            hex_str = f"{packed:08X}"

            # به‌روزرسانی نتایج متنی
            self.hex_res.update_result(hex_str)
            self.bin_res.update_result(bin_str)

            # تجزیه بیت‌ها (1 | 8 | 23)
            sign = bin_str[0]
            exponent = bin_str[1:9]
            mantissa = bin_str[9:]

            # به‌روزرسانی بخش اجزاء با رنگ‌بندی تفکیکی
            self.sign_lbl.configure(text=f"Sign: {sign}")
            self.exp_lbl.configure(text=f"Exp: {exponent}")
            self.man_lbl.configure(text=f"Mantissa: {mantissa[:8]}...")
            
        except ValueError:
            self._reset_labels()

    def _reset_labels(self):
        self.hex_res.update_result("---")
        self.bin_res.update_result("---")
        self.sign_lbl.configure(text="Sign: -")
        self.exp_lbl.configure(text="Exponent: -")
        self.man_lbl.configure(text="Mantissa: -")
