"""
Professional Timing & Protocol Engine
محاسبات فرکانس، دوره تناوب و پارامترهای زمان‌بندی پروتکل‌های ارتباطی (UART, SPI, I2C)
"""

import math
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class TimingEngine:
    @staticmethod
    def freq_to_period(freq_hz):
        """تبدیل فرکانس به دوره تناوب (ثانیه)"""
        if freq_hz <= 0: return 0
        return 1.0 / freq_hz

    @staticmethod
    def period_to_freq(period_sec):
        """تبدیل دوره تناوب به فرکانس (هرتز)"""
        if period_sec <= 0: return 0
        return 1.0 / period_sec

    @staticmethod
    def calculate_uart_divider(system_clk_hz, target_baud_rate):
        """
        محاسبه عدد تقسیم‌کننده (Divider) برای UART
        فرمول: Divider = System_Clock / (Baud_Rate * Oversampling)
        Oversampling معمولاً 16 است.
        """
        if target_baud_rate <= 0: return 0
        oversampling = 16
        divider = system_clk_hz / (target_baud_rate * oversampling)
        
        # محاسبه درصد خطا
        actual_baud = system_clk_hz / (round(divider) * oversampling)
        error_percent = abs((actual_baud - target_baud_rate) / target_baud_rate) * 100
        
        return {
            "divider_float": divider,
            "divider_integer": round(divider),
            "actual_baud": round(actual_baud, 2),
            "error_percent": round(error_percent, 4)
        }

    @staticmethod
    def calculate_spi_clock(system_clk_hz, target_sclk_hz):
        """
        محاسبه تقسیم‌کننده کلاک SPI
        معمولاً در FPGAها تقسیم‌کننده باید مضربی از 2 باشد.
        """
        if target_sclk_hz <= 0: return 0
        raw_divider = system_clk_hz / target_sclk_hz
        # گرد کردن به نزدیک‌ترین عدد زوج (Power of 2 یا زوج ساده بر اساس معماری)
        even_divider = math.ceil(raw_divider / 2) * 2
        
        actual_sclk = system_clk_hz / even_divider
        
        return {
            "divider": even_divider,
            "actual_sclk_mhz": actual_sclk / 1e6,
            "period_ns": (1.0 / actual_sclk) * 1e9
        }

    @staticmethod
    def calculate_data_rate(bus_width_bits, frequency_hz):
        """محاسبه نرخ انتقال داده (Throughput)"""
        bits_per_second = bus_width_bits * frequency_hz
        return {
            "bps": bits_per_second,
            "kbps": bits_per_second / 1e3,
            "mbps": bits_per_second / 1e6,
            "gbps": bits_per_second / 1e9
        }

# ایجاد یک نمونه سراسری
timing_engine = TimingEngine()
