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
    try:
        app.launch([], None)
    except Exception:
        cmd = app.get_commandline()
        if cmd:
            clean_cmd = [part for part in cmd.split() if not part.startswith("%")]
            subprocess.Popen(clean_cmd)
