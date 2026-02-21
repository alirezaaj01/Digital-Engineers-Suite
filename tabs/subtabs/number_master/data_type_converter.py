"""
Data Type Converter Subtab
نمایش و تبدیل اعداد با در نظر گرفتن علامت و مکمل دو
"""
import customtkinter as ctk

class DataTypeConverterTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_ui()

    def _build_ui(self):
        # بخش تنظیمات ورودی
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(top_frame, text="Value (Decimal):").pack(side="left", padx=5)
        self.entry_val = ctk.CTkEntry(top_frame, width=150)
        self.entry_val.pack(side="left", padx=5)
        self.entry_val.bind("<KeyRelease>", self._calculate)

        ctk.CTkLabel(top_frame, text="Bit Width:").pack(side="left", padx=(20, 5))
        self.combo_width = ctk.CTkComboBox(
            top_frame, 
            values=["8", "16", "32", "64"], 
            width=80,
            command=self._calculate
        )
        self.combo_width.pack(side="left")
        self.combo_width.set("16")

        # بخش نمایش نتایج
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.lbl_unsigned = self._add_result_row(res_frame, "Unsigned:")
        self.lbl_signed = self._add_result_row(res_frame, "Signed (2's Comp):")
        self.lbl_hex = self._add_result_row(res_frame, "Hexadecimal:")
        self.lbl_bin = self._add_result_row(res_frame, "Binary:")

    def _add_result_row(self, parent, title):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=8, padx=10)
        ctk.CTkLabel(row, text=title, width=150, anchor="w").pack(side="left")
        lbl = ctk.CTkLabel(row, text="---", anchor="w", font=("Consolas", 14))
        lbl.pack(side="left", fill="x", expand=True)
        return lbl

    def _calculate(self, event=None):
        val_str = self.entry_val.get().strip()
        if not val_str:
            self._clear_labels()
            return
            
        try:
            val = int(val_str)
            width = int(self.combo_width.get())
            max_unsigned = (1 << width) - 1
            min_signed = -(1 << (width - 1))
            max_signed = (1 << (width - 1)) - 1

            # ماسک کردن برای استخراج بیت‌ها
            val_masked = val & max_unsigned

            # محاسبه Unsigned
            unsigned_val = val_masked
            
            # محاسبه Signed
            if val_masked > max_signed:
                signed_val = val_masked - (1 << width)
            else:
                signed_val = val_masked

            # نمایش
            self.lbl_unsigned.configure(text=str(unsigned_val))
            self.lbl_signed.configure(text=str(signed_val))
            
            hex_str = hex(val_masked)[2:].upper().zfill(width // 4)
            self.lbl_hex.configure(text=f"0x{hex_str}")
            
            bin_str = bin(val_masked)[2:].zfill(width)
            formatted_bin = " ".join([bin_str[i:i+4] for i in range(0, len(bin_str), 4)])
            self.lbl_bin.configure(text=formatted_bin)
            
            self.entry_val.configure(border_color="green")
        except ValueError:
            self.entry_val.configure(border_color="red")
            self._clear_labels()

    def _clear_labels(self):
        for lbl in [self.lbl_unsigned, self.lbl_signed, self.lbl_hex, self.lbl_bin]:
            lbl.configure(text="---")
