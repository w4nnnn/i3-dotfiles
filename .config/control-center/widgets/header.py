import os
import math
import subprocess
import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Gdk, Pango, PangoCairo
from services import get_username, get_hostname, get_uptime
from config import hex_to_rgb, THEMES

class HeaderWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.window = window
        self._build_ui()

    def _build_ui(self):
        # Distro avatar (32x32, Arch icon drawn with Cairo for perfect centering)
        self.avatar_area = Gtk.DrawingArea()
        self.avatar_area.set_size_request(32, 32)
        self.avatar_area.set_valign(Gtk.Align.CENTER)
        self.avatar_area.set_halign(Gtk.Align.CENTER)
        self.avatar_area.connect("draw", self.on_avatar_draw)
        self.pack_start(self.avatar_area, False, False, 0)

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

        # Theme Switcher button
        theme_btn = Gtk.Button(label="")
        theme_btn.get_style_context().add_class("header-btn")
        if theme_btn.get_child():
            theme_btn.get_child().set_halign(Gtk.Align.CENTER)
            theme_btn.get_child().set_valign(Gtk.Align.CENTER)
        theme_btn.set_tooltip_text("Switch Theme")
        theme_btn.connect("clicked", self.on_theme_clicked)
        actions_box.pack_start(theme_btn, False, False, 0)

        # Lock button
        lock_btn = Gtk.Button(label="")
        lock_btn.get_style_context().add_class("header-btn")
        if lock_btn.get_child():
            lock_btn.get_child().set_halign(Gtk.Align.CENTER)
            lock_btn.get_child().set_valign(Gtk.Align.CENTER)
        lock_btn.set_tooltip_text("Lock Screen")
        lock_btn.connect("clicked", lambda w: (self.window.close_and_exit(), subprocess.Popen([os.path.join(bin_dir, "lockscreen")])))
        actions_box.pack_start(lock_btn, False, False, 0)

        # Power button
        power_btn = Gtk.Button(label="")
        power_btn.get_style_context().add_class("header-btn")
        power_btn.get_style_context().add_class("power-btn")
        if power_btn.get_child():
            power_btn.get_child().set_halign(Gtk.Align.CENTER)
            power_btn.get_child().set_valign(Gtk.Align.CENTER)
        power_btn.set_tooltip_text("Power Menu")
        power_btn.connect("clicked", lambda w: (self.window.close_and_exit(), subprocess.Popen([os.path.join(bin_dir, "powermenu")])))
        actions_box.pack_start(power_btn, False, False, 0)

        self.pack_start(actions_box, False, False, 0)

    def on_theme_clicked(self, btn):
        menu = Gtk.Menu()
        menu.get_style_context().add_class("theme-menu")
        for key, theme_data in THEMES.items():
            name = theme_data.get("name", key)
            is_active = key == self.window.current_theme_key
            label = f"● {name}" if is_active else f"  {name}"
            item = Gtk.MenuItem(label=label)
            item.connect("activate", lambda w, k=key: self.window.set_theme(k))
            menu.append(item)
        menu.show_all()
        try:
            menu.popup_at_widget(btn, Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, None)
        except Exception:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def update_uptime(self):
        self.host_meta_lbl.set_text(f"X11 · Up {get_uptime()}")

    def on_avatar_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        r = 8

        # Rounded rectangle background
        cr.new_sub_path()
        cr.arc(w - r, r, r, -math.pi / 2, 0)
        cr.arc(w - r, h - r, r, 0, math.pi / 2)
        cr.arc(r, h - r, r, math.pi / 2, math.pi)
        cr.arc(r, r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()

        ar, ag, ab = self.window.current_theme.get("accent_rgb", (203 / 255.0, 166 / 255.0, 247 / 255.0))
        cr.set_source_rgb(ar, ag, ab)
        cr.fill()

        # Arch logo centered exactly by ink bounds
        layout = self.create_pango_layout("󰣇")
        desc = Pango.FontDescription("JetBrainsMono Nerd Font Bold 14")
        layout.set_font_description(desc)
        ink, log = layout.get_pixel_extents()

        x = round((w - ink.width) / 2.0 - ink.x)
        y = round((h - ink.height) / 2.0 - ink.y)

        cr.move_to(x, y)
        cr_text = self.window.current_theme.get("accent_contrast", "#11111b")
        tr, tg, tb = hex_to_rgb(cr_text)
        cr.set_source_rgb(tr, tg, tb)
        PangoCairo.show_layout(cr, layout)
