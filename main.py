"""
Digital Engineer's Suite - Main Application Entry Point
"""

import customtkinter as ctk
import os
import sys

# تنظیم مسیر پایه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import config

# تنظیم تم کلی customtkinter بر اساس تنظیمات شما
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DigitalEngineerSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        # تنظیمات پنجره اصلی
        self.title(f"{config.APP_INFO['NAME']} v{config.APP_INFO['VERSION']}")
        
        # ابعاد پنجره
        min_w = config.UI_THEME["DIMENSIONS"]["MIN_WIDTH"]
        min_h = config.UI_THEME["DIMENSIONS"]["MIN_HEIGHT"]
        self.geometry(f"{min_w}x{min_h}")
        self.minsize(min_w, min_h)
        
        # رنگ پس زمینه اصلی
        self.configure(fg_color=config.UI_THEME["COLORS"]["BG_MAIN"])

        self._build_ui()

    def _build_ui(self):
        """ساخت رابط کاربری اصلی شامل تب‌ها"""
        # ساخت TabView برای مدیریت بخش‌های مختلف
        self.main_tabview = ctk.CTkTabview(
            self, 
            fg_color=config.UI_THEME["COLORS"]["BG_SIDEBAR"],
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            segmented_button_selected_color=config.UI_THEME["COLORS"]["ACCENT"],
            segmented_button_selected_hover_color=config.UI_THEME["COLORS"]["ACCENT_HOVER"]
        )
        self.main_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # اضافه کردن تب‌های اصلی
        self.tab_number_master = self.main_tabview.add("Number Master")
        self.tab_code_gen = self.main_tabview.add("Code Generators")
        self.tab_dsp_tools = self.main_tabview.add("DSP Tools")
        self.tab_hw_utils = self.main_tabview.add("Hardware Utils")

        # یک لیبل موقت برای نمایش اجرای موفق
        ctk.CTkLabel(
            self.tab_number_master, 
            text="Welcome to Number Master!\n(UI components will be loaded here)", 
            font=config.UI_THEME["FONTS"]["HEADER"]
        ).pack(expand=True)

if __name__ == "__main__":
    app = DigitalEngineerSuite()
    app.mainloop()
