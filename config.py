"""
Digital Engineer's Suite - Global Configuration System
Professional Grade Configuration for HDL, DSP, and UI Engines.
"""

import os
import sys

# =============================================================================
# 1. APPLICATION IDENTITY
# =============================================================================
APP_INFO = {
    "NAME": "Digital Engineer's Suite",
    "VERSION": "5.0.0-PRO",
    "AUTHOR": "Alireza",
    "ORGANIZATION": "Digital Electronics Lab",
    "DESCRIPTION": "Advanced RTL Generation & DSP Optimization Toolkit"
}

# =============================================================================
# 2. UI & EXPERIENCE (Dark Mode Professional)
# =============================================================================
UI_THEME = {
    "COLORS": {
        "BG_MAIN": "#0F0F0F",         # Very Dark (Professional Carbon)
        "BG_SIDEBAR": "#1A1A1A",
        "ACCENT": "#007ACC",          # VSCode Blue
        "ACCENT_HOVER": "#1E90FF",
        "TEXT_PRIMARY": "#E1E1E1",    # High Contrast
        "TEXT_SECONDARY": "#A0A0A0",  # Low Contrast for hints
        "SUCCESS": "#4CAF50",
        "WARNING": "#FF9800",
        "ERROR": "#F44336",
        "HDL_KEYWORD": "#569CD6",     # Syntax highlighting style
        "HDL_COMMENT": "#6A9955"
    },
    "FONTS": {
        "GUI_BASE": ("Segoe UI", 10),
        "CODE_EDITOR": ("Consolas", 11, "normal"),
        "HEADER": ("Segoe UI", 14, "bold")
    },
    "DIMENSIONS": {
        "MIN_WIDTH": 1100,
        "MIN_HEIGHT": 750,
        "SIDEBAR_WIDTH": 220
    }
}

# =============================================================================
# 3. HDL GENERATION STANDARDS
# =============================================================================
HDL_SETTINGS = {
    "DEFAULT_LANG": "VHDL",           # Preferred: VHDL, Optional: Verilog
    "VHDL_STANDARD": "2008",          # 93, 2002, 2008
    "VERILOG_STANDARD": "2001",       # 2001, SystemVerilog
    "INDENT_SIZE": 4,                 # Number of spaces
    "VECTOR_DIRECTION": "downto",     # "downto" (Xilinx style) or "to"
    "USE_IEEE_NUMERIC_STD": True,     # Best practice for VHDL
    "CLOCK_EDGE": "rising",           # rising_edge or falling_edge
    "RESET_TYPE": "async",            # sync or async
    "RESET_LEVEL": '1'                # '1' for Active High, '0' for Active Low
}

# =============================================================================
# 4. DSP & MATHEMATICAL ENGINES (Fixed-Point Logic)
# =============================================================================
DSP_CONFIG = {
    "ROUNDING_MODE": "TRUNCATE",      # Options: TRUNCATE, NEAREST, FLOOR
    "OVERFLOW_MODE": "SATURATE",      # Options: SATURATE, WRAP
    "DEFAULT_Q_FORMAT": "Q1.15",      # Common for 16-bit DSP
    "CORDIC_ITERATIONS": 16,          # Precision for CORDIC engine
    "MAX_BIT_WIDTH": 64,              # Guard against impractical hardware widths
    "PI_APPROX": 3.141592653589793
}

# =============================================================================
# 5. FPGA VENDOR SPECIFIC (Memory & Resources)
# =============================================================================
FPGA_TARGETS = {
    "VENDORS": ["Xilinx", "Intel", "Generic"],
    "BRAM_SIZES_KB": {
        "XILINX_7SERIES": 36,
        "XILINX_ULTRASCALE": 36,
        "INTEL_M9K": 9,
        "INTEL_M20K": 20
    },
    "FILE_EXTENSIONS": {
        "COE": ".coe",                # Xilinx Memory Initialization
        "MIF": ".mif",                # Intel Memory Initialization
        "HEX": ".hex",                # Generic Hex
        "VHD": ".vhd",
        "V": ".v"
    }
}

# =============================================================================
# 6. FILE SYSTEM & PROJECT PATHS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "ROOT": BASE_DIR,
    "CORE": os.path.join(BASE_DIR, "core"),
    "ENGINES": os.path.join(BASE_DIR, "engines"),
    "EXPORTS": os.path.join(BASE_DIR, "exports"),
    "TEMPLATES": os.path.join(BASE_DIR, "resources", "templates"),
    "LOGS": os.path.join(BASE_DIR, "logs"),
    "SETTINGS_FILE": os.path.join(BASE_DIR, "core", "user_settings.json")
}

# Ensure critical directories exist
for path in [PATHS["EXPORTS"], PATHS["LOGS"]]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# =============================================================================
# 7. LOGGING & DEBUGGING
# =============================================================================
LOGGING_CONFIG = {
    "LEVEL": "DEBUG",                 # DEBUG, INFO, WARNING, ERROR
    "ENABLE_CONSOLE_LOG": True,
    "LOG_TO_FILE": True,
    "MAX_LOG_SIZE_MB": 5
}
