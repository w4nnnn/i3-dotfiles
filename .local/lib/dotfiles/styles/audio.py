"""
CSS styles for Audio Selector Window.
"""

def get_audio_selector_css(t):
    return f"""
    window {{
        background-color: transparent;
    }}
    #main-card {{
        background-color: {t["bg_rgba"] if "bg_rgba" in t else t["bg"]};
        border: 2px solid {t["accent"]};
        border-radius: 16px;
        padding: 18px 20px;
    }}
    #header-box {{
        padding: 0px 4px 10px 4px;
        border-bottom: 1px solid {t["surface0"]};
        margin-bottom: 4px;
    }}
    #hdr-title {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 13pt;
        font-weight: bold;
    }}
    #hdr-status {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
    }}
    .status-badge-active {{
        background-color: {t["accent"]};
        color: {t["accent_contrast"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
        font-weight: bold;
        border-radius: 999px;
        padding: 3px 10px;
    }}
    #listbox {{
        background-color: transparent;
    }}
    .audio-row {{
        background-color: transparent;
        border: 1.5px solid transparent;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }}
    .audio-row:hover,
    .audio-row:selected {{
        background-color: {t["surface0"]};
        border-color: {t["accent"]};
    }}
    .icon-large {{
        color: {t["accent"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 18pt;
        margin-right: 12px;
    }}
    .row-title {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 10pt;
        font-weight: bold;
    }}
    .row-desc {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
    }}
    .active-pill {{
        background-color: {t["green"]};
        color: {t["accent_contrast"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        font-weight: bold;
        border-radius: 999px;
        padding: 2px 8px;
        margin-right: 8px;
    }}
    .hotkey-badge {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8pt;
        background-color: {t["surface0"]};
        border-radius: 4px;
        padding: 2px 6px;
    }}
    #footer-bar {{
        background-color: {t["surface0"]};
        border-radius: 10px;
        padding: 6px 10px;
        margin-top: 8px;
    }}
    button.footer-action-btn,
    .footer-action-btn {{
        background-color: transparent;
        border: none;
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        border-radius: 6px;
        padding: 4px 10px;
    }}
    button.footer-action-btn:hover,
    .footer-action-btn:hover {{
        background-color: {t["surface1"]};
        color: {t["accent"]};
    }}
    """
