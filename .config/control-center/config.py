import os

# ---------------------------------------------------------
# Themes Configuration
# ---------------------------------------------------------
THEMES = {
    "catppuccin": {
        "name": "Catppuccin Mocha",
        "bg_card": "rgba(30, 30, 46, 0.82)",
        "bg_surface": "#1e1e2e",
        "bg_hover": "#313244",
        "border_color": "rgba(203, 166, 247, 0.20)",
        "border_active": "#cba6f7",
        "text_primary": "#cdd6f4",
        "text_secondary": "#a6adc8",
        "text_muted": "#6c7086",
        "accent": "#cba6f7",
        "accent_rgb": (203 / 255, 166 / 255, 247 / 255),
        "accent_secondary": "#89b4fa",
        "accent_contrast": "#11111b",
        "danger": "#f38ba8",
        "danger_bg": "rgba(243, 139, 168, 0.15)",
        "success": "#a6e3a1",
        "warning": "#f9e2af",
        "trough": "#181825",
        "meter_trough_rgb": (49 / 255, 50 / 255, 68 / 255),
        "cover_grad1": "#4338ca",
        "cover_grad2": "#6d28d9",
    },
    "tokyo-night": {
        "name": "Tokyo Night",
        "bg_card": "rgba(26, 27, 38, 0.94)",
        "bg_surface": "#24283b",
        "bg_hover": "#2f3549",
        "border_color": "rgba(122, 162, 247, 0.22)",
        "border_active": "#7aa2f7",
        "text_primary": "#c0caf5",
        "text_secondary": "#a9b1d6",
        "text_muted": "#565f89",
        "accent": "#7aa2f7",
        "accent_rgb": (122 / 255, 162 / 255, 247 / 255),
        "accent_secondary": "#bb9af7",
        "accent_contrast": "#16161e",
        "danger": "#f7768e",
        "danger_bg": "rgba(247, 118, 142, 0.15)",
        "success": "#9ece6a",
        "warning": "#e0af68",
        "trough": "#1a1b26",
        "meter_trough_rgb": (47 / 255, 53 / 255, 73 / 255),
        "cover_grad1": "#3d59a1",
        "cover_grad2": "#7aa2f7",
    },
    "nord": {
        "name": "Nordic Frost",
        "bg_card": "rgba(46, 52, 64, 0.94)",
        "bg_surface": "#3b4252",
        "bg_hover": "#434c5e",
        "border_color": "rgba(136, 192, 208, 0.22)",
        "border_active": "#88c0d0",
        "text_primary": "#eceff4",
        "text_secondary": "#d8dee9",
        "text_muted": "#4c566a",
        "accent": "#88c0d0",
        "accent_rgb": (136 / 255, 192 / 255, 208 / 255),
        "accent_secondary": "#81a1c1",
        "accent_contrast": "#242933",
        "danger": "#bf616a",
        "danger_bg": "rgba(191, 97, 106, 0.15)",
        "success": "#a3be8c",
        "warning": "#ebcb8b",
        "trough": "#2e3440",
        "meter_trough_rgb": (67 / 255, 76 / 255, 94 / 255),
        "cover_grad1": "#5e81ac",
        "cover_grad2": "#88c0d0",
    },
    "oled": {
        "name": "OLED Pitch Black",
        "bg_card": "rgba(9, 9, 11, 0.97)",
        "bg_surface": "#141418",
        "bg_hover": "#222228",
        "border_color": "rgba(56, 189, 248, 0.25)",
        "border_active": "#38bdf8",
        "text_primary": "#ffffff",
        "text_secondary": "#a1a1aa",
        "text_muted": "#52525b",
        "accent": "#38bdf8",
        "accent_rgb": (56 / 255, 189 / 255, 248 / 255),
        "accent_secondary": "#34d399",
        "accent_contrast": "#000000",
        "danger": "#f43f5e",
        "danger_bg": "rgba(244, 63, 94, 0.15)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "trough": "#0a0a0c",
        "meter_trough_rgb": (34 / 255, 34 / 255, 40 / 255),
        "cover_grad1": "#0284c7",
        "cover_grad2": "#38bdf8",
    },
    "light": {
        "name": "Paper Light",
        "bg_card": "rgba(255, 255, 255, 0.96)",
        "bg_surface": "#f8fafc",
        "bg_hover": "#e2e8f0",
        "border_color": "rgba(15, 23, 42, 0.12)",
        "border_active": "#0284c7",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_muted": "#94a3b8",
        "accent": "#0284c7",
        "accent_rgb": (2 / 255, 132 / 255, 199 / 255),
        "accent_secondary": "#6366f1",
        "accent_contrast": "#ffffff",
        "danger": "#ef4444",
        "danger_bg": "rgba(239, 68, 68, 0.15)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "trough": "#cbd5e1",
        "meter_trough_rgb": (226 / 255, 232 / 255, 240 / 255),
        "cover_grad1": "#0284c7",
        "cover_grad2": "#6366f1",
    }
}

THEME_PREF_FILE = os.path.expanduser("~/.config/control-center-theme")
NIGHT_LIGHT_FILE = "/tmp/nightlight_state"
PID_FILE = "/tmp/catppuccin_control_center.pid"

def load_saved_theme():
    if os.path.exists(THEME_PREF_FILE):
        try:
            with open(THEME_PREF_FILE) as f:
                th = f.read().strip()
                if th in THEMES:
                    return th
        except Exception:
            pass
    return "catppuccin"

def save_theme(theme_name):
    try:
        os.makedirs(os.path.dirname(THEME_PREF_FILE), exist_ok=True)
        with open(THEME_PREF_FILE, "w") as f:
            f.write(theme_name)
    except Exception:
        pass

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 6:
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return (0.5, 0.5, 0.5)
