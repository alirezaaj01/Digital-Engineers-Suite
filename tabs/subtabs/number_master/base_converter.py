"""
Base Converter Subtab
تبدیل آنی بین مبناهای Hex, Bin, Dec
"""
import customtkinter as ctk
from core.validators import validator

class BaseConverterTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_ui()

    def _build_ui(self):
        # بخش ورودی
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(input_frame, text="Input Value:").pack(side="left", padx=5)
        
        self.entry_val = ctk.CTkEntry(input_frame, width=200)
        self.entry_val.pack(side="left", padx=5)
        self.entry_val.bind("<KeyRelease>", self._on_calculate)

        self.combo_base = ctk.CTkComboBox(
            input_frame, 
            values=["Hex", "Decimal", "Binary"],
            command=self._on_calculate,
            width=100
        )
        self.combo_base.pack(side="left", padx=5)
        self.combo_base.set("Hex")

        # بخش نمایش خروجی‌ها
        out_frame = ctk.CTkFrame(self)
        out_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # دیکشنری برای نگهداری لیبل‌های خروجی
        self.outputs = {}
        for base in ["Hex", "Decimal", "Binary"]:
            row = ctk.CTkFrame(out_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(row, text=f"{base}:", width=80, anchor="w").pack(side="left")
            lbl_res = ctk.CTkLabel(row, text="0", anchor="w", font=("Consolas", 14))
            lbl_res.pack(side="left", fill="x", expand=True)
            self.outputs[base] = lbl_res

    def _on_calculate(self, event=None):
        val_str = self.entry_val.get().strip()
        if not val_str:
            self._clear_outputs()
            return

        base_type = self.combo_base.get()
        try:
            # تبدیل به عدد صحیح مبنای 10
            if base_type == "Hex":
                if not validator.is_valid_hex(val_str): raise ValueError
                num = int(val_str, 16)
            elif base_type == "Binary":
                if not validator.is_valid_binary(val_str): raise ValueError
                num = int(val_str, 2)
            else: # Decimal
                num = int(val_str, 10)

            # بروزرسانی رابط کاربری
            self.outputs["Hex"].configure(text=hex(num)[2:].upper())
            self.outputs["Decimal"].configure(text=str(num))
            self.outputs["Binary"].configure(text=bin(num)[2:])
            self.entry_val.configure(border_color="green")
            
        except ValueError:
            self.entry_val.configure(border_color="red")
            self._clear_outputs()

    def _clear_outputs(self):
        for base in self.outputs:
            self.outputs[base].configure(text="---")
