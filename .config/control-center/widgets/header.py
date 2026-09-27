import os
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from services import get_username, get_hostname, get_uptime

class HeaderWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.window = window
        self._build_ui()

    def _build_ui(self):
        # Distro avatar (32x32, Arch icon)
        avatar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        avatar.get_style_context().add_class("distro-avatar")
        avatar_lbl = Gtk.Label(label="󰣇")
        avatar_lbl.set_halign(Gtk.Align.CENTER)
        avatar_lbl.set_valign(Gtk.Align.CENTER)
        avatar.pack_start(avatar_lbl, True, True, 0)
        self.pack_start(avatar, False, False, 0)

        # Host info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        info_box.set_valign(Gtk.Align.CENTER)
        host_title = Gtk.Label(label=f"{get_username()}@{get_hostname()}", xalign=0)
        host_title.get_style_context().add_class("host-title")
        self.host_meta_lbl = Gtk.Label(label=f"X11 · Up {get_uptime()}", xalign=0)
        self.host_meta_lbl.get_style_context().add_class("host-meta")
        info_box.pack_start(host_title, False, False, 0)
        info_box.pack_start(self.host_meta_lbl, False, False, 0)
        self.pack_start(info_box, True, True, 0)

        # Header actions
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        bin_dir = os.path.expanduser("~/.local/bin")

        # Lock button
        lock_btn = Gtk.Button(label="󰌾")
        lock_btn.get_style_context().add_class("header-btn")
        if lock_btn.get_child():
            lock_btn.get_child().set_halign(Gtk.Align.CENTER)
            lock_btn.get_child().set_valign(Gtk.Align.CENTER)
        lock_btn.set_tooltip_text("Lock Screen")
        lock_btn.connect("clicked", lambda w: (self.window.close_and_exit(), subprocess.Popen([os.path.join(bin_dir, "lockscreen")])))
        actions_box.pack_start(lock_btn, False, False, 0)

        # Power button
        power_btn = Gtk.Button(label="󰐥")
        power_btn.get_style_context().add_class("header-btn")
        power_btn.get_style_context().add_class("power-btn")
        if power_btn.get_child():
            power_btn.get_child().set_halign(Gtk.Align.CENTER)
            power_btn.get_child().set_valign(Gtk.Align.CENTER)
        power_btn.set_tooltip_text("Power Menu")
        power_btn.connect("clicked", lambda w: (self.window.close_and_exit(), subprocess.Popen([os.path.join(bin_dir, "powermenu")])))
        actions_box.pack_start(power_btn, False, False, 0)

        self.pack_start(actions_box, False, False, 0)

    def update_uptime(self):
        self.host_meta_lbl.set_text(f"X11 · Up {get_uptime()}")
