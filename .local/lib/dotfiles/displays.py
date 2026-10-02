"""
Display management, multi-monitor configuration via xrandr, and wireless cast hooks.
"""
import os
import shutil
import subprocess
from .gtk_utils import notify

def get_displays_info():
    try:
        out = subprocess.check_output(["xrandr", "--query"], text=True)
    except Exception:
        return None, [], []

    internal = None
    connected_ext = []
    all_outputs = []

    for line in out.splitlines():
        if " connected" in line:
            parts = line.split()
            name = parts[0]
            is_internal = any(name.startswith(p) for p in ["eDP", "LVDS", "DSI"])
            if is_internal and internal is None:
                internal = name
            else:
                connected_ext.append(name)
            all_outputs.append(name)
        elif " disconnected" in line:
            all_outputs.append(line.split()[0])

    if not internal and all_outputs:
        internal = all_outputs[0]
        if internal in connected_ext:
            connected_ext.remove(internal)

    return internal, connected_ext, all_outputs

def is_web_cast_active():
    pid_f = "/tmp/web_screen_share.pid"
    if os.path.exists(pid_f):
        try:
            with open(pid_f, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except Exception:
            pass
    return False

def post_display_hooks():
    polybar_launch = os.path.expanduser("~/.config/polybar/launch.sh")
    if os.path.exists(polybar_launch):
        subprocess.Popen([polybar_launch])
    wall_script = os.path.expanduser("~/.local/bin/wallpaper-selector")
    if os.path.exists(wall_script):
        subprocess.Popen([wall_script, "--restore"])
    elif os.path.exists(os.path.expanduser("~/.cache/current_wallpaper")):
        with open(os.path.expanduser("~/.cache/current_wallpaper")) as f:
            wpath = f.read().strip()
        if os.path.exists(wpath):
            subprocess.Popen(["feh", "--bg-fill", wpath])

def apply_display_mode(mode, internal, connected_ext, all_outputs):
    internal = internal or "eDP-1"
    has_cable = bool(connected_ext)
    ext_target = connected_ext[0] if has_cable else "HDMI-1"

    if mode == "internal":
        cmd = ["xrandr", "--output", internal, "--auto", "--primary"]
        for o in all_outputs:
            if o != internal:
                cmd.extend(["--output", o, "--off"])
        subprocess.run(cmd)
        post_display_hooks()
        notify("Display", "PC Screen Only", "External monitors disconnected.", icon="video-display", tag="display")

    elif mode == "mirror":
        cmd = ["xrandr", "--output", internal, "--auto", "--primary", "--output", ext_target, "--auto", "--same-as", internal]
        subprocess.run(cmd)
        post_display_hooks()
        notify("Display", "Duplicate / Mirror", f"Screen mirrored with {ext_target}.", icon="video-display", tag="display")

    elif mode == "extend_right":
        cmd = ["xrandr", "--output", internal, "--auto", "--primary", "--output", ext_target, "--auto", "--right-of", internal]
        subprocess.run(cmd)
        post_display_hooks()
        notify("Display", "Extended Display", f"Desktop extended to right ({ext_target}).", icon="video-display", tag="display")

    elif mode == "extend_left":
        cmd = ["xrandr", "--output", internal, "--auto", "--primary", "--output", ext_target, "--auto", "--left-of", internal]
        subprocess.run(cmd)
        post_display_hooks()
        notify("Display", "Extended Display", f"Desktop extended to left ({ext_target}).", icon="video-display", tag="display")

    elif mode == "external":
        cmd = ["xrandr", "--output", ext_target, "--auto", "--primary", "--output", internal, "--off"]
        subprocess.run(cmd)
        post_display_hooks()
        notify("Display", "Second Screen Only", f"Displaying exclusively on {ext_target}.", icon="video-display", tag="display")

    elif mode == "web_cast":
        web_bin = os.path.expanduser("~/.local/bin/web-screen-share")
        subprocess.Popen([web_bin, "toggle"])

    elif mode == "miracast":
        if shutil.which("gnome-network-displays"):
            subprocess.Popen(["gnome-network-displays"])
        else:
            notify("Display", "Miracast Tool", "Install GNOME Network Displays via AUR:\nyay -S gnome-network-displays", icon="dialog-information", tag="display")

def launch_arandr():
    if shutil.which("arandr"):
        subprocess.Popen(["arandr"])
    else:
        notify("Display", "ARandR Not Found", "Install with: sudo pacman -S arandr", icon="dialog-information", tag="display")
