"""
Professional Waveform & LUT Generation Engine
تولید سیگنال‌های دیجیتال و خروجی‌های حافظه (COE/MIF/HEX) برای FPGA
"""

import numpy as np
import math
import os
import sys

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class WaveformEngine:
    def __init__(self):
        self.dsp_settings = config.DSP_CONFIG
        self.file_settings = config.FPGA_TARGETS["FILE_EXTENSIONS"]

    def generate_signal(self, wave_type, samples, amplitude, freq_hz=1, fs_hz=100, phase_deg=0):
        """
        تولید آرایه نمونه‌های سیگنال بر اساس پارامترهای فیزیکی
        """
        t = np.arange(samples) / fs_hz
        phase_rad = np.deg2rad(phase_deg)
        
        if wave_type.lower() == "sine":
            signal = amplitude * np.sin(2 * np.pi * freq_hz * t + phase_rad)
        elif wave_type.lower() == "square":
            signal = amplitude * np.sign(np.sin(2 * np.pi * freq_hz * t + phase_rad))
        elif wave_type.lower() == "sawtooth":
            signal = amplitude * (2 * (freq_hz * t + phase_deg/360 - np.floor(0.5 + freq_hz * t + phase_deg/360)))
        elif wave_type.lower() == "noise":
            signal = amplitude * np.random.uniform(-1, 1, samples)
        else:
            raise ValueError(f"Wave type {wave_type} not supported.")
            
        return signal

    def quantize_for_hdl(self, signal, bit_width, is_signed=True):
        """
        کوانتایز کردن سیگنال برای سخت‌افزار با رعایت محدوده بیت‌ها
        """
        if is_signed:
            max_val = (1 << (bit_width - 1)) - 1
            min_val = -(1 << (bit_width - 1))
        else:
            max_val = (1 << bit_width) - 1
            min_val = 0

        # نرمال‌سازی و مقیاس‌دهی به محدوده سخت‌افزاری
        # فرض بر این است که دامنه ورودی (Amplitude) با دقت تنظیم شده است
        quantized = np.round(signal)
        
        # اعمال اشباع (Saturation)
        quantized = np.clip(quantized, min_val, max_val).astype(np.int64)
        
        return quantized

    def to_hex_list(self, quantized_signal, bit_width):
        """تبدیل آرایه اعداد به لیست رشته‌های هگزادسیمال"""
        hex_len = math.ceil(bit_width / 4)
        hex_list = []
        for val in quantized_signal:
            if val < 0:
                val = (1 << bit_width) + val
            hex_list.append(f"{val:0{hex_len}X}")
        return hex_list

    def export_coe(self, hex_list, radix=16):
        """تولید محتوای فایل COE برای Xilinx IP Core (مثل Block Memory Generator)"""
        header = f"memory_initialization_radix={radix};\n"
        header += "memory_initialization_vector=\n"
        body = ",\n".join(hex_list) + ";"
        return header + body

    def export_mif(self, hex_list, bit_width):
        """تولید محتوای فایل MIF برای Intel/Altera"""
        depth = len(hex_list)
        header = f"DEPTH = {depth};\nWIDTH = {bit_width};\nADDRESS_RADIX = DEC;\nDATA_RADIX = HEX;\n\nCONTENT\nBEGIN\n"
        body = ""
        for i, val in enumerate(hex_list):
            body += f"    {i} : {val};\n"
        footer = "END;"
        return header + body + footer

# نمونه‌سازی سراسری
waveform_engine = WaveformEngine()
