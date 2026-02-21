"""
Universal HDL Snippet Generator
هسته اصلی تولید کدهای VHDL و Verilog برای تمام بخش‌های برنامه
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class HDLSnippetGenerator:
    @staticmethod
    def generate_constant(name, value, width, hdl_lang=None):
        """تولید کد تعریف ثابت (Constant/Parameter)"""
        lang = hdl_lang or config.HDL_SETTINGS["DEFAULT_LANG"]
        name = name.upper()
        
        if lang == "VHDL":
            # بررسی استایل بردارها در VHDL از تنظیمات
            vector_style = config.HDL_SETTINGS["VECTOR_DIRECTION"]
            if vector_style == "downto":
                range_str = f"{width-1} downto 0"
            else:
                range_str = f"0 to {width-1}"
                
            return f'constant {name} : std_logic_vector({range_str}) := x"{value}";'
        
        elif lang == "Verilog":
            return f'localparam [{width-1}:0] {name} = {width}\'h{value};'
            
        return ""

    @staticmethod
    def generate_array(name, values, width, depth, hdl_lang=None):
        """تولید کد آرایه (LUT/ROM)"""
        lang = hdl_lang or config.HDL_SETTINGS["DEFAULT_LANG"]
        name = name.upper()
        
        if lang == "VHDL":
            lines = [f"type {name}_ARRAY_TYPE is array (0 to {depth-1}) of std_logic_vector({width-1} downto 0);"]
            lines.append(f"constant {name} : {name}_ARRAY_TYPE := (")
            formatted_vals = [f'    x"{v}"' for v in values]
            lines.append(",\n".join(formatted_vals))
            lines.append(");")
            return "\n".join(lines)
            
        elif lang == "Verilog":
            lines = [f"reg [{width-1}:0] {name} [0:{depth-1}];"]
            lines.append("initial begin")
            for i, v in enumerate(values):
                lines.append(f"    {name}[{i}] = {width}'h{v};")
            lines.append("end")
            return "\n".join(lines)
            
        return ""
