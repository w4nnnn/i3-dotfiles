"""
Dotfiles shared Python library.
"""
from .themes import (
    THEMES,
    get_current_theme_key,
    get_current_theme,
    hex_to_rgba,
    hex_to_rgb_float,
)
from .gtk_utils import (
    manage_single_instance,
    cleanup_pid,
    grab_seat,
    ungrab_seat,
    is_click_outside,
    center_window,
    setup_transparent_window,
    notify,
)
from .theme_sync import apply_global_theme
from .audio import play_test_chime, get_audio_outputs, set_audio_output
from .displays import get_displays_info, is_web_cast_active, apply_display_mode, launch_arandr
from .apps import get_username, get_desktop_apps, launch_desktop_app
from .bluetooth import (
    get_device_icon,
    fetch_bluetooth_state,
    connect_device,
    pair_device,
    disconnect_device,
    set_adapter_discovery,
    set_adapter_power,
)
from .network import (
    scan_networks,
    connect_saved_or_open,
    connect_with_password,
    disconnect_active,
    toggle_wifi_radio,
    open_captive_portal,
)

__all__ = [
    "THEMES",
    "get_current_theme_key",
    "get_current_theme",
    "manage_single_instance",
    "cleanup_pid",
    "grab_seat",
    "ungrab_seat",
    "is_click_outside",
    "center_window",
    "setup_transparent_window",
    "notify",
    "apply_global_theme",
    "play_test_chime",
    "get_audio_outputs",
    "set_audio_output",
    "get_displays_info",
    "is_web_cast_active",
    "apply_display_mode",
    "launch_arandr",
    "get_username",
    "get_desktop_apps",
    "launch_desktop_app",
    "get_device_icon",
    "fetch_bluetooth_state",
    "connect_device",
    "pair_device",
    "disconnect_device",
    "set_adapter_discovery",
    "set_adapter_power",
    "scan_networks",
    "connect_saved_or_open",
    "connect_with_password",
    "disconnect_active",
    "toggle_wifi_radio",
    "open_captive_portal",
]
