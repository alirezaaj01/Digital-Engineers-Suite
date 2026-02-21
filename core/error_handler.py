"""
Professional Error Handling & Logging System
مدیریت استثناها و ثبت خطاهای سیستم در فایل برای عیب‌یابی (Debugging)
"""

import logging
import os
import sys
from datetime import datetime
from tkinter import messagebox

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class ErrorHandler:
    def __init__(self):
        self.log_dir = config.PATHS["LOGS"]
        self._setup_logging()

    def _setup_logging(self):
        """تنظیمات اولیه کتابخانه logging"""
        log_file = os.path.join(self.log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG if config.LOGGING_CONFIG["LEVEL"] == "DEBUG" else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
            encoding='utf-8'
        )

        # اگر تنظیم شده باشد، لاگ‌ها در کنسول هم نمایش داده شوند
        if config.LOGGING_CONFIG["ENABLE_CONSOLE_LOG"]:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            logging.getLogger('').addHandler(console)

    @staticmethod
    def log_error(message, include_traceback=True):
        """ثبت خطا در فایل لاگ بدون قطع اجرای برنامه"""
        logging.error(message, exc_info=include_traceback)

    @staticmethod
    def show_error(title, message, parent=None):
        """نمایش پنجره خطا به کاربر و ثبت در لاگ"""
        logging.error(f"User Error Dialog [{title}]: {message}")
        messagebox.showerror(title, message, parent=parent)

    @staticmethod
    def show_info(title, message, parent=None):
        """نمایش پنجره اطلاع‌رسانی"""
        messagebox.showinfo(title, message, parent=parent)

    @staticmethod
    def handle_critical_exception(e):
        """مدیریت خطاهای بحرانی که ممکن است باعث کرش برنامه شوند"""
        error_msg = f"A critical error occurred: {str(e)}"
        logging.critical(error_msg, exc_info=True)
        messagebox.showerror("Critical Error", "The application encountered a serious problem.\nCheck the logs for details.")

# ایجاد یک نمونه سراسری
error_handler = ErrorHandler()
