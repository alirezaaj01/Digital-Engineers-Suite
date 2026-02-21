"""
Professional CORDIC Engine
محاسبات تکرار شونده CORDIC برای توابع مثلثاتی و تبدیل مختصات در سخت‌افزار
"""

import numpy as np
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class CordicEngine:
    def __init__(self, iterations=None):
        # تعداد تکرارها از فایل تنظیمات خوانده می‌شود یا به صورت دستی وارد می‌گردد
        self.iterations = iterations or config.DSP_CONFIG.get("CORDIC_ITERATIONS", 16)
        # پیش‌محاسبه جدول آرکتان (Atan Table) برای سرعت بالاتر
        self.atan_table = [np.arctan(2.0**(-i)) for i in range(self.iterations)]
        # ضریب تصحیح بهره (Gain Factor) که به سمت 0.607252... میل می‌کند
        self.gain = self._calculate_gain()

    def _calculate_gain(self):
        """محاسبه ضریب مقیاس (An) برای تعداد تکرار مشخص شده"""
        gain = 1.0
        for i in range(self.iterations):
            gain *= np.sqrt(1 + 2.0**(-2 * i))
        return 1.0 / gain

    def rotate(self, target_angle_rad):
        """
        حالت چرخش (Rotation Mode): محاسبه Sin و Cos یک زاویه
        خروجی: (cos, sin)
        """
        x = self.gain
        y = 0.0
        z = target_angle_rad

        for i in range(self.iterations):
            if z >= 0:
                d = 1
            else:
                d = -1
            
            x_new = x - d * y * (2.0**(-i))
            y_new = y + d * x * (2.0**(-i))
            z_new = z - d * self.atan_table[i]
            
            x, y, z = x_new, y_new, z_new
            
        return x, y

    def vectorize(self, x_in, y_in):
        """
        حالت برداری (Vector Mode): محاسبه اندازه و فاز (Magnitude & Phase)
        خروجی: (magnitude, phase_rad)
        """
        x = x_in
        y = y_in
        z = 0.0

        for i in range(self.iterations):
            if y < 0:
                d = 1
            else:
                d = -1
            
            x_new = x - d * y * (2.0**(-i))
            y_new = y + d * x * (2.0**(-i))
            z_new = z - d * self.atan_table[i]
            
            x, y, z = x_new, y_new, z_new
            
        # در این حالت x نهایی ضرب در (1/gain) برابر با اندازه بردار است
        return x * self.gain, -z

    def get_fixed_point_table(self, bit_width):
        """تولید جدول Atan به صورت Hex برای استفاده در کدهای VHDL/Verilog"""
        table_hex = []
        for val in self.atan_table:
            # تبدیل زاویه رادیان به مقدار فیکس پوینت (فرض: Q1.X)
            scale = (1 << (bit_width - 1)) / np.pi
            int_val = int(round(val * scale))
            table_hex.append(f"{int_val:X}")
        return table_hex

# ایجاد نمونه سراسری
cordic_engine = CordicEngine()
