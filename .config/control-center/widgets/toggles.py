import os
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from services import (
    get_wifi_status,
    toggle_wifi,
    get_bluetooth_status,
    toggle_bluetooth,
    get_dnd,
    toggle_dnd,
    get_night_light,
    toggle_night_light,
    get_game_mode,
    toggle_game_mode,
)

class TogglesWidget(Gtk.Grid):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_column_spacing(6)
        self.set_row_spacing(6)
        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self._build_ui()

    def _build_ui(self):
        # 1. Wi-Fi
        is_wifi = get_wifi_status()
        self.wifi_btn, self.wifi_icon_lbl = self.make_toggle_tile("" if is_wifi else "", "Wi-Fi", is_wifi)
        self.wifi_btn.connect("button-press-event", self.on_wifi_press)
        self.attach(self.wifi_btn, 0, 0, 1, 1)

        # 2. Bluetooth
        is_bt = get_bluetooth_status()
        self.bt_btn, self.bt_icon_lbl = self.make_toggle_tile("" if is_bt else "", "Bluetooth", is_bt)
        self.bt_btn.connect("clicked", self.on_bluetooth_clicked)
        self.attach(self.bt_btn, 1, 0, 1, 1)

        # 3. DND
        is_dnd = get_dnd()
        self.dnd_btn, self.dnd_icon_lbl = self.make_toggle_tile("" if is_dnd else "", "DND", is_dnd)
        self.dnd_btn.connect("clicked", self.on_dnd_clicked)
        self.attach(self.dnd_btn, 2, 0, 1, 1)

        # 4. Night Light
        is_night = get_night_light()
        self.night_btn, self.night_icon_lbl = self.make_toggle_tile("", "Night Light", is_night)
        self.night_btn.connect("clicked", self.on_night_clicked)
        self.attach(self.night_btn, 3, 0, 1, 1)

        # 5. Game Mode
        is_game = get_game_mode()
        self.game_btn, self.game_icon_lbl = self.make_toggle_tile("", "Game Mode", is_game)
        self.game_btn.connect("clicked", self.on_game_clicked)
        self.attach(self.game_btn, 0, 1, 1, 1)

        # 6. Project
        bin_dir = os.path.expanduser("~/.local/bin")
        self.project_btn, _ = self.make_toggle_tile("󰍹", "Project", False)
        self.project_btn.connect(
            "clicked",
            lambda w: (
                self.window.close_and_exit(),
                subprocess.Popen([os.path.join(bin_dir, "screen-project")]),
            ),
        )
        self.attach(self.project_btn, 1, 1, 1, 1)

        # 7. Screenshot
        sc_btn, _ = self.make_toggle_tile("", "Screenshot", False)
        sc_btn.connect(
            "clicked",
            lambda w: (
                self.window.hide(),
                GLib.timeout_add(
                    150,
                    lambda: (
                        subprocess.Popen([os.path.join(bin_dir, "screenshot"), "select"]),
                        self.window.close_and_exit(),
                    ),
                ),
            ),
        )
        self.attach(sc_btn, 2, 1, 1, 1)

        # 8. Wallpaper
        wall_btn, _ = self.make_toggle_tile("", "Wallpaper", False)
        wall_btn.connect(
            "clicked",
            lambda w: (
                self.window.close_and_exit(),
                subprocess.Popen([os.path.join(bin_dir, "wallpaper-selector")]),
            ),
        )
        self.attach(wall_btn, 3, 1, 1, 1)

    def make_toggle_tile(self, icon, label, is_active=False):
        btn = Gtk.Button()
        btn.get_style_context().add_class("toggle-tile")
        if is_active:
            btn.get_style_context().add_class("active")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_halign(Gtk.Align.CENTER)

        icon_lbl = Gtk.Label(label=icon)
        icon_lbl.get_style_context().add_class("toggle-icon")
        icon_lbl.set_halign(Gtk.Align.CENTER)
        icon_lbl.set_valign(Gtk.Align.CENTER)
        icon_lbl.set_xalign(0.5)
        icon_lbl.set_yalign(0.5)
        vbox.pack_start(icon_lbl, False, False, 0)

        text_lbl = Gtk.Label(label=label)
        text_lbl.get_style_context().add_class("toggle-label")
        text_lbl.set_halign(Gtk.Align.CENTER)
        text_lbl.set_valign(Gtk.Align.CENTER)
        text_lbl.set_xalign(0.5)
        text_lbl.set_yalign(0.5)
        vbox.pack_start(text_lbl, False, False, 0)

        btn.add(vbox)
        return btn, icon_lbl

    def on_wifi_press(self, widget, event):
        if event.button == 3:  # Right-click opens network-menu
            self.window.close_and_exit()
            subprocess.Popen([os.path.expanduser("~/.local/bin/network-menu")])
            return True
        elif event.button == 1:  # Left-click toggles wifi
            new_state = toggle_wifi()
            if new_state:
                self.wifi_btn.get_style_context().add_class("active")
                self.wifi_icon_lbl.set_text("")
            else:
                self.wifi_btn.get_style_context().remove_class("active")
                self.wifi_icon_lbl.set_text("")
            return True
        return False

    def on_bluetooth_clicked(self, btn):
        new_state = toggle_bluetooth()
        if new_state:
            self.bt_btn.get_style_context().add_class("active")
            self.bt_icon_lbl.set_text("")
        else:
            self.bt_btn.get_style_context().remove_class("active")
            self.bt_icon_lbl.set_text("")

    def on_dnd_clicked(self, btn):
        new_state = toggle_dnd()
        if new_state:
            self.dnd_btn.get_style_context().add_class("active")
            self.dnd_icon_lbl.set_text("")
        else:
            self.dnd_btn.get_style_context().remove_class("active")
            self.dnd_icon_lbl.set_text("")

    def on_night_clicked(self, btn):
        new_state = toggle_night_light()
        if new_state:
            self.night_btn.get_style_context().add_class("active")
        else:
            self.night_btn.get_style_context().remove_class("active")

    def on_game_clicked(self, btn):
        new_state = toggle_game_mode()
        if new_state:
            self.game_btn.get_style_context().add_class("active")
        else:
            self.game_btn.get_style_context().remove_class("active")

    def on_floating_clicked(self, btn):
        subprocess.run(["i3-msg", "floating", "toggle"], stderr=subprocess.DEVNULL)
