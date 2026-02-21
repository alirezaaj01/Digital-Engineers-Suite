"""
Settings Manager Module
ذخیره و بازیابی تنظیمات کاربر در قالب فایل JSON برای ماندگاری (Persistence)
"""

import json
import os
import sys

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات پیش‌فرض
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class SettingsManager:
    def __init__(self):
        self.settings_path = config.PATHS["SETTINGS_FILE"]
        self.defaults = {
            "hdl_language": config.HDL_SETTINGS["DEFAULT_LANG"],
            "vhdl_standard": config.HDL_SETTINGS["VHDL_STANDARD"],
            "indent_size": config.HDL_SETTINGS["INDENT_SIZE"],
            "last_export_dir": config.PATHS["EXPORTS"],
            "theme_mode": "dark",
            "auto_copy_on_calculate": False
        }
        self.current_settings = self.load_settings()

    def load_settings(self):
        """بارگذاری تنظیمات از فایل؛ اگر فایل وجود نداشت، تنظیمات پیش‌فرض را می‌سازد"""
        if not os.path.exists(self.settings_path):
            self.save_settings(self.defaults)
            return self.defaults.copy()
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                # اطمینان از اینکه تمام کلیدهای ضروری وجود دارند (Merge با Defaults)
                full_settings = self.defaults.copy()
                full_settings.update(loaded)
                return full_settings
        except (json.JSONDecodeError, IOError):
            return self.defaults.copy()

    def save_settings(self, new_settings=None):
        """ذخیره تنظیمات فعلی در فایل JSON"""
        if new_settings:
            self.current_settings.update(new_settings)
            
        try:
            # اطمینان از وجود دایرکتوری قبل از ذخیره
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings, f, indent=4)
            return True
        except IOError:
            return False

    def get(self, key):
        """دریافت یک مقدار خاص از تنظیمات"""
        return self.current_settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        """تغییر یک مقدار و ذخیره آنی"""
        self.current_settings[key] = value
        self.save_settings()

# ایجاد یک نمونه سراسری برای استفاده در تمام بخش‌های برنامه
settings_manager = SettingsManager()
