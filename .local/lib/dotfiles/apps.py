"""
Desktop application scanning and launching utilities using Gio.AppInfo.
"""
import os
import subprocess
import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio

def get_username():
    return os.getenv("USER", "User")

def get_desktop_apps():
    all_apps = Gio.AppInfo.get_all()
    res = []
    seen = set()
    for app in all_apps:
        if app.should_show():
            name = app.get_name()
            if name not in seen:
                seen.add(name)
                res.append(app)
    # Sort alphabetically
    res.sort(key=lambda a: a.get_name().lower())
    return res

def launch_desktop_app(app):
    # Ensure any stale startup notification is removed from environment
    # so applications open on the active workspace instead of workspace 1
    os.environ.pop("DESKTOP_STARTUP_ID", None)
    try:
        app.launch([], None)
    except Exception:
        cmd = app.get_commandline()
        if cmd:
            clean_cmd = [part for part in cmd.split() if not (part.startswith("%") and len(part) == 2)]
            clean_env = os.environ.copy()
            clean_env.pop("DESKTOP_STARTUP_ID", None)
            subprocess.Popen(clean_cmd, env=clean_env)
