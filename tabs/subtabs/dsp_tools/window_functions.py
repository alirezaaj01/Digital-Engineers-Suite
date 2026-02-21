"""
Professional FIR Filter Designer Subtab
طراحی فیلترهای FIR با استفاده از روش پنجره‌گذاری (Window Method) و تولید ضرایب برای FPGA
"""

import customtkinter as ctk
import numpy as np
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات، موتورها و ویجت‌ها
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import config
from engines.plot_engine import plot_engine
from widgets.dark_entry import DarkEntry
from widgets.result_label import ResultLabel
from widgets.hdl_copy_button import HDLCopyButton

class FIRDesigner(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        """چیدمان المان‌های رابط کاربری"""
        # --- پارامترهای طراحی ---
        # فرکانس نمونه‌برداری (Fs)
        ctk.CTkLabel(self, text="Sampling Freq (Hz):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.fs_entry = DarkEntry(self, placeholder="e.g. 1000", validate_type="float")
        self.fs_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.fs_entry.insert(0, "1000")

        # فرکانس قطع (Fc)
        ctk.CTkLabel(self, text="Cutoff Freq (Hz):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.fc_entry = DarkEntry(self, placeholder="e.g. 100", validate_type="float")
        self.fc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.fc_entry.insert(0, "100")

        # تعداد تپ‌ها (N)
        ctk.CTkLabel(self, text="Number of Taps (N):", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.n_entry = DarkEntry(self, placeholder="e.g. 31", validate_type="int")
        self.n_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.n_entry.insert(0, "31")

        # نوع پنجره (Window Type)
        ctk.CTkLabel(self, text="Window Type:", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"]).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.win_var = ctk.StringVar(value="Hamming")
        self.win_menu = ctk.CTkOptionMenu(self, values=["Rectangular", "Hamming", "Hanning", "Blackman"], 
                                         variable=self.win_var, fg_color=config.UI_THEME["COLORS"]["BG_LIGHT"])
        self.win_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # --- دکمه طراحی و رسم ---
        self.design_btn = ctk.CTkButton(self, text="Design Filter & Plot", command=self._design_filter,
                                        fg_color=config.UI_THEME["COLORS"]["ACCENT"])
        self.design_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # --- دکمه کپی ضرایب ---
        self.copy_btn = HDLCopyButton(self, self._get_coeffs_data, data_type="constant", text="Copy Coefficients (COE/VHDL)")
        self.copy_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # --- محل نمایش نمودار (Placeholder) ---
        self.plot_label = ctk.CTkLabel(self, text="Plot will appear here after design", text_color=config.UI_THEME["COLORS"]["TEXT_SECONDARY"])
        self.plot_label.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def _design_filter(self):
        """محاسبه ضرایب فیلتر FIR به روش پنجره‌گذاری"""
        try:
            fs = float(self.fs_entry.get())
            fc = float(self.fc_entry.get())
            n = int(self.n_entry.get())
            win_name = self.win_var.get().lower()

            if n % 2 == 0: n += 1 # تعداد تپ‌ها را برای فیلترهای متقارن فرد می‌کنیم

            # نرمال‌سازی فرکانس قطع
            omega_c = 2 * np.pi * fc / fs
            m = (n - 1) / 2
            n_indices = np.arange(n) - m
            
            # تابع Sinc برای فیلتر پایین‌گذر ایده‌آل
            h_ideal = np.sinc(2 * fc * n_indices / fs) * (2 * fc / fs)
            
            # اعمال پنجره
            if win_name == "hamming": window = np.hamming(n)
            elif win_name == "hanning": window = np.hanning(n)
            elif win_name == "blackman": window = np.blackman(n)
            else: window = np.ones(n) # Rectangular
            
            self.coeffs = h_ideal * window
            
            # رسم پاسخ فرکانسی (به کمک موتور رسم)
            # در نسخه‌های بعدی، اینجا آبجکت فلوتینگ مت‌پلات‌لیب نمایش داده می‌شود
            print(f"Designed FIR with {n} taps. Max coeff: {max(self.coeffs)}")
            
        except Exception as e:
            print(f"Design Error: {e}")

    def _get_coeffs_data(self):
        """آماده‌سازی ضرایب برای کپی در کلیپ‌بورد"""
        if not hasattr(self, 'coeffs'): return None
        # تبدیل ضرایب به رشته برای پکیج VHDL یا فایل COE
        coeffs_str = ", ".join([f"{c:.10f}" for c in self.coeffs])
        return {"value": coeffs_str, "width": len(self.coeffs)}
