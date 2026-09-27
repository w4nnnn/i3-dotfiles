import math
import cairo
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from services import get_cpu_info, get_ram_info, get_battery_and_temp

class TelemetryWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.window = window
        self.set_homogeneous(True)

        self.cpu_frac = 0.18
        self.ram_frac = 0.25
        self.bat_frac = 0.85

        self._build_ui()

    def _build_ui(self):
        # CPU Card
        cpu_usage, cpu_brand = get_cpu_info()
        self.cpu_frac = cpu_usage / 100.0
        self.cpu_val_lbl, self.cpu_meter, cpu_card = self.make_stat_card(
            "CPU", cpu_brand, f"{cpu_usage}%", lambda: self.cpu_frac
        )
        self.pack_start(cpu_card, True, True, 0)

        # RAM Card
        ram_used, ram_pct, ram_frac = get_ram_info()
        self.ram_frac = ram_frac
        self.ram_val_lbl, self.ram_meter, ram_card = self.make_stat_card(
            "RAM", "DDR", ram_used, lambda: self.ram_frac
        )
        self.pack_start(ram_card, True, True, 0)

        # BAT / TEMP Card
        has_bat, bat_cap, bat_stat, temp_c = get_battery_and_temp()
        self.bat_frac = bat_cap / 100.0
        bat_str = f"{bat_cap}% " if "Charging" in bat_stat else f"{bat_cap}%"
        self.bat_val_lbl, self.bat_meter, bat_card = self.make_stat_card(
            "BAT", f"{temp_c}°C", bat_str, lambda: self.bat_frac
        )
        self.pack_start(bat_card, True, True, 0)

    def make_stat_card(self, title, subtitle, value_str, get_frac):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        card.get_style_context().add_class("stat-badge")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        t_lbl = Gtk.Label(label=title, xalign=0)
        t_lbl.get_style_context().add_class("stat-name")
        s_lbl = Gtk.Label(label=subtitle, xalign=1)
        s_lbl.get_style_context().add_class("stat-sub")
        header.pack_start(t_lbl, True, True, 0)
        header.pack_start(s_lbl, False, False, 0)
        card.pack_start(header, False, False, 0)

        v_lbl = Gtk.Label(label=value_str, xalign=0)
        v_lbl.get_style_context().add_class("stat-val")
        card.pack_start(v_lbl, False, False, 0)

        # Thin 4px pill meter using Cairo DrawingArea
        meter = Gtk.DrawingArea()
        meter.set_size_request(-1, 4)

        def draw_meter(w_meter, cr):
            w = w_meter.get_allocated_width()
            h = w_meter.get_allocated_height()
            rad = h / 2.0
            # Background trough
            tr, tg, tb = self.window.current_theme.get("meter_trough_rgb", (0.2, 0.2, 0.25))
            cr.set_source_rgba(tr, tg, tb, 1.0)
            cr.new_sub_path()
            cr.arc(rad, rad, rad, math.pi / 2, 3 * math.pi / 2)
            cr.arc(w - rad, rad, rad, -math.pi / 2, math.pi / 2)
            cr.close_path()
            cr.fill()

            # Fill bar
            frac = max(0.0, min(1.0, get_frac()))
            fill_w = w * frac
            if fill_w > rad * 2:
                ar, ag, ab = self.window.current_theme.get("accent_rgb", (0.8, 0.65, 0.97))
                cr.set_source_rgba(ar, ag, ab, 1.0)
                cr.new_sub_path()
                cr.arc(rad, rad, rad, math.pi / 2, 3 * math.pi / 2)
                cr.arc(fill_w - rad, rad, rad, -math.pi / 2, math.pi / 2)
                cr.close_path()
                cr.fill()

        meter.connect("draw", draw_meter)
        card.pack_start(meter, False, False, 0)

        return v_lbl, meter, card

    def update_telemetry(self):
        cpu_usage, _ = get_cpu_info()
        self.cpu_frac = cpu_usage / 100.0
        self.cpu_val_lbl.set_text(f"{cpu_usage}%")
        self.cpu_meter.queue_draw()

        ram_used, _, ram_frac = get_ram_info()
        self.ram_frac = ram_frac
        self.ram_val_lbl.set_text(ram_used)
        self.ram_meter.queue_draw()

        has_bat, bat_cap, bat_stat, temp_c = get_battery_and_temp()
        self.bat_frac = bat_cap / 100.0
        bat_str = f"{bat_cap}% " if "Charging" in bat_stat else f"{bat_cap}%"
        self.bat_val_lbl.set_text(bat_str)
        self.bat_meter.queue_draw()
