"""
Power management, display filters, compositor toggles, and notification services.
"""
import os
import signal
import subprocess
import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib
from config import NIGHT_LIGHT_FILE

CAFFEINE_STATE_FILE = "/tmp/caffeine_mode.state"
CAFFEINE_PID_FILE = "/tmp/caffeine_inhibitor.pid"

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
# Caffeine Mode (Keep Screen Awake & Anti-Sleep)
# ---------------------------------------------------------
def get_caffeine_status():
    if os.path.exists(CAFFEINE_STATE_FILE):
        try:
            with open(CAFFEINE_STATE_FILE, "r") as f:
                return f.read().strip() == "on"
        except Exception:
            pass
    return False

def turn_off_caffeine(notify=True):
    subprocess.run(["xset", "s", "on", "+dpms"], stderr=subprocess.DEVNULL)
    if os.path.exists(CAFFEINE_PID_FILE):
        try:
            with open(CAFFEINE_PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
        try:
            os.remove(CAFFEINE_PID_FILE)
        except Exception:
            pass
    try:
        with open(CAFFEINE_STATE_FILE, "w") as f:
            f.write("off")
    except Exception:
        pass

    if notify:
        subprocess.Popen([
            "dunstify", "-a", "Caffeine",
            "-h", "string:x-dunst-stack-tag:caffeine",
            "-i", "caffeine",
            "-t", "2000", "-u", "low",
            "☕ Caffeine Disabled", "Normal screen sleep & auto-lock restored."
        ], stderr=subprocess.DEVNULL)
    return False

def toggle_caffeine():
    is_on = get_caffeine_status()
    if is_on:
        return turn_off_caffeine(notify=True)
    else:
        subprocess.run(["xset", "s", "off", "-dpms"], stderr=subprocess.DEVNULL)
        try:
            p = subprocess.Popen([
                "systemd-inhibit",
                "--what=idle:sleep",
                "--who=Caffeine",
                "--why=Caffeine Mode Active",
                "sleep", "infinity"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(CAFFEINE_PID_FILE, "w") as f:
                f.write(str(p.pid))
        except Exception:
            pass

        try:
            with open(CAFFEINE_STATE_FILE, "w") as f:
                f.write("on")
        except Exception:
            pass

        subprocess.Popen([
            "dunstify", "-a", "Caffeine",
            "-h", "string:x-dunst-stack-tag:caffeine",
            "-i", "caffeine",
            "-t", "2000", "-u", "low",
            "☕ Caffeine Active", "Screen sleep & auto-lock disabled."
        ], stderr=subprocess.DEVNULL)
        return True

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
