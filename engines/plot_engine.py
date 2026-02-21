"""
Professional DSP Plotting Engine
موتور رسم نمودارهای زمان و فرکانس برای تحلیل سیگنال‌های دیجیتال
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# اضافه کردن مسیر ریشه برای دسترسی به تنظیمات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.error_handler import error_handler

class PlotEngine:
    def __init__(self):
        # تنظیم استایل ظاهری مطابق با تم برنامه
        self._apply_dark_theme()

    def _apply_dark_theme(self):
        """تنظیمات بصری Matplotlib برای هماهنگی با تم تاریک"""
        plt.style.use('dark_background')
        plt.rcParams.update({
            'axes.facecolor': config.UI_THEME["COLORS"]["BG_MAIN"],
            'figure.facecolor': config.UI_THEME["COLORS"]["BG_MAIN"],
            'axes.edgecolor': config.UI_THEME["COLORS"]["TEXT_SECONDARY"],
            'grid.color': '#333333',
            'font.family': 'Segoe UI',
            'axes.labelcolor': config.UI_THEME["COLORS"]["TEXT_PRIMARY"],
            'xtick.color': config.UI_THEME["COLORS"]["TEXT_SECONDARY"],
            'ytick.color': config.UI_THEME["COLORS"]["TEXT_SECONDARY"],
            'text.color': config.UI_THEME["COLORS"]["TEXT_PRIMARY"]
        })

    def plot_time_domain(self, signal, title="Time Domain Signal", fs=None):
        """رسم سیگنال در حوزه زمان"""
        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            
            if fs:
                t = np.arange(len(signal)) / fs
                ax.plot(t, signal, color=config.UI_THEME["COLORS"]["ACCENT"], linewidth=1.5)
                ax.set_xlabel("Time (s)")
            else:
                ax.plot(signal, color=config.UI_THEME["COLORS"]["ACCENT"], linewidth=1.5)
                ax.set_xlabel("Sample Index")
                
            ax.set_ylabel("Amplitude")
            ax.set_title(title)
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig
        except Exception as e:
            error_handler.log_error(f"Plotting error: {str(e)}")
            return None

    def plot_fft(self, signal, fs, title="Frequency Spectrum"):
        """محاسبه و رسم تبدیل فوریه سریع (FFT) برای تحلیل طیفی"""
        try:
            n = len(signal)
            freqs = np.fft.fftfreq(n, 1/fs)
            fft_vals = np.abs(np.fft.fft(signal)) / n
            
            # فقط بخش مثبت فرکانس‌ها را نمایش می‌دهیم
            half_n = n // 2
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(freqs[:half_n], 20 * np.log10(fft_vals[:half_n] + 1e-12), 
                    color=config.UI_THEME["COLORS"]["SUCCESS"])
            
            ax.set_title(title)
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Magnitude (dB)")
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig
        except Exception as e:
            error_handler.log_error(f"FFT Plotting error: {str(e)}")
            return None

# ایجاد نمونه سراسری
plot_engine = PlotEngine()
