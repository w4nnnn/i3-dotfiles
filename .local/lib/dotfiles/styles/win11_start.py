"""
CSS styles for Windows 11 Start Menu window.
"""

def get_win11_start_css(t):
    bg_card = t.get("bg_rgba", t["bg"])
    bg_inner = t.get("surface0_rgba", t["surface0"])
    bg_footer = t.get("surface0", "#181825")
    muted = t.get("overlay", "#6c7086")
    danger = t.get("red", "#f38ba8")

    return f"""
    window {{
        background-color: transparent;
    }}
    #start-window {{
        background-color: {bg_card};
        border: 2px solid {t["accent"]};
        border-radius: 16px;
        padding: 0px;
    }}
    #search-wrapper {{
        padding: 20px 26px 16px 26px;
        border-bottom: 1px solid {t["surface0"]};
        margin-bottom: 8px;
    }}
    #search-bar {{
        background-color: {bg_inner};
        border: 1px solid {t["surface0"]};
        border-radius: 8px;
        padding: 6px 14px;
        outline: none;
        box-shadow: none;
    }}
    #search-bar:focus-within {{
        border: 1px solid {t["surface1"]};
    }}
    #search-icon {{
        color: {t["accent"]};
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 13pt;
    }}
    entry,
    #search-entry,
    #search-entry:focus {{
        background-color: transparent;
        border: none;
        outline: none;
        box-shadow: none;
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 10.5pt;
    }}
    .close-search-btn {{
        background-color: transparent;
        border: none;
        color: {muted};
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 12pt;
        padding: 0;
        min-width: 24px;
        min-height: 24px;
        border-radius: 6px;
    }}
    .close-search-btn:hover {{
        color: {danger};
        background-color: {t["surface0"]};
    }}
    #body-container {{
        padding: 0px 24px 8px 24px;
    }}
    .app-tile {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 10px 4px;
    }}
    .app-tile:hover {{
        background-color: {t["surface0"]};
        border-color: {t["surface1"]};
    }}
    .app-tile-label {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        margin-top: 5px;
    }}
    .no-results-lbl {{
        color: {muted};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 10pt;
    }}
    #footer-bar {{
        background-color: {bg_footer};
        border-top: 1px solid {t["surface0"]};
        border-radius: 0px 0px 16px 16px;
        padding: 12px 28px;
    }}
    .avatar-circle {{
        background-color: {t["surface0"]};
        border-radius: 50%;
        min-width: 32px;
        min-height: 32px;
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 13pt;
        color: {t["accent"]};
    }}
    .user-name {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 9.5pt;
        font-weight: bold;
        margin-left: 8px;
    }}
    .footer-power-btn {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        min-width: 34px;
        min-height: 34px;
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 14pt;
        color: {danger};
        padding: 0;
    }}
    .footer-power-btn:hover {{
        background-color: {t["surface0"]};
    }}
    scrollbar,
    scrollbar.vertical {{
        background-color: transparent;
        border: none;
    }}
    scrollbar trough {{
        background-color: transparent;
        border: none;
    }}
    scrollbar slider {{
        background-color: {t["surface0"]};
        border-radius: 6px;
        min-width: 4px;
        border: none;
    }}
    scrollbar slider:hover {{
        background-color: {t["accent"]};
    }}
    """
