"""
Logic Lab Main Tab
تب اصلی آزمایشگاه منطق شامل ابزارهای تولید CRC، PRBS و محاسبات چک‌سام
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LogicLabTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ایجاد Tabview برای سازماندهی ابزارهای منطقی
        self.tabview = ctk.CTkTabview(
            self,
            segmented_button_selected_color=config.UI_THEME["COLORS"]["SUCCESS"], # رنگ متمایز برای این تب
            segmented_button_selected_hover_color=config.UI_THEME["COLORS"]["ACCENT_HOVER"]
        )
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ایجاد زیرتب‌های تخصصی
        self.tabview.add("CRC Generator")
        self.tabview.add("PRBS & LFSR")
        self.tabview.add("Checksum Calc")

        self._setup_subtabs()

    def _setup_subtabs(self):
        """آماده‌سازی فریم‌های داخلی برای هر ابزار منطقی"""
        self.crc_frame = self.tabview.tab("CRC Generator")
        self.prbs_frame = self.tabview.tab("PRBS & LFSR")
        self.checksum_frame = self.tabview.tab("Checksum Calc")

        # تنظیم گرید برای زیرتب‌ها
        for frame in [self.crc_frame, self.prbs_frame, self.checksum_frame]:
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        # قرار دادن لیبل‌های موقت (تا زمان تکمیل ماژول‌های بعدی)
        ctk.CTkLabel(self.crc_frame, text="CRC Hardware Engine - Ready for integration").grid(pady=20)
        ctk.CTkLabel(self.prbs_frame, text="PRBS/LFSR Designer - Ready for integration").grid(pady=20)
