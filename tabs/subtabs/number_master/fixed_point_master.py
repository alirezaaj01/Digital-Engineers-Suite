"""
Professional Fixed-Point Designer & Converter
مبدل تخصصی اعداد اعشاری به ممیز ثابت (Q-Format) با تحلیل خطا
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات، موتورها و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from engines.fixed_point_engine import fp_engine
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class FixedPointMaster(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # ورودی عدد اعشاری (Float)
        ctk.CTkLabel(self, text="Float Value:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.float_entry = DarkEntry(self, placeholder="e.g. 0.707", validate_type="float")
        self.float_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # ورودی فرمت Q (مثلا 8.8)
        ctk.CTkLabel(self, text="Q-Format (I.F):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.q_entry = DarkEntry(self, placeholder="e.g. 1.15", validate_type=None) # فرمت Q اختصاصی بررسی می‌شود
        self.q_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.q_entry.insert(0, "1.15")

        # سوئیچ علامت‌دار/بدون علامت
        self.signed_var = ctk.BooleanVar(value=True)
        self.signed_switch = ctk.CTkSwitch(self, text="Signed (Two's Complement)", variable=self.signed_var, 
                                          progress_color=config.UI_THEME["COLORS"]["ACCENT"])
        self.signed_switch.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # دکمه محاسبه
        self.calc_btn = ctk.CTkButton(self, text="Calculate & Analyze", command=self._calculate,
                                      fg_color=config.UI_THEME["COLORS"]["ACCENT"])
        self.calc_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # نمایش نتایج
        self.hex_res = ResultLabel(self, text="---", prefix="Hex Result: ")
        self.hex_res.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.bin_res = ResultLabel(self, text="---", prefix="Binary Result: ")
        self.bin_res.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.error_res = ResultLabel(self, text="---", prefix="Quantization Error: ")
        self.error_res.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # دکمه جادویی کپی به صورت HDL
        self.copy_btn = HDLCopyButton(self, self._get_export_data, data_type="fixed_point")
        self.copy_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

    def _calculate(self):
        """اجرای محاسبات و به‌روزرسانی رابط کاربری"""
        try:
            val = float(self.float_entry.get())
            q_str = self.q_entry.get()
            
            # استخراج بیت‌های صحیح و اعشاری
            parts = q_str.split('.')
            if len(parts) != 2: raise ValueError
            i_bits, f_bits = int(parts[0]), int(parts[1])
            
            # استفاده از موتور اصلی برای محاسبات
            result = fp_engine.float_to_fixed(val, i_bits, f_bits, is_signed=self.signed_var.get())
            
            # به‌روزرسانی لیبل‌ها
            self.hex_res.update_result(result["hex"])
            self.bin_res.update_result(result["binary"])
            self.error_res.update_result(f"{result['error']:.8f}")
            
            # نمایش هشدار در صورت Overflow
            if result["overflow"]:
                self.error_res.configure(text_color=config.UI_THEME["COLORS"]["WARNING"])
            else:
                self.error_res.configure(text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"])

        except (ValueError, ZeroDivisionError):
            self.hex_res.update_result("Error: Invalid Format")

    def _get_export_data(self):
        """آماده‌سازی داده برای دکمه کپی HDL"""
        q_str = self.q_entry.get()
        try:
            parts = q_str.split('.')
            width = int(parts[0]) + int(parts[1])
            return {
                "hex": self.hex_res.actual_value,
                "width": width
            }
        except:
            return None
