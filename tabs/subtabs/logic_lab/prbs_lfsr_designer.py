"""
Professional PRBS & LFSR Designer Subtab
طراحی و تولید کد RTL برای مولدهای دنباله شبه‌تصادفی و ثبات‌های فیدبک خطی
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class PRBSDesigner(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # استانداردهای معروف PRBS (تپ‌های چندجمله‌ای)
        self.prbs_standards = {
            "PRBS7  (x^7 + x^6 + 1)": {"width": 7, "taps": [7, 6]},
            "PRBS9  (x^9 + x^5 + 1)": {"width": 9, "taps": [9, 5]},
            "PRBS15 (x^15 + x^14 + 1)": {"width": 15, "taps": [15, 14]},
            "PRBS23 (x^23 + x^18 + 1)": {"width": 23, "taps": [23, 18]},
            "PRBS31 (x^31 + x^28 + 1)": {"width": 31, "taps": [31, 28]}
        }
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- انتخاب استاندارد PRBS ---
        ctk.CTkLabel(self, text="Standard PRBS:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.std_var = ctk.StringVar(value=list(self.prbs_standards.keys())[0])
        self.std_menu = ctk.CTkOptionMenu(
            self, values=list(self.prbs_standards.keys()), 
            variable=self.std_var,
            fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"],
            button_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.std_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- مقدار اولیه (Seed) ---
        ctk.CTkLabel(self, text="Initial Seed (Hex):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.seed_entry = DarkEntry(self, placeholder="e.g. 0x1", validate_type="hex")
        self.seed_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.seed_entry.insert(0, "0x1")

        # --- دکمه تولید منطق ---
        self.gen_btn = ctk.CTkButton(
            self, text="Generate LFSR Logic", command=self._generate_logic,
            fg_color=config.UI_THEME["COLORS"]["SUCCESS"]
        )
        self.gen_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # --- نمایش معادله فیدبک ---
        self.logic_res = ResultLabel(self, text="---", prefix="Feedback Logic: ")
        self.logic_res.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # --- دکمه کپی کد RTL ---
        self.copy_btn = HDLCopyButton(self, self._get_hdl_payload, data_type="constant", text="Copy RTL Snippet")
        self.copy_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

    def _generate_logic(self):
        """تولید معادله منطقی بر اساس تپ‌های استاندارد"""
        selected = self.std_var.get()
        config_data = self.prbs_standards[selected]
        taps = config_data["taps"]
        width = config_data["width"]
        
        # تولید رشته متنی معادله (مثلاً: q(7) xor q(6))
        logic_parts = [f"r_reg({t-1})" for t in taps]
        self.current_logic_raw = " xor ".join(logic_parts)
        
        self.logic_res.update_result(f"Feedback = {self.current_logic_raw}")
        self.current_width = width

    def _get_hdl_payload(self):
        """آماده‌سازی داده برای کپی در کلیپ‌بورد"""
        if not hasattr(self, 'current_logic_raw'): return None
        return {
            "value": self.current_logic_raw,
            "width": self.current_width
        }
