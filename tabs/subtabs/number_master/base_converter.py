"""
Number Master Main Tab
تب اصلی مدیریت اعداد شامل زیرتب‌های مبدل مبنا، IEEE-754 و تبدیل داده
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class NumberMasterTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ایجاد Tabview برای سازماندهی ابزارهای مختلف اعداد
        self.tabview = ctk.CTkTabview(
            self,
            segmented_button_selected_color=config.UI_THEME["COLORS"]["ACCENT"],
            segmented_button_selected_hover_color=config.UI_THEME["COLORS"]["ACCENT_HOVER"]
        )
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ایجاد زیرتب‌ها
        self.tabview.add("Base Converter")
        self.tabview.add("IEEE-754 Analyzer")
        self.tabview.add("Fixed-Point Master")
        self.tabview.add("Data Type Converter")

        # در مراحل بعدی، هر زیرتب را با کلاس مخصوص خودش پر می‌کنیم
        self._setup_subtabs()

    def _setup_subtabs(self):
        """آماده‌سازی فریم‌های داخلی هر زیرتب"""
        
        # دسترسی به فریم‌های زیرتب‌ها برای چیدمان
        self.base_conv_frame = self.tabview.tab("Base Converter")
        self.ieee_frame = self.tabview.tab("IEEE-754 Analyzer")
        self.fp_frame = self.tabview.tab("Fixed-Point Master")
        self.data_type_frame = self.tabview.tab("Data Type Converter")

        # تنظیم گرید برای زیرتب‌ها
        for frame in [self.base_conv_frame, self.ieee_frame, self.fp_frame, self.data_type_frame]:
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        # به عنوان مثال، یک پیام موقت تا زمان کامل شدن ماژول بعدی:
        ctk.CTkLabel(self.base_conv_frame, text="Base Converter Module - Loading...").grid(pady=20)
        ctk.CTkLabel(self.ieee_frame, text="IEEE-754 Analyzer Module - Loading...").grid(pady=20)
