"""
CSS styles for Screen Project & Cast Window.
"""
from ..themes import hex_to_rgba

def get_screen_project_css(t):
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
    #header-box {{
        padding: 0px 4px 10px 4px;
        border-bottom: 1px solid {t["surface0"]};
        margin-bottom: 8px;
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
        font-size: 9pt;
    }}
    .status-badge-connected {{
        background-color: {hex_to_rgba(t["green"], 0.18)};
        color: {t["green"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        font-weight: bold;
    }}
    .status-badge-disconnected {{
        background-color: {hex_to_rgba(t["red"], 0.15)};
        color: {t["red"]};
        border-radius: 6px;
        padding: 2px 8px;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
    }}
    #listbox {{
        background-color: transparent;
    }}
    .project-row {{
        background-color: transparent;
        border: 1.5px solid transparent;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }}
    .project-row:hover,
    .project-row:selected {{
        background-color: {t["surface0"]};
        border-color: {t["accent"]};
    }}
    .icon-large {{
        color: {t["accent"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 16pt;
        margin-right: 8px;
    }}
    .row-title {{
        color: {t["fg"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 10.5pt;
        font-weight: bold;
    }}
    .row-desc {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
    }}
    .hotkey-badge {{
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.5pt;
        background-color: {t["surface0"]};
        border-radius: 4px;
        padding: 2px 6px;
    }}
    #footer-bar {{
        background-color: {t["surface0"]};
        border-radius: 10px;
        padding: 6px 10px;
        margin-top: 10px;
    }}
    button.footer-action-btn,
    .footer-action-btn {{
        background-color: transparent;
        border: none;
        border-color: transparent;
        outline: none;
        box-shadow: none;
        border-radius: 8px;
        padding: 5px 10px;
        color: {t["subtext"]};
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 8.8pt;
        font-weight: 500;
    }}
    button.footer-action-btn:focus,
    button.footer-action-btn:hover,
    .footer-action-btn:focus,
    .footer-action-btn:hover {{
        background-color: {t["surface1"]};
        color: {t["accent"]};
        border: none;
        outline: none;
        box-shadow: none;
    }}
    """
