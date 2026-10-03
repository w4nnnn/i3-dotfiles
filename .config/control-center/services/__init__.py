"""
Control Center Services Package
Re-exports modular hardware and system services.
"""
from .system import (
    get_username,
    get_hostname,
    get_uptime,
    get_cpu_info,
    get_ram_info,
    get_battery_and_temp,
)
from .audio import (
    get_initial_audio,
    get_volume,
    get_sink_mute,
    set_volume,
    toggle_sink_mute,
    toggle_mute,
    get_mic_volume,
    get_mic_mute,
    set_mic_volume,
    toggle_mic_mute,
)
from .brightness import (
    get_brightness,
    set_brightness,
)
from .network import (
    get_wifi_status,
    toggle_wifi,
)
from .bluetooth import (
    get_bluetooth_status,
    toggle_bluetooth,
)
from .power import (
    get_dnd,
    toggle_dnd,
    get_caffeine_status,
    toggle_caffeine,
    turn_off_caffeine,
    get_night_light,
    toggle_night_light,
    get_game_mode,
    toggle_game_mode,
    get_power_profile,
    set_power_profile,
    get_connected_outputs,
)
from .media import (
    get_media_info,
    format_time,
)

__all__ = [
    "get_username",
    "get_hostname",
    "get_uptime",
    "get_cpu_info",
    "get_ram_info",
    "get_battery_and_temp",
    "get_initial_audio",
    "get_volume",
    "get_sink_mute",
    "set_volume",
    "toggle_sink_mute",
    "toggle_mute",
    "get_mic_volume",
    "get_mic_mute",
    "set_mic_volume",
    "toggle_mic_mute",
    "get_brightness",
    "set_brightness",
    "get_wifi_status",
    "toggle_wifi",
    "get_bluetooth_status",
    "toggle_bluetooth",
    "get_dnd",
    "toggle_dnd",
    "get_caffeine_status",
    "toggle_caffeine",
    "turn_off_caffeine",
    "get_night_light",
    "toggle_night_light",
    "get_game_mode",
    "toggle_game_mode",
    "get_power_profile",
    "set_power_profile",
    "get_connected_outputs",
    "get_media_info",
    "format_time",
]
