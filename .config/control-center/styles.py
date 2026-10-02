"""
Dynamic CSS generator for Control Center supporting all desktop themes.
"""

def generate_css(theme):
    t = theme
    return f"""
    window {{
        background-color: transparent;
    }}
    #main-panel {{
        background-color: {t["bg_card"]};
        border: 2px solid {t["border_active"]};
        border-radius: 16px;
        padding: 12px;
        min-width: 380px;
    }}
    .distro-avatar {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        border-radius: 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 14pt;
        font-weight: bold;
        min-width: 32px;
        min-height: 32px;
    }}
    .host-title {{
        color: {t["text_primary"]};
        font-size: 9.5pt;
        font-weight: bold;
        font-family: 'JetBrainsMono Nerd Font';
    }}
    .host-meta {{
        color: {t["text_muted"]};
        font-size: 7.5pt;
        font-family: 'JetBrainsMono Nerd Font';
    }}
    .header-btn {{
        background-color: {t["bg_surface"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border_color"]};
        border-radius: 8px;
        min-width: 30px;
        min-height: 30px;
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 13pt;
        padding: 0;
    }}
    .header-btn:hover {{
        background-color: {t["bg_hover"]};
        color: {t["accent"]};
    }}
    .header-btn.active {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        border-color: {t["accent"]};
    }}
    .header-btn.active:hover {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        opacity: 0.9;
    }}
    .power-btn {{
        background-color: {t["danger_bg"]};
        color: {t["danger"]};
        border-color: transparent;
    }}
    .power-btn:hover {{
        background-color: {t["danger"]};
        color: {t["accent_contrast"]};
    }}

    /* Music Card */
    .music-widget {{
        background-color: {t["bg_surface"]};
        border: 1px solid {t["border_color"]};
        border-radius: 12px;
        padding: 10px;
    }}
    .source-badge {{
        color: {t["accent"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7pt;
        font-weight: bold;
    }}
    .track-title {{
        color: {t["text_primary"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 9.5pt;
        font-weight: bold;
    }}
    .track-artist {{
        color: {t["text_secondary"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
    }}
    .time-label {{
        color: {t["text_muted"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
    }}
    .ctrl-btn {{
        background-color: transparent;
        border: none;
        color: {t["text_primary"]};
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 13pt;
        min-width: 28px;
        min-height: 28px;
        border-radius: 6px;
        padding: 0;
    }}
    .ctrl-btn:hover {{
        background-color: {t["bg_hover"]};
        color: {t["accent"]};
    }}
    .ctrl-btn.active {{
        color: {t["accent"]};
    }}
    .play-btn {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        border: none;
        border-radius: 8px;
        min-width: 32px;
        min-height: 32px;
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 14pt;
        padding: 0;
    }}
    .play-btn:hover {{
        opacity: 0.92;
    }}

    /* Scale / Sliders */
    scale {{
        margin: 0;
        padding: 0;
        min-height: 10px;
    }}
    scale trough {{
        background-color: {t["trough"]};
        border-radius: 999px;
        min-height: 4px;
        margin: 0;
        padding: 0;
    }}
    scale highlight,
    scale trough highlight {{
        background-color: {t["accent"]};
        background-image: none;
        border-radius: 999px;
    }}
    scale slider {{
        background-color: {t["text_primary"]};
        background-image: none;
        border: 2px solid {t["bg_card"]};
        box-shadow: none;
        border-radius: 50%;
        min-width: 10px;
        min-height: 10px;
        margin: -3px 0;
    }}

    /* Sliders Box */
    .sliders-box {{
        background-color: {t["bg_surface"]};
        border: 1px solid {t["border_color"]};
        border-radius: 12px;
        padding: 6px 10px;
    }}
    .slider-row {{
        min-height: 24px;
    }}
    .slider-icon-btn {{
        background-color: transparent;
        border: none;
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 13pt;
        color: {t["accent"]};
        min-width: 24px;
        min-height: 24px;
        padding: 0;
    }}
    .slider-icon-btn:hover {{
        color: {t["text_primary"]};
    }}
    .slider-icon-bright {{
        color: {t["warning"]};
    }}
    .slider-val {{
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
        font-weight: bold;
        color: {t["text_secondary"]};
        min-width: 32px;
    }}

    /* Toggles Grid */
    .toggle-tile {{
        background-color: {t["bg_surface"]};
        border: 1px solid {t["border_color"]};
        border-radius: 8px;
        padding: 5px 2px;
        min-height: 44px;
    }}
    .toggle-tile:hover {{
        background-color: {t["bg_hover"]};
    }}
    .toggle-tile.active {{
        background-color: {t["accent"]};
        border-color: {t["accent"]};
    }}
    .toggle-icon {{
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 15pt;
        color: {t["accent_secondary"]};
    }}
    .toggle-tile.active .toggle-icon {{
        color: {t["accent_contrast"]};
    }}
    .toggle-label {{
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        font-weight: 500;
        color: {t["text_secondary"]};
    }}
    .toggle-tile.active .toggle-label {{
        color: {t["accent_contrast"]};
        font-weight: bold;
    }}

    /* Telemetry Row */
    .stat-badge {{
        background-color: {t["bg_surface"]};
        border: 1px solid {t["border_color"]};
        border-radius: 8px;
        padding: 5px 8px;
    }}
    .stat-name {{
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7pt;
        font-weight: bold;
        color: {t["text_muted"]};
    }}
    .stat-sub {{
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7pt;
        color: {t["text_muted"]};
    }}
    .stat-val {{
        font-family: 'JetBrainsMono Nerd Font', 'lucide';
        font-size: 9.5pt;
        font-weight: bold;
        color: {t["text_primary"]};
    }}

    /* Power Profiles */
    .power-profiles {{
        background-color: {t["bg_surface"]};
        border: 1px solid {t["border_color"]};
        border-radius: 8px;
        padding: 2px;
    }}
    .profile-pill {{
        background-color: transparent;
        border: none;
        color: {t["text_secondary"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
        font-weight: 500;
        border-radius: 6px;
        padding: 3px 6px;
    }}
    .profile-pill:hover {{
        background-color: {t["bg_hover"]};
    }}
    .profile-pill.active {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        font-weight: bold;
    }}

    /* Footer */
    .panel-footer {{
        border-top: 1px solid {t["border_color"]};
        padding-top: 4px;
    }}
    .footer-text {{
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        color: {t["text_muted"]};
    }}
    .footer-btn {{
        background-color: transparent;
        border: none;
        border-radius: 6px;
        box-shadow: none;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.8pt;
        color: {t["accent"]};
        padding: 2px 6px;
        margin: 0;
        min-height: 0;
        font-weight: bold;
    }}
    .footer-btn:hover {{
        background-color: {t["bg_hover"]};
        color: {t["accent"]};
    }}

    /* Theme Dropdown Menu */
    .theme-menu {{
        background-color: {t["bg_card"]};
        border: 1px solid {t["border_color"]};
        border-radius: 10px;
        padding: 4px;
    }}
    .theme-menu menuitem {{
        color: {t["text_primary"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        border-radius: 6px;
        padding: 4px 10px;
    }}
    .theme-menu menuitem:hover {{
        background-color: {t["bg_hover"]};
        color: {t["accent"]};
    }}
    """
