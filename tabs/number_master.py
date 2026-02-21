"""
Number Master Tab (Main Container)
مدیریت زیرتب‌های مربوط به تبدیل اعداد و محاسبات پایه‌ای
"""
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from tabs.subtabs.number_master.base_converter import BaseConverterTab
from tabs.subtabs.number_master.fixed_point_master import FixedPointMasterTab
# سایر تب‌ها در صورت وجود اضافه می‌شوند

class NumberMasterTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._setup_subtabs()

    def _setup_subtabs(self):
        """ساخت تب‌های داخلی (Subtabs)"""
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=config.UI_THEME["COLORS"]["BG_SIDEBAR"],
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            segmented_button_selected_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)

        # اضافه کردن بخش‌ها
        self.tab_base = self.tabview.add("Base Converter")
        self.tab_fixed = self.tabview.add("Fixed-Point")
        self.tab_data_type = self.tabview.add("Data Type")
        self.tab_ieee754 = self.tabview.add("IEEE-754")

        # مقداردهی کلاس‌های زیرتب و قرار دادن در تب مربوطه
        self.base_converter_ui = BaseConverterTab(self.tab_base)
        self.base_converter_ui.pack(fill="both", expand=True)
        
        self.fixed_point_ui = FixedPointMasterTab(self.tab_fixed)
        self.fixed_point_ui.pack(fill="both", expand=True)

        # برای تب‌های Data Type و IEEE-754 موقتاً لیبل قرار می‌دهیم تا فایل‌هایشان کامل شود
        ctk.CTkLabel(self.tab_data_type, text="Data Type Converter: Coming Soon").pack(expand=True)
        ctk.CTkLabel(self.tab_ieee754, text="IEEE-754 Analyzer: Coming Soon").pack(expand=True)
