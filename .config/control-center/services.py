import os
import re
import socket
import glob
import subprocess
import concurrent.futures
import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib
from config import NIGHT_LIGHT_FILE

# ---------------------------------------------------------
# System Identity & Uptime
# ---------------------------------------------------------
def get_username():
    return os.getenv("USER", "user")

def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "archlinux"

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            up_sec = int(float(f.readline().split()[0]))
        days = up_sec // 86400
        hours = (up_sec % 86400) // 3600
        mins = (up_sec % 3600) // 60
        res = []
        if days > 0:
            res.append(f"{days}d")
        if hours > 0:
            res.append(f"{hours}h")
        res.append(f"{mins}m")
        return " ".join(res)
    except Exception:
        return "Active"

# ---------------------------------------------------------
# Audio Management (PulseAudio / PipeWire via pactl & pamixer)
# ---------------------------------------------------------
def get_volume():
    try:
        out = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
        m = re.search(r'/\s*(\d+)%', out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 50

def get_sink_mute():
    try:
        out = subprocess.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
        return "yes" in out.lower()
    except Exception:
        return False

def set_volume(val):
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{int(val)}%"], stderr=subprocess.DEVNULL)

def toggle_sink_mute():
    subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"], stderr=subprocess.DEVNULL)

def get_mic_volume():
    try:
        out = subprocess.check_output(["pamixer", "--default-source", "--get-volume"], stderr=subprocess.DEVNULL, text=True).strip()
        if out.isdigit():
            return int(out)
    except Exception:
        pass
    try:
        out = subprocess.check_output(["pactl", "get-source-volume", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
        m = re.search(r'/\s*(\d+)%', out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 60

def get_mic_mute():
    try:
        out = subprocess.check_output(["pamixer", "--default-source", "--get-mute"], stderr=subprocess.DEVNULL, text=True).strip()
        return "true" in out.lower()
    except Exception:
        pass
    try:
        out = subprocess.check_output(["pactl", "get-source-mute", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
        return "yes" in out.lower()
    except Exception:
        return False

def set_mic_volume(val):
    val = int(val)
    subprocess.run(["pamixer", "--default-source", "--set-volume", str(val)], stderr=subprocess.DEVNULL)
    subprocess.run(["pactl", "set-source-volume", "@DEFAULT_SOURCE@", f"{val}%"], stderr=subprocess.DEVNULL)

def toggle_mic_mute():
    subprocess.run(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "toggle"], stderr=subprocess.DEVNULL)

def get_initial_audio():
    def get_sv():
        try:
            out = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
            m = re.search(r'/\s*(\d+)%', out)
            return int(m.group(1)) if m else 50
        except Exception:
            return 50

    def get_sm():
        try:
            out = subprocess.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
            return "yes" in out.lower()
        except Exception:
            return False

    def get_mv():
        try:
            out = subprocess.check_output(["pactl", "get-source-volume", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
            m = re.search(r'/\s*(\d+)%', out)
            return int(m.group(1)) if m else 80
        except Exception:
            return 80

    def get_mm():
        try:
            out = subprocess.check_output(["pactl", "get-source-mute", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
            return "yes" in out.lower()
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        f_sv = ex.submit(get_sv)
        f_sm = ex.submit(get_sm)
        f_mv = ex.submit(get_mv)
        f_mm = ex.submit(get_mm)
        return f_sv.result(), f_sm.result(), f_mv.result(), f_mm.result()

# ---------------------------------------------------------
# Display Brightness
# ---------------------------------------------------------
def get_brightness():
    for p in glob.glob("/sys/class/backlight/*"):
        try:
            with open(os.path.join(p, "brightness")) as f:
                curr = int(f.read().strip())
            with open(os.path.join(p, "max_brightness")) as f:
                max_b = int(f.read().strip())
            return round((curr / max_b) * 100)
        except Exception:
            pass
    try:
        out = subprocess.check_output(["brightnessctl", "-m", "info"], stderr=subprocess.DEVNULL, text=True)
        for line in out.strip().split("\n"):
            parts = line.split(",")
            if len(parts) >= 4 and "backlight" in parts[1]:
                return int(parts[3].replace("%", ""))
    except Exception:
        pass
    return 80

def set_brightness(val):
    pct = max(5, min(100, int(val)))
    subprocess.run(["brightnessctl", "set", f"{pct}%"], stderr=subprocess.DEVNULL)

# ---------------------------------------------------------
# Network (Wi-Fi)
# ---------------------------------------------------------
def get_wifi_status():
    for path in glob.glob("/sys/class/rfkill/rfkill*"):
        try:
            with open(os.path.join(path, "type")) as f:
                if f.read().strip() == "wlan":
                    with open(os.path.join(path, "soft")) as sf:
                        s = sf.read().strip() == "1"
                    with open(os.path.join(path, "hard")) as hf:
                        h = hf.read().strip() == "1"
                    return not (s or h)
        except Exception:
            pass
    try:
        out = subprocess.check_output(["nmcli", "radio", "wifi"], stderr=subprocess.DEVNULL, text=True).strip()
        return out.lower() == "enabled"
    except Exception:
        return False

def toggle_wifi():
    is_on = get_wifi_status()
    new_state = "off" if is_on else "on"
    subprocess.run(["nmcli", "radio", "wifi", new_state], stderr=subprocess.DEVNULL)
    return not is_on

# ---------------------------------------------------------
# Bluetooth
# ---------------------------------------------------------
def get_bluetooth_status():
    for path in glob.glob("/sys/class/rfkill/rfkill*"):
        try:
            with open(os.path.join(path, "type")) as f:
                if f.read().strip() == "bluetooth":
                    with open(os.path.join(path, "soft")) as sf:
                        s = sf.read().strip() == "1"
                    with open(os.path.join(path, "hard")) as hf:
                        h = hf.read().strip() == "1"
                    return not (s or h)
        except Exception:
            pass
    try:
        out = subprocess.check_output(["bluetoothctl", "show"], stderr=subprocess.DEVNULL, text=True)
        return "Powered: yes" in out
    except Exception:
        return False

def toggle_bluetooth():
    is_on = get_bluetooth_status()
    cmd = "off" if is_on else "on"
    subprocess.run(["bluetoothctl", "power", cmd], stderr=subprocess.DEVNULL)
    return not is_on

# ---------------------------------------------------------
# Notifications (DND via dunstctl)
# ---------------------------------------------------------
def get_dnd():
    try:
        out = subprocess.check_output(["dunstctl", "is-paused"], stderr=subprocess.DEVNULL, text=True).strip()
        return out.lower() == "true"
    except Exception:
        return False

def toggle_dnd():
    subprocess.run(["dunstctl", "set-paused", "toggle"], stderr=subprocess.DEVNULL)
    return get_dnd()

# ---------------------------------------------------------
# Night Light (Gamma via xrandr)
# ---------------------------------------------------------
def get_connected_outputs():
    try:
        out = subprocess.check_output(["xrandr", "--query"], stderr=subprocess.DEVNULL, text=True)
        outs = []
        for line in out.splitlines():
            if " connected" in line:
                outs.append(line.split()[0])
        return outs if outs else ["eDP-1"]
    except Exception:
        return ["eDP-1"]

def get_night_light():
    if os.path.exists(NIGHT_LIGHT_FILE):
        try:
            with open(NIGHT_LIGHT_FILE) as f:
                return f.read().strip() == "on"
        except Exception:
            pass
    return False

def toggle_night_light():
    is_on = get_night_light()
    outputs = get_connected_outputs()
    if is_on:
        for o in outputs:
            subprocess.run(["xrandr", "--output", o, "--gamma", "1.0:1.0:1.0"], stderr=subprocess.DEVNULL)
        try:
            with open(NIGHT_LIGHT_FILE, "w") as f:
                f.write("off")
        except Exception:
            pass
        return False
    else:
        for o in outputs:
            subprocess.run(["xrandr", "--output", o, "--gamma", "1.0:0.85:0.7"], stderr=subprocess.DEVNULL)
        try:
            with open(NIGHT_LIGHT_FILE, "w") as f:
                f.write("on")
        except Exception:
            pass
        return True

# ---------------------------------------------------------
# Game Mode (Compositor Picom Toggle)
# ---------------------------------------------------------
def get_game_mode():
    try:
        for pid in os.listdir("/proc"):
            if pid.isdigit():
                try:
                    with open(f"/proc/{pid}/comm", "r") as f:
                        if f.read().strip() == "picom":
                            return False
                except Exception:
                    pass
        return True
    except Exception:
        return False

def toggle_game_mode():
    is_game = get_game_mode()
    if is_game:
        subprocess.Popen(["picom", "-b"], stderr=subprocess.DEVNULL)
        return False
    else:
        subprocess.run(["killall", "picom"], stderr=subprocess.DEVNULL)
        return True

# ---------------------------------------------------------
# Power Profiles (D-Bus org.freedesktop.UPower.PowerProfiles)
# ---------------------------------------------------------
def get_power_profile():
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        proxy = Gio.DBusProxy.new_sync(
            bus, Gio.DBusProxyFlags.NONE, None,
            "org.freedesktop.UPower.PowerProfiles",
            "/org/freedesktop/UPower/PowerProfiles",
            "org.freedesktop.DBus.Properties",
            None
        )
        return proxy.Get("(ss)", "org.freedesktop.UPower.PowerProfiles", "ActiveProfile")
    except Exception:
        pass
    try:
        out = subprocess.check_output(["powerprofilesctl", "get"], stderr=subprocess.DEVNULL, text=True).strip()
        return out
    except Exception:
        return "balanced"

def set_power_profile(profile):
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        proxy = Gio.DBusProxy.new_sync(
            bus, Gio.DBusProxyFlags.NONE, None,
            "org.freedesktop.UPower.PowerProfiles",
            "/org/freedesktop/UPower/PowerProfiles",
            "org.freedesktop.DBus.Properties",
            None
        )
        proxy.Set("(ssv)", "org.freedesktop.UPower.PowerProfiles", "ActiveProfile", GLib.Variant.new_string(profile))
    except Exception:
        subprocess.run(["powerprofilesctl", "set", profile], stderr=subprocess.DEVNULL)

# ---------------------------------------------------------
# System Telemetry Helpers (CPU, RAM, Battery, Thermal)
# ---------------------------------------------------------
_prev_idle = 0
_prev_total = 0

def get_cpu_info():
    global _prev_idle, _prev_total
    try:
        with open("/proc/stat") as f:
            fields = [float(x) for x in f.readline().strip().split()[1:]]
        idle = fields[3] + fields[4]
        total = sum(fields)
        if _prev_total > 0:
            d_idle = idle - _prev_idle
            d_total = total - _prev_total
            usage = int((1.0 - d_idle / d_total) * 100) if d_total > 0 else 0
        else:
            usage = 18
        _prev_idle, _prev_total = idle, total
        usage = max(0, min(100, usage))
    except Exception:
        usage = 20

    cpu_brand = "CPU"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    m = line.split(":", 1)[1].strip()
                    if "Intel" in m:
                        cpu_brand = "Intel"
                    elif "AMD" in m:
                        cpu_brand = "AMD"
                    else:
                        cpu_brand = m.split()[0]
                    break
    except Exception:
        pass
    return usage, cpu_brand

def get_ram_info():
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem[parts[0].strip()] = int(parts[1].strip().split()[0])
        total = mem.get("MemTotal", 1) / (1024 * 1024)
        avail = mem.get("MemAvailable", mem.get("MemFree", 0)) / (1024 * 1024)
        used = total - avail
        pct = int((used / total) * 100) if total > 0 else 0
        return f"{used:.1f} GB", pct, used / total
    except Exception:
        return "2.0 GB", 25, 0.25

def get_battery_and_temp():
    bat_cap = 100
    bat_stat = "Full"
    has_bat = False
    ps = "/sys/class/power_supply"
    if os.path.exists(ps):
        for entry in sorted(os.listdir(ps)):
            if entry.startswith("BAT"):
                try:
                    cap_f = os.path.join(ps, entry, "capacity")
                    stat_f = os.path.join(ps, entry, "status")
                    if os.path.exists(cap_f):
                        bat_cap = int(open(cap_f).read().strip())
                        has_bat = True
                    if os.path.exists(stat_f):
                        bat_stat = open(stat_f).read().strip()
                    break
                except Exception:
                    pass

    temp_c = 45
    tz = "/sys/class/thermal"
    if os.path.exists(tz):
        for zone in os.listdir(tz):
            if zone.startswith("thermal_zone"):
                try:
                    t = int(open(os.path.join(tz, zone, "temp")).read().strip()) // 1000
                    if 20 <= t <= 115:
                        temp_c = t
                        break
                except Exception:
                    pass

    return has_bat, bat_cap, bat_stat, temp_c

# ---------------------------------------------------------
# MPRIS Player Helpers
# ---------------------------------------------------------
def get_media_info():
    try:
        status = subprocess.check_output(["playerctl", "status"], stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        status = "Stopped"

    if status in ("Playing", "Paused"):
        try:
            out = subprocess.check_output(
                ["playerctl", "metadata", "--format", "{{playerName}}|{{title}}|{{artist}}|{{mpris:artUrl}}|{{mpris:length}}"],
                stderr=subprocess.DEVNULL, text=True
            ).strip()
            parts = out.split("|")
            player = parts[0] if len(parts) > 0 and parts[0] else "MPRIS"
            title = parts[1] if len(parts) > 1 and parts[1] else "Unknown Title"
            artist = parts[2] if len(parts) > 2 and parts[2] else "Unknown Artist"
            art_url = parts[3] if len(parts) > 3 else ""
            length_us = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
            duration_sec = length_us // 1000000
        except Exception:
            player = "MPRIS"
            title = "Playing"
            artist = ""
            art_url = ""
            duration_sec = 0

        try:
            pos_out = subprocess.check_output(["playerctl", "position"], stderr=subprocess.DEVNULL, text=True).strip()
            pos_sec = int(float(pos_out))
        except Exception:
            pos_sec = 0

        return {
            "status": status,
            "player": player,
            "title": title,
            "artist": artist,
            "art_url": art_url,
            "position": pos_sec,
            "duration": duration_sec
        }

    return {
        "status": "Stopped",
        "player": "MPRIS",
        "title": "No media playing",
        "artist": "Desktop Audio · Idle",
        "art_url": "",
        "position": 0,
        "duration": 0
    }

def format_time(sec):
    sec = max(0, int(sec))
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"
