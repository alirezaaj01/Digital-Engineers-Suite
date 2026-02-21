"""
BRAM / Block Memory Calculator Engine
محاسبه و تخمین تعداد بلوک‌های حافظه مورد نیاز برای Xilinx و Intel
"""
import math

class BRAMEngine:
    def __init__(self):
        # مشخصات بلوک‌های حافظه استاندارد
        # ظرفیت‌ها به بیت و حداکثر عرض مجاز داده در یک بلوک مشخص شده است
        self.bram_configs = {
            "Xilinx_18Kb": {"capacity": 18432, "max_width": 36},
            "Xilinx_36Kb": {"capacity": 36864, "max_width": 72},
            "Intel_M9K":   {"capacity": 9216,  "max_width": 36},
            "Intel_M20K":  {"capacity": 20480, "max_width": 40},
            "Generic_URAM": {"capacity": 294912, "max_width": 72} # UltraRAM
        }

    def get_supported_architectures(self):
        """دریافت لیست معماری‌های پشتیبانی‌شده"""
        return list(self.bram_configs.keys())

    def calculate_bram_usage(self, target_width, target_depth, architecture="Xilinx_36Kb"):
        """
        محاسبه تعداد BRAM های مورد نیاز بر اساس ماتریس Cascading (گسترش عمق و عرض)
        """
        if architecture not in self.bram_configs:
            raise ValueError(f"Architecture '{architecture}' is not supported.")

        config = self.bram_configs[architecture]
        bram_capacity = config["capacity"]
        max_bram_width = config["max_width"]

        total_target_bits = target_width * target_depth

        # گام اول: بررسی گسترش افقی (نیاز به چند BRAM برای تامین عرض باس؟)
        brams_for_width = math.ceil(target_width / max_bram_width)
        
        # محاسبه عمق قابل تامین توسط یک ردیف BRAM با این عرض
        # هر BRAM وقتی در حداکثر عرض استفاده شود، عمق مشخصی دارد
        effective_depth_per_bram = bram_capacity // max_bram_width
        
        # گام دوم: بررسی گسترش عمودی (نیاز به چند ردیف برای تامین عمق؟)
        brams_for_depth = math.ceil(target_depth / effective_depth_per_bram)

        # کل BRAM های مورد نیاز
        total_brams_needed = brams_for_width * brams_for_depth
        
        # محاسبه بهره‌وری (Efficiency)
        total_allocated_bits = total_brams_needed * bram_capacity
        utilization_percent = (total_target_bits / total_allocated_bits) * 100 if total_allocated_bits > 0 else 0

        # محاسبه هدررفت حافظه (Wastage)
        wasted_bits = total_allocated_bits - total_target_bits

        return {
            "total_brams": total_brams_needed,
            "brams_cascade_width": brams_for_width,
            "brams_cascade_depth": brams_for_depth,
            "total_target_bits": total_target_bits,
            "total_allocated_bits": total_allocated_bits,
            "wasted_bits": wasted_bits,
            "utilization_percent": round(utilization_percent, 2),
            "architecture_used": architecture
        }

    def suggest_optimal_architecture(self, target_width, target_depth):
        """
        پیشنهاد بهترین نوع BRAM برای کمترین هدررفت حافظه
        """
        best_arch = None
        best_utilization = -1
        results = {}

        for arch in self.bram_configs.keys():
            res = self.calculate_bram_usage(target_width, target_depth, arch)
            results[arch] = res
            if res["utilization_percent"] > best_utilization:
                best_utilization = res["utilization_percent"]
                best_arch = arch

        return {
            "recommended": best_arch,
            "highest_efficiency": best_utilization,
            "all_results": results
        }

# نمونه‌سازی سراسری
bram_engine = BRAMEngine()
