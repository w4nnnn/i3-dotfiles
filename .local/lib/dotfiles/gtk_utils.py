"""
GTK3 window helpers: Single instance management, seat grabbing, positioning, and notifications.
"""
import os
import sys
import signal
import subprocess
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

def manage_single_instance(pid_file):
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                old_pid = int(f.read().strip())
            os.remove(pid_file)
            os.kill(old_pid, signal.SIGTERM)
            sys.exit(0)
        except Exception:
            pass

    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

def cleanup_pid(pid_file):
    if os.path.exists(pid_file):
        try:
            os.remove(pid_file)
        except Exception:
            pass

def grab_seat(window):
    try:
        seat = Gdk.Display.get_default().get_default_seat()
        if seat and window.get_window():
            cursor = window.get_window().get_cursor()
            seat.grab(window.get_window(), Gdk.SeatCapabilities.ALL, True, cursor, None, None)
    except Exception:
        pass
    return False

def ungrab_seat():
    try:
        seat = Gdk.Display.get_default().get_default_seat()
        if seat:
            seat.ungrab()
    except Exception:
        pass

def is_click_outside(window, event):
    if not window.get_window():
        return False
    success, ox, oy = window.get_window().get_origin()
    w = window.get_window().get_width()
    h = window.get_window().get_height()
    return not ((ox <= event.x_root <= ox + w) and (oy <= event.y_root <= oy + h))

def center_window(window, win_w, win_h):
    display = Gdk.Display.get_default()
    monitor = display.get_primary_monitor() or display.get_monitor_at_point(0, 0)
    geom = monitor.get_geometry()
    x = geom.x + (geom.width - win_w) // 2
    y = geom.y + (geom.height - win_h) // 2
    window.move(x, y)

def setup_transparent_window(window):
    window.set_decorated(False)
    window.set_skip_taskbar_hint(True)
    window.set_skip_pager_hint(True)
    window.set_keep_above(True)
    window.set_resizable(False)

    screen = window.get_screen()
    visual = screen.get_rgba_visual()
    if visual:
        window.set_visual(visual)

def notify(app_name, title, message, icon="dialog-information", timeout=2000, tag=None):
    cmd = [
        "dunstify", "-a", app_name,
        "-i", icon,
        "-t", str(timeout),
    ]
    if tag:
        cmd.extend(["-h", f"string:x-dunst-stack-tag:{tag}"])
    cmd.extend([title, message])
    subprocess.Popen(cmd, stderr=subprocess.DEVNULL)
