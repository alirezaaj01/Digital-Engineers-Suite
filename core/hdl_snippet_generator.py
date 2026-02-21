"""
Universal HDL Snippet Generator
هسته اصلی تولید کدهای VHDL و Verilog برای استفاده در سراسر برنامه
"""

import sys
import os
# اضافه کردن مسیر ریشه به sys.path برای دسترسی به config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class HDLSnippetGenerator:
    def __init__(self):
        # زبان پیش‌فرض از فایل تنظیمات خوانده می‌شود
        self.language = config.DEFAULT_HDL_LANG  

    def set_language(self, lang):
        """تغییر زبان تولید کد در زمان اجرا"""
        if lang in ["VHDL", "Verilog"]:
            self.language = lang

    def generate_constant(self, name, value, bit_width=None, data_type="std_logic_vector"):
        """تولید کد تعریف ثابت (Constant) در سخت‌افزار"""
        name = name.upper()
        
        if self.language == "VHDL":
            if data_type == "std_logic_vector" and bit_width:
                return f'constant {name}: {data_type}({bit_width-1} {config.VHDL_STD_LOGIC_VECTOR_STYLE} 0) := "{value}";'
            elif data_type == "integer":
                return f'constant {name}: integer := {value};'
            elif data_type == "unsigned" and bit_width:
                 return f'constant {name}: unsigned({bit_width-1} {config.VHDL_STD_LOGIC_VECTOR_STYLE} 0) := to_unsigned({value}, {bit_width});'
                 
        elif self.language == "Verilog":
            if bit_width:
                return f'localparam [{bit_width-1}:0] {name} = {bit_width}\'h{value};'
            return f'localparam {name} = {value};'
            
        return ""

    def generate_rgb_color(self, name, hex_color):
        """تولید اسنیپت برای رنگ RGB (مفید برای درایورهای VGA/LCD)"""
        name = name.upper()
        hex_color = hex_color.replace("#", "")
        
        if self.language == "VHDL":
            return f'constant {name}: std_logic_vector(23 downto 0) := x"{hex_color}";'
        elif self.language == "Verilog":
            return f'localparam [23:0] {name} = 24\'h{hex_color};'

    def generate_fixed_point_coeff(self, name, hex_value, bit_width=16):
        """تولید اسنیپت برای ضرایب ممیز ثابت (مناسب برای فیلترهای FIR و DSP)"""
        name = name.upper()
        
        if self.language == "VHDL":
            return f'constant {name}: signed({bit_width-1} {config.VHDL_STD_LOGIC_VECTOR_STYLE} 0) := x"{hex_value}";'
        elif self.language == "Verilog":
            return f'localparam signed [{bit_width-1}:0] {name} = {bit_width}\'h{hex_value};'

    def generate_instantiation_template(self, entity_name, ports):
        """تولید قالب خام برای نمونه‌سازی (Instantiation) یک ماژول"""
        # این متد در فازهای بعدی برای Entity Skeleton تکمیل می‌شود
        pass

# ایجاد یک نمونه (Instance) سراسری سینگلتون برای استفاده در تمام تب‌های UI
snippet_generator = HDLSnippetGenerator()
