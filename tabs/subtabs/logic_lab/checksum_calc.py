"""
Professional Checksum Calculator Subtab
محاسبه‌گر چک‌سام‌های مهندسی و تولید منطق سخت‌افزاری برای تایید صحت داده‌ها
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class ChecksumCalc(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- ورودی جریان داده (Data Stream) ---
        ctk.CTkLabel(self, text="Data Stream (Hex):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.data_entry = DarkEntry(self, placeholder="e.g. AA 55 01 02", validate_type=None)
        self.data_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- انتخاب نوع چک‌سام ---
        ctk.CTkLabel(self, text="Checksum Type:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.type_var = ctk.StringVar(value="Additive (Sum)")
        self.type_menu = ctk.CTkOptionMenu(
            self, values=["Additive (Sum)", "XOR-based", "Two's Complement Sum"], 
            variable=self.type_var,
            fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"],
            button_color=config.UI_THEME["COLORS"]["ACCENT"]
        )
        self.type_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # --- عرض بیت (Bit Width) ---
        ctk.CTkLabel(self, text="Result Width:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.width_var = ctk.StringVar(value="8")
        self.width_menu = ctk.CTkOptionMenu(self, values=["8", "16", "32"], variable=self.width_var,
                                           fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"])
        self.width_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # --- دکمه محاسبه ---
        self.calc_btn = ctk.CTkButton(
            self, text="Calculate Checksum", command=self._calculate,
            fg_color=config.UI_THEME["COLORS"]["SUCCESS"]
        )
        self.calc_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # --- نمایش نتیجه ---
        self.res_label = ResultLabel(self, text="---", prefix="Result (Hex): ")
        self.res_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # --- دکمه کپی کد HDL ---
        self.copy_btn = HDLCopyButton(self, self._get_hdl_code, data_type="constant", text="Copy Checksum Logic")
        self.copy_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

    def _calculate(self):
        """الگوریتم محاسبه چک‌سام"""
        try:
            raw_data = self.data_entry.get().strip().replace(" ", "")
            if not raw_data: return

            # تبدیل استریم هگز به لیست اعداد
            bytes_data = [int(raw_data[i:i+2], 16) for i in range(0, len(raw_data), 2)]
            
            width = int(self.width_var.get())
            mask = (1 << width) - 1
            mode = self.type_var.get()

            result = 0
            if mode == "Additive (Sum)":
                result = sum(bytes_data) & mask
            elif mode == "XOR-based":
                for b in bytes_data:
                    result ^= b
                result &= mask
            elif mode == "Two's Complement Sum":
                result = (-(sum(bytes_data))) & mask

            self.res_label.update_result(f"{result:0{width//4}X}")
            self.current_result = result

        except Exception:
            self.res_label.update_result("Error: Invalid Hex Data")

    def _get_hdl_code(self):
        """تولید تکه کد VHDL/Verilog برای پیاده‌سازی چک‌سام"""
        mode = self.type_var.get()
        width = self.width_var.get()
        
        if "XOR" in mode:
            logic = f"checksum_out <= data_in_1 xor data_in_2; -- XOR {width}-bit"
        else:
            logic = f"checksum_out <= std_logic_vector(unsigned(sum_reg) + unsigned(data_in)); -- Additive {width}-bit"
            
        return {"value": logic, "width": width}
