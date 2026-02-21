"""
Professional CRC Hardware Generator Subtab
رابط کاربری تولید خودکار کدهای RTL برای محاسبات CRC و مدیریت خطای داده
"""

import customtkinter as ctk
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات، موتورها و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from engines.crc_engine import crc_engine
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class CRCGenerator(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- ورودی چندجمله‌ای (Polynomial) ---
        ctk.CTkLabel(self, text="Polynomial (Hex):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.poly_entry = DarkEntry(self, placeholder="e.g. 0x04C11DB7 (CRC-32)", validate_type="hex")
        self.poly_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.poly_entry.insert(0, "0x04C11DB7")

        # --- عرض داده (Data Width) ---
        ctk.CTkLabel(self, text="Data Width (Bits):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.width_var = ctk.StringVar(value="32")
        self.width_menu = ctk.CTkOptionMenu(self, values=["8", "16", "32", "64"], variable=self.width_var,
                                           fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"])
        self.width_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # --- مقدار اولیه (Initial Value) ---
        ctk.CTkLabel(self, text="Init Value (Hex):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.init_entry = DarkEntry(self, placeholder="e.g. 0xFFFFFFFF", validate_type="hex")
        self.init_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.init_entry.insert(0, "0xFFFFFFFF")

        # --- دکمه تولید کد ---
        self.gen_btn = ctk.CTkButton(self, text="Generate RTL Logic", command=self._generate,
                                     fg_color=config.UI_THEME["COLORS"]["SUCCESS"],
                                     hover_color=config.UI_THEME["COLORS"]["ACCENT_HOVER"])
        self.gen_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # --- نمایش شماتیک متنی معادلات ---
        self.logic_res = ResultLabel(self, text="---", prefix="Feedback Logic: ")
        self.logic_res.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # --- دکمه‌های کپی کد ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.copy_vhdl = HDLCopyButton(self.button_frame, self._get_vhdl_data, data_type="constant", text="Copy VHDL Logic")
        self.copy_vhdl.pack(side="left", padx=5)
        
        self.copy_verilog = HDLCopyButton(self.button_frame, self._get_verilog_data, data_type="constant", text="Copy Verilog Logic")
        self.copy_verilog.pack(side="left", padx=5)

    def _generate(self):
        """تولید منطق و به‌روزرسانی UI"""
        try:
            poly = int(self.poly_entry.get(), 16)
            width = int(self.width_var.get())
            
            # دریافت اطلاعات از موتور CRC
            logic_str = crc_engine.generate_lfsr_logic(poly, width)
            self.logic_res.update_result(f"Polynomial 0x{poly:X} with {width}-bits")
            
            # ذخیره منطق تولید شده برای استفاده در کپی
            self.current_logic = logic_str
            
        except ValueError:
            self.logic_res.update_result("Error: Invalid Polynomial")

    def _get_vhdl_data(self):
        # این تابع به موتور Snippet وصل می‌شود تا کد کامل تولید کند
        return {"value": self.current_logic, "width": self.width_var.get()}

    def _get_verilog_data(self):
        return {"value": self.current_logic, "width": self.width_var.get()}
