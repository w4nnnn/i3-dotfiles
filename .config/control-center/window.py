import os
import sys
import math
import signal
import subprocess
import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

from config import THEMES, PID_FILE, load_saved_theme, save_theme
from widgets import (
    HeaderWidget,
    PlayerWidget,
    SlidersWidget,
    TogglesWidget,
    TelemetryWidget,
    PowerProfilesWidget,
    FooterWidget,
)

class ControlCenterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("CatppuccinControlCenter")
        self.set_role("control-center-popup")
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.taking_screenshot = False

        # Load Theme
        self.current_theme_key = load_saved_theme()
        self.current_theme = THEMES.get(self.current_theme_key, THEMES["catppuccin"])

        # RGBA Visual for true transparency on X11
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        # Style provider
        self.css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
        self.apply_theme_css()

        # Build Main Layout (Compact and elegant, 380px fixed width)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_box.set_name("main-panel")
        main_box.set_size_request(380, -1)
        self.add(main_box)

        # 1. Header Bar
        self.header = HeaderWidget(self)
        main_box.pack_start(self.header, False, False, 0)

        # 2. Prominent Music Player
        self.player = PlayerWidget(self)
        main_box.pack_start(self.player, False, False, 0)

        # 3. Sliders Box (Audio Volume, Microphone, Display Brightness)
        self.sliders = SlidersWidget(self)
        main_box.pack_start(self.sliders, False, False, 0)

        # 4. Quick Toggles Grid (4x2 = 8 tiles)
        self.toggles = TogglesWidget(self)
        main_box.pack_start(self.toggles, False, False, 0)

        # 5. System Telemetry Row (CPU, RAM, BAT/TEMP)
        self.telemetry = TelemetryWidget(self)
        main_box.pack_start(self.telemetry, False, False, 0)

        # 6. Power Profiles (Performance, Balanced, Power Saver)
        self.power_profiles = PowerProfilesWidget(self)
        main_box.pack_start(self.power_profiles, False, False, 0)

        # 7. Footer Metadata
        self.footer = FooterWidget(self)
        main_box.pack_start(self.footer, False, False, 0)

        # Window Events
        self.connect("key-press-event", self.on_key_press)
        self.connect("map-event", self.on_map_event)
        self.connect("button-press-event", self.on_button_press)
        self.connect("size-allocate", self.on_size_allocate)
        self.connect("destroy", self.cleanup)

        # Timers
        GLib.timeout_add(70, self.player.on_visualizer_tick)
        GLib.timeout_add(1000, self.player.on_media_tick)
        GLib.timeout_add(2500, self.on_telemetry_tick)

        self.show_all()
        self.position_top_right()
        self.apply_cursor()

    # -----------------------------------------------------
    # Window Shape & Positioning
    # -----------------------------------------------------
    def on_size_allocate(self, widget, alloc):
        w, h = alloc.width, alloc.height
        r = 16
        surf = cairo.ImageSurface(cairo.FORMAT_A1, w, h)
        cr = cairo.Context(surf)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()

        cr.new_sub_path()
        cr.arc(w - r, r, r, -math.pi / 2, 0)
        cr.arc(w - r, h - r, r, 0, math.pi / 2)
        cr.arc(r, h - r, r, math.pi / 2, math.pi)
        cr.arc(r, r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill()

        region = Gdk.cairo_region_create_from_surface(surf)
        widget.shape_combine_region(region)

    def position_top_right(self):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() or display.get_monitor_at_point(0, 0)
        geom = monitor.get_geometry()
        min_sz, nat_sz = self.get_preferred_size()
        pos_x = geom.x + geom.width - nat_sz.width - 12
        pos_y = geom.y + 44
        self.move(pos_x, pos_y)

    def apply_cursor(self):
        display = Gdk.Display.get_default()
        cursor = Gdk.Cursor.new_from_name(display, "default")
        if not cursor:
            cursor = Gdk.Cursor.new_from_name(display, "left_ptr")
        if cursor and self.get_window():
            self.get_window().set_cursor(cursor)

    # -----------------------------------------------------
    # Theme & CSS
    # -----------------------------------------------------
    def apply_theme_css(self):
        t = self.current_theme
        css = f"""
        window {{
            background-color: transparent;
        }}
        #main-panel {{
            background-color: {t["bg_card"]};
            border: 2px solid {t["border_active"]};
            border-radius: 16px;
            padding: 12px;
            min-width: 380px;
        }}
        .distro-avatar {{
            background-color: {t["accent"]};
            color: {t["accent_contrast"]};
            border-radius: 8px;
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 14pt;
            font-weight: bold;
            min-width: 32px;
            min-height: 32px;
        }}
        .host-title {{
            color: {t["text_primary"]};
            font-size: 9.5pt;
            font-weight: bold;
            font-family: 'JetBrainsMono Nerd Font';
        }}
        .host-meta {{
            color: {t["text_muted"]};
            font-size: 7.5pt;
            font-family: 'JetBrainsMono Nerd Font';
        }}
        .header-btn {{
            background-color: {t["bg_surface"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border_color"]};
            border-radius: 8px;
            min-width: 30px;
            min-height: 30px;
            font-family: 'lucide', 'JetBrainsMono Nerd Font';
            font-size: 13pt;
            padding: 0;
        }}
        .header-btn:hover {{
            background-color: {t["bg_hover"]};
            color: {t["accent"]};
        }}
        .power-btn {{
            background-color: {t["danger_bg"]};
            color: {t["danger"]};
            border-color: transparent;
        }}
        .power-btn:hover {{
            background-color: {t["danger"]};
            color: {t["accent_contrast"]};
        }}

        /* Music Card */
        .music-widget {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border_color"]};
            border-radius: 12px;
            padding: 10px;
        }}
        .source-badge {{
            color: {t["accent"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7pt;
            font-weight: bold;
        }}
        .track-title {{
            color: {t["text_primary"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 9.5pt;
            font-weight: bold;
        }}
        .track-artist {{
            color: {t["text_secondary"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 8pt;
        }}
        .time-label {{
            color: {t["text_muted"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7.5pt;
        }}
        .ctrl-btn {{
            background-color: transparent;
            border: none;
            color: {t["text_primary"]};
            font-family: 'lucide', 'JetBrainsMono Nerd Font';
            font-size: 13pt;
            min-width: 28px;
            min-height: 28px;
            border-radius: 6px;
            padding: 0;
        }}
        .ctrl-btn:hover {{
            background-color: {t["bg_hover"]};
            color: {t["accent"]};
        }}
        .ctrl-btn.active {{
            color: {t["accent"]};
        }}
        .play-btn {{
            background-color: {t["accent"]};
            color: {t["accent_contrast"]};
            border: none;
            border-radius: 8px;
            min-width: 32px;
            min-height: 32px;
            font-family: 'lucide', 'JetBrainsMono Nerd Font';
            font-size: 14pt;
            padding: 0;
        }}
        .play-btn:hover {{
            opacity: 0.92;
        }}

        /* Scale / Sliders */
        scale {{
            margin: 0;
            padding: 0;
            min-height: 10px;
        }}
        scale trough {{
            background-color: {t["trough"]};
            border-radius: 999px;
            min-height: 4px;
            margin: 0;
            padding: 0;
        }}
        scale highlight,
        scale trough highlight {{
            background-color: {t["accent"]};
            background-image: none;
            border-radius: 999px;
        }}
        scale slider {{
            background-color: {t["text_primary"]};
            background-image: none;
            border: 2px solid {t["bg_card"]};
            box-shadow: none;
            border-radius: 50%;
            min-width: 10px;
            min-height: 10px;
            margin: -3px 0;
        }}

        /* Sliders Box */
        .sliders-box {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border_color"]};
            border-radius: 12px;
            padding: 6px 10px;
        }}
        .slider-row {{
            min-height: 24px;
        }}
        .slider-icon-btn {{
            background-color: transparent;
            border: none;
            font-family: 'lucide', 'JetBrainsMono Nerd Font';
            font-size: 13pt;
            color: {t["accent"]};
            min-width: 24px;
            min-height: 24px;
            padding: 0;
        }}
        .slider-icon-btn:hover {{
            color: {t["text_primary"]};
        }}
        .slider-icon-bright {{
            color: {t["warning"]};
        }}
        .slider-val {{
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 8pt;
            font-weight: bold;
            color: {t["text_secondary"]};
            min-width: 32px;
        }}

        /* Toggles Grid */
        .toggle-tile {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border_color"]};
            border-radius: 8px;
            padding: 5px 2px;
            min-height: 44px;
        }}
        .toggle-tile:hover {{
            background-color: {t["bg_hover"]};
        }}
        .toggle-tile.active {{
            background-color: {t["accent"]};
            border-color: {t["accent"]};
        }}
        .toggle-icon {{
            font-family: 'lucide', 'JetBrainsMono Nerd Font';
            font-size: 15pt;
            color: {t["accent_secondary"]};
        }}
        .toggle-tile.active .toggle-icon {{
            color: {t["accent_contrast"]};
        }}
        .toggle-label {{
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7.5pt;
            font-weight: 500;
            color: {t["text_secondary"]};
        }}
        .toggle-tile.active .toggle-label {{
            color: {t["accent_contrast"]};
            font-weight: bold;
        }}

        /* Telemetry Row */
        .stat-badge {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border_color"]};
            border-radius: 8px;
            padding: 5px 8px;
        }}
        .stat-name {{
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7pt;
            font-weight: bold;
            color: {t["text_muted"]};
        }}
        .stat-sub {{
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7pt;
            color: {t["text_muted"]};
        }}
        .stat-val {{
            font-family: 'JetBrainsMono Nerd Font', 'lucide';
            font-size: 9.5pt;
            font-weight: bold;
            color: {t["text_primary"]};
        }}

        /* Power Profiles */
        .power-profiles {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border_color"]};
            border-radius: 8px;
            padding: 2px;
        }}
        .profile-pill {{
            background-color: transparent;
            border: none;
            color: {t["text_secondary"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 8pt;
            font-weight: 500;
            border-radius: 6px;
            padding: 3px 6px;
        }}
        .profile-pill:hover {{
            background-color: {t["bg_hover"]};
        }}
        .profile-pill.active {{
            background-color: {t["accent"]};
            color: {t["accent_contrast"]};
            font-weight: bold;
        }}

        /* Footer */
        .panel-footer {{
            border-top: 1px solid {t["border_color"]};
            padding-top: 4px;
        }}
        .footer-text {{
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7.5pt;
            color: {t["text_muted"]};
        }}
        .footer-btn {{
            background-color: transparent;
            border: none;
            border-radius: 6px;
            box-shadow: none;
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 7.8pt;
            color: {t["accent"]};
            padding: 2px 6px;
            margin: 0;
            min-height: 0;
            font-weight: bold;
        }}
        .footer-btn:hover {{
            background-color: {t["bg_hover"]};
            color: {t["accent"]};
        }}

        /* Theme Dropdown Menu */
        .theme-menu {{
            background-color: {t["bg_card"]};
            border: 1px solid {t["border_color"]};
            border-radius: 10px;
            padding: 4px;
        }}
        .theme-menu menuitem {{
            color: {t["text_primary"]};
            font-family: 'JetBrainsMono Nerd Font';
            font-size: 8.5pt;
            border-radius: 6px;
            padding: 4px 10px;
        }}
        .theme-menu menuitem:hover {{
            background-color: {t["bg_hover"]};
            color: {t["accent"]};
        }}
        """
        self.css_provider.load_from_data(css.encode())

    def set_theme(self, theme_key):
        if theme_key in THEMES:
            self.current_theme_key = theme_key
            self.current_theme = THEMES[theme_key]
            save_theme(theme_key)
            self.apply_theme_css()
            self.header.avatar_area.queue_draw()
            self.player.cover_area.queue_draw()
            self.player.vis_area.queue_draw()
            self.telemetry.cpu_meter.queue_draw()
            self.telemetry.ram_meter.queue_draw()
            self.telemetry.bat_meter.queue_draw()

            # Synchronize global desktop theme (Rofi, Polybar, i3, Dunst, Kitty)
            bin_switcher = os.path.expanduser("~/.local/bin/theme-switcher")
            if os.path.isfile(bin_switcher):
                subprocess.Popen([bin_switcher, theme_key], stderr=subprocess.DEVNULL)

    def on_telemetry_tick(self):
        self.telemetry.update_telemetry()
        self.header.update_uptime()
        return True

    # -----------------------------------------------------
    # Window Interaction & Grab
    # -----------------------------------------------------
    def on_key_press(self, widget, event):
        if event.keyval in (Gdk.KEY_Escape,):
            self.close_and_exit()
            return True
        elif event.keyval == Gdk.KEY_Print:
            self.taking_screenshot = True
            bin_dir = os.path.expanduser("~/.local/bin")
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                subprocess.Popen([os.path.join(bin_dir, "screenshot"), "full"])
            else:
                subprocess.Popen([os.path.join(bin_dir, "screenshot"), "select"])
            GLib.timeout_add(1500, lambda: setattr(self, "taking_screenshot", False))
            return True
        return False

    def on_map_event(self, widget, event):
        GLib.idle_add(self.grab_seat)

    def grab_seat(self):
        try:
            seat = Gdk.Display.get_default().get_default_seat()
            if seat and self.get_window():
                cursor = self.get_window().get_cursor()
                seat.grab(self.get_window(), Gdk.SeatCapabilities.ALL, True, cursor, None, None)
        except Exception:
            pass
        return False

    def on_button_press(self, widget, event):
        if getattr(self, "taking_screenshot", False):
            return False
        if not self.get_window():
            return False
        success, ox, oy = self.get_window().get_origin()
        w = self.get_window().get_width()
        h = self.get_window().get_height()
        inside = (ox <= event.x_root <= ox + w) and (oy <= event.y_root <= oy + h)
        if not inside:
            self.close_and_exit()
            return True
        return False

    def close_and_exit(self):
        try:
            seat = Gdk.Display.get_default().get_default_seat()
            if seat:
                seat.ungrab()
        except Exception:
            pass
        self.destroy()
        Gtk.main_quit()

    def cleanup(self, *args):
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except Exception:
                pass

def main():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.remove(PID_FILE)
            os.kill(old_pid, signal.SIGTERM)
            sys.exit(0)
        except Exception:
            pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    win = ControlCenterWindow()
    Gtk.main()

if __name__ == "__main__":
    main()
