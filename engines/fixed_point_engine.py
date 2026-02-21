"""
Fixed-Point Math Engine
موتور تبدیل اعداد اعشاری (Float) به ممیز ثابت (Fixed-Point / Q-Format) برای سخت‌افزار
"""

class FixedPointEngine:
    @staticmethod
    def float_to_fixed(float_val, integer_bits, fractional_bits, is_signed=True):
        """
        تبدیل عدد اعشاری به فرمت سخت‌افزاری Q-Format
        
        خروجی یک دیکشنری شامل مقدار کوانتایز شده، خطای محاسبه، و رشته‌های هگز/باینری است.
        """
        total_bits = integer_bits + fractional_bits
        scale_factor = 1 << fractional_bits  # معادل 2 به توان fractional_bits
        
        # کوانتایز کردن (گرد کردن به نزدیک‌ترین عدد صحیح)
        raw_val = round(float_val * scale_factor)
        
        # محاسبه بازه مجاز برای بررسی سرریز (Overflow)
        if is_signed:
            min_val = -(1 << (total_bits - 1))
            max_val = (1 << (total_bits - 1)) - 1
        else:
            min_val = 0
            max_val = (1 << total_bits) - 1
            
        # بررسی و اعمال اشباع (Saturation) در صورت سرریز
        overflow = False
        if raw_val > max_val:
            raw_val = max_val
            overflow = True
        elif raw_val < min_val:
            raw_val = min_val
            overflow = True
            
        # محاسبه مقدار واقعی کوانتایز شده و خطای گردکردن
        quantized_float = raw_val / scale_factor
        quantization_error = float_val - quantized_float
        
        # اعمال متمم دو (Two's Complement) برای اعداد منفی جهت نمایش سخت‌افزاری
        hw_val = raw_val
        if is_signed and hw_val < 0:
            hw_val = (1 << total_bits) + hw_val
            
        # تولید رشته‌های باینری و هگزادسیمال با طول ثابت
        hex_chars = (total_bits + 3) // 4  # محاسبه تعداد کاراکترهای هگز
        hex_str = f"{hw_val:0{hex_chars}X}"
        bin_str = f"{hw_val:0{total_bits}b}"
        
        return {
            "original": float_val,
            "quantized": quantized_float,
            "hardware_integer": raw_val, # مقدار صحیحی که در رجیستر ذخیره می‌شود
            "hex": hex_str,
            "binary": bin_str,
            "error": quantization_error,
            "overflow": overflow,
            "total_bits": total_bits
        }

    @staticmethod
    def fixed_to_float(hardware_val_str, integer_bits, fractional_bits, base=16, is_signed=True):
        """
        عملیات معکوس: تبدیل رشته هگز یا باینریِ سخت‌افزار به عدد اعشاری
        """
        total_bits = integer_bits + fractional_bits
        hw_val = int(str(hardware_val_str), base)
        
        # بررسی متمم دو برای اعداد علامت‌دار
        if is_signed and (hw_val & (1 << (total_bits - 1))):
            hw_val -= (1 << total_bits)
            
        scale_factor = 1 << fractional_bits
        return hw_val / scale_factor

# نمونه‌سازی سراسری
fp_engine = FixedPointEngine()
