"""
CRC & LFSR Engine Module
محاسبه نرم‌افزاری مقادیر CRC و تولید خودکار کدهای سخت‌افزاری VHDL/Verilog برای LFSR
"""

class CRCEngine:
    def __init__(self):
        # چندجمله‌ای‌های استاندارد و پرکاربرد در سخت‌افزار
        self.standard_polys = {
            "CRC-8 (ATM)": {"poly": 0x07, "width": 8},       # x^8 + x^2 + x + 1
            "CRC-16 (CCITT)": {"poly": 0x1021, "width": 16}, # x^16 + x^12 + x^5 + 1
            "CRC-32 (IEEE 802.3)": {"poly": 0x04C11DB7, "width": 32}
        }

    def calculate_crc_software(self, data_bytes, poly, bit_width, init_val=0x00, xor_out=0x00):
        """
        محاسبه CRC یک آرایه از بایت‌ها به صورت نرم‌افزاری
        (کاربرد: تولید داده‌های Golden Reference برای تست‌بنچ)
        """
        crc = init_val
        for byte in data_bytes:
            crc ^= (byte << (bit_width - 8))
            for _ in range(8):
                if crc & (1 << (bit_width - 1)):
                    crc = (crc << 1) ^ poly
                else:
                    crc = (crc << 1)
            # محدود کردن به طول بیت مورد نظر
            crc &= (1 << bit_width) - 1
            
        return crc ^ xor_out

    def generate_lfsr_vhdl(self, poly, bit_width, module_name="crc_lfsr"):
        """
        تولید کد خام VHDL برای پیاده‌سازی یک LFSR سریال (Serial CRC)
        استخراج معادلات فیدبک مستقیماً از روی چندجمله‌ای انجام می‌شود.
        """
        poly_bin = f"{poly:0{bit_width}b}"
        
        vhdl_code = f"-- ==========================================\n"
        vhdl_code += f"-- Auto-Generated LFSR VHDL Code\n"
        vhdl_code += f"-- Polynomial: x^{bit_width} + ... (Hex: {hex(poly)})\n"
        vhdl_code += f"-- ==========================================\n\n"
        
        vhdl_code += f"signal lfsr_reg : std_logic_vector({bit_width-1} downto 0) := (others => '0');\n\n"
        vhdl_code += "process(clk, rst)\nbegin\n"
        vhdl_code += "    if rst = '1' then\n"
        vhdl_code += f"        lfsr_reg <= (others => '0');\n"
        vhdl_code += "    elsif rising_edge(clk) then\n"
        vhdl_code += "        if enable = '1' then\n"
        
        # معادله فیدبک اصلی (بیت ورودی XOR با بالاترین بیت)
        vhdl_code += f"            lfsr_reg(0) <= lfsr_reg({bit_width-1}) xor data_in;\n"
        
        # تولید معادلات گیت‌های XOR میانی بر اساس بیت‌های یک در چندجمله‌ای
        for i in range(1, bit_width):
            if poly_bin[bit_width - 1 - i] == '1': 
                vhdl_code += f"            lfsr_reg({i}) <= lfsr_reg({i-1}) xor lfsr_reg({bit_width-1});\n"
            else:
                vhdl_code += f"            lfsr_reg({i}) <= lfsr_reg({i-1});\n"
                
        vhdl_code += "        end if;\n"
        vhdl_code += "    end if;\n"
        vhdl_code += "end process;\n\n"
        
        vhdl_code += f"crc_out <= lfsr_reg; -- Assign to output port\n"
        
        return vhdl_code

# نمونه‌سازی سراسری برای دسترسی در تب‌های برنامه
crc_engine = CRCEngine()
