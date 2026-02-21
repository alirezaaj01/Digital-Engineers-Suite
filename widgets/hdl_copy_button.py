"""
HDL Copy Button Widget
دکمه هوشمند برای تولید و کپی کردن کدهای HDL به کلیپ‌بورد با یک کلیک
"""
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.hdl_snippet_generator import HDLSnippetGenerator

class HDLCopyButton(ctk.CTkButton):
    def __init__(self, master, get_value_cb, get_width_cb, default_name="MY_CONST", **kwargs):
        """
        get_value_cb: تابعی که مقدار هگزادسیمال را برمی‌گرداند
        get_width_cb: تابعی که عرض بیت را برمی‌گرداند
        """
        super().__init__(
            master,
            text="Copy as HDL",
            command=self._copy_to_clipboard,
            fg_color=config.UI_THEME["COLORS"]["SUCCESS"],
            hover_color=config.UI_THEME["COLORS"]["ACCENT_HOVER"],
            text_color=config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            font=config.UI_THEME["FONTS"]["GUI_BASE"],
            corner_radius=6,
            **kwargs
        )
        self.get_value_cb = get_value_cb
        self.get_width_cb = get_width_cb
        self.default_name = default_name

    def _copy_to_clipboard(self):
        try:
            val = self.get_value_cb()
            width = self.get_width_cb()
            
            if not val or not width:
                self._show_status("Empty Data!", is_error=True)
                return

            snippet = HDLSnippetGenerator.generate_constant(
                name=self.default_name,
                value=val,
                width=int(width)
            )

            # استفاده از سیستم کلیپ‌بورد خود تکینتر (Tkinter)
            self.clipboard_clear()
            self.clipboard_append(snippet)
            self.update() # جلوگیری از پاک شدن سریع کلیپ‌بورد در لینوکس/مک
            
            self._show_status("Copied HDL!")
        except Exception as e:
            self._show_status("Error!", is_error=True)

    def _show_status(self, msg, is_error=False):
        """نمایش موقت پیام روی دکمه"""
        original_text = self.cget("text")
        original_color = self.cget("fg_color")
        
        err_color = config.UI_THEME["COLORS"]["ERROR"]
        succ_color = config.UI_THEME["COLORS"]["SUCCESS"]
        
        self.configure(text=msg, fg_color=err_color if is_error else succ_color)
        self.after(1500, lambda: self.configure(text=original_text, fg_color=original_color))
