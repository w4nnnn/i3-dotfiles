"""
CSS styles for Bluetooth Manager Menu.
"""
from ..themes import hex_to_rgba

def get_bluetooth_css(t):
    contrast = t.get("accent_contrast", "#11111b")
    return f"""
    window {{
        background-color: transparent;
    }}
    #main-card {{
        background-color: {t["bg_rgba"] if "bg_rgba" in t else t["bg"]};
        border: 2px solid {t["accent"]};
        border-radius: 16px;
        padding: 20px;
    }}
    #inputbar {{
        background-color: {t["surface0"]};
        border-radius: 12px;
        padding: 8px 14px;
    }}
    #prompt-icon {{
        color: {t["accent"]};
        font-family: 'lucide', 'JetBrainsMono Nerd Font';
        font-size: 14pt;
        margin-right: 6px;
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
        font-size: 10pt;
    }}
    #listbox {{
        background-color: transparent;
    }}
    .element-row {{
        background-color: transparent;
        border: 1.5px solid transparent;
        border-radius: 10px;
        padding: 6px 12px;
        margin-bottom: 2px;
    }}
    .element-row:hover,
    .element-row:selected {{
        background-color: {t["surface0"]};
        border-color: {t["accent"]};
    }}
    .element-row.connected {{
        border-left: 3px solid {t["green"]};
    }}
    .element-icon {{
        color: {t["accent"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 15pt;
        margin-right: 8px;
    }}
    .element-text {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 9.5pt;
    }}
    .element-sub {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
    }}
    .badge-connected {{
        background-color: {hex_to_rgba(t["green"], 0.18)};
        color: {t["green"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        font-weight: bold;
    }}
    .badge-paired {{
        background-color: {hex_to_rgba(t["blue"], 0.15)};
        color: {t["blue"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
    }}
    .badge-battery {{
        background-color: {hex_to_rgba(t["yellow"], 0.15)};
        color: {t["yellow"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        font-weight: bold;
    }}
    .badge-rssi {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 7.5pt;
        padding: 2px 4px;
    }}
    #footer-bar {{
        background-color: {t["surface0"]};
        border-radius: 10px;
        padding: 6px 10px;
        margin-top: 6px;
    }}
    button.footer-action-btn,
    .footer-action-btn {{
        background-color: transparent;
        border: none;
        border-color: transparent;
        outline: none;
        box-shadow: none;
        border-radius: 8px;
        padding: 5px 8px;
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        font-weight: 500;
    }}
    button.footer-action-btn:focus,
    button.footer-action-btn:hover,
    .footer-action-btn:focus,
    .footer-action-btn:hover {{
        background-color: {t["surface1"]};
        color: {t["accent"]};
    }}
    .footer-action-btn.danger {{
        color: {t["red"]};
    }}
    button.footer-action-btn.danger:hover,
    .footer-action-btn.danger:hover {{
        background-color: {t["red"]};
        color: {contrast};
    }}
    .footer-action-btn.rescan {{
        color: {t["accent"]};
    }}
    button.footer-action-btn.rescan:hover,
    .footer-action-btn.rescan:hover {{
        background-color: {t["accent"]};
        color: {contrast};
    }}
    .footer-action-btn.terminal {{
        color: {t["yellow"]};
    }}
    button.footer-action-btn.terminal:hover,
    .footer-action-btn.terminal:hover {{
        background-color: {t["yellow"]};
        color: {contrast};
    }}
    .footer-action-btn.radio {{
        color: {t["green"]};
    }}
    button.footer-action-btn.radio:hover,
    .footer-action-btn.radio:hover {{
        background-color: {t["green"]};
        color: {contrast};
    }}
    scrollbar trough {{
        background-color: transparent;
    }}
    scrollbar slider {{
        background-color: {t["surface0"]};
        border-radius: 6px;
        min-width: 4px;
    }}
    scrollbar slider:hover {{
        background-color: {t["accent"]};
    }}
    """
