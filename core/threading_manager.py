"""
Background Threading Manager
مدیریت اجرای الگوریتم‌های سنگین در پس‌زمینه برای جلوگیری از فریز شدن رابط کاربری
"""

import threading
import logging
from concurrent.futures import ThreadPoolExecutor

class ThreadingManager:
    def __init__(self, max_workers=4):
        # استفاده از Executor برای مدیریت بهینه تعداد رشته‌ها
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_threads = []

    def run_task(self, task_func, callback=None, error_callback=None, *args, **kwargs):
        """
        اجرای یک تابع در پس‌زمینه
        task_func: تابعی که باید اجرا شود (مثلاً تولید یک سیگنال سنگین)
        callback: تابعی که پس از اتمام موفقیت‌آمیز با نتیجه اجرا می‌شود
        error_callback: تابعی که در صورت بروز خطا اجرا می‌شود
        """
        def wrapper():
            try:
                # اجرای تابع اصلی
                result = task_func(*args, **kwargs)
                
                # اگر کالبک تعریف شده باشد، نتیجه را به آن برمی‌گردانیم
                if callback:
                    # نکته: در برنامه‌های GUI، تغییرات UI باید در Thread اصلی انجام شود
                    # این منیجر فرض می‌کند کالبک فرستاده شده این موضوع را مدیریت می‌کند
                    callback(result)
                    
            except Exception as e:
                logging.error(f"Error in background task: {str(e)}")
                if error_callback:
                    error_callback(e)

        # شروع اجرای ترد
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        return thread

    def shutdown(self):
        """بستن تمام پردازش‌ها هنگام خروج از برنامه"""
        self.executor.shutdown(wait=False)

# ایجاد یک نمونه سراسری
thread_manager = ThreadingManager()
