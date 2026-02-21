"""
Hardware Input Validators Module
اعتبارسنجی ورودی‌های کاربر (هگز، باینری، اعشاری، فرمت Q و محدودیت‌های بیتی)
"""
import re

class HardwareValidators:
    @staticmethod
    def is_valid_hex(value_str):
        """بررسی صحت فرمت هگزادسیمال (با یا بدون پیشوند 0x/x)"""
        if not value_str: return False
        value_str = str(value_str).strip().upper().replace("0X", "").replace("X", "")
        return bool(re.fullmatch(r'[0-9A-F]+', value_str))

    @staticmethod
    def is_valid_binary(value_str):
        """بررسی صحت فرمت باینری (با یا بدون پیشوند 0b/b)"""
        if not value_str: return False
        value_str = str(value_str).strip().upper().replace("0B", "").replace("B", "")
        return bool(re.fullmatch(r'[01]+', value_str))

    @staticmethod
    def is_valid_float(value_str):
        """بررسی صحت عدد اعشاری (Float)"""
        try:
            float(value_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_q_format(q_str):
        """
        بررسی صحت فرمت Q (مثلا Q8.8 یا 8.8)
        خروجی: (وضعیت بررسی، تعداد بیت صحیح، تعداد بیت اعشاری)
        """
        if not q_str: return False, 0, 0
        q_str = str(q_str).strip().upper().replace("Q", "")
        match = re.fullmatch(r'(\d+)\.(\d+)', q_str)
        
        if match:
            integer_bits = int(match.group(1))
            fractional_bits = int(match.group(2))
            # جلوگیری از فرمت‌های غیرمنطقی مثل 0.0
            if integer_bits + fractional_bits > 0:
                return True, integer_bits, fractional_bits
        return False, 0, 0

    @staticmethod
    def validate_unsigned_bit_width(value, max_bits):
        """بررسی جا شدن یک عدد صحیح بدون علامت (Unsigned) در تعداد بیت مشخص"""
        try:
            val = int(value)
            max_val = (1 << max_bits) - 1
            return 0 <= val <= max_val
        except ValueError:
            return False

    @staticmethod
    def validate_signed_bit_width(value, max_bits):
        """بررسی جا شدن یک عدد علامت‌دار (Signed - Two's Complement) در تعداد بیت مشخص"""
        try:
            val = int(value)
            max_val = (1 << (max_bits - 1)) - 1
            min_val = -(1 << (max_bits - 1))
            return min_val <= val <= max_val
        except ValueError:
            return False

# یک نمونه (Instance) سراسری برای استفاده راحت در سایر ماژول‌ها
validator = HardwareValidators()
