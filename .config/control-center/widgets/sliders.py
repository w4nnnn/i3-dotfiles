import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from services import (
    get_initial_audio,
    get_volume,
    get_sink_mute,
    set_volume,
    toggle_sink_mute,
    get_mic_volume,
    get_mic_mute,
    set_mic_volume,
    toggle_mic_mute,
    get_brightness,
    set_brightness,
)

class SlidersWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.window = window
        self.get_style_context().add_class("sliders-box")
        self._build_ui()

    def _build_ui(self):
        # Initial Audio Levels (parallel fetch)
        vol_val, vol_mute, mic_val, mic_mute = get_initial_audio()

        # Master Audio
        vol_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vol_row.get_style_context().add_class("slider-row")

        self.vol_btn = Gtk.Button(label="󰝟" if vol_mute else "󰕾")
        self.vol_btn.get_style_context().add_class("slider-icon-btn")
        self.vol_btn.connect("clicked", self.on_vol_mute_clicked)
        vol_row.pack_start(self.vol_btn, False, False, 0)

        self.vol_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.vol_scale.set_value(0 if vol_mute else vol_val)
        self.vol_scale.set_draw_value(False)
        self.vol_scale.connect("value-changed", self.on_vol_changed)
        vol_row.pack_start(self.vol_scale, True, True, 0)

        self.vol_lbl = Gtk.Label(label=f"{vol_val}%", xalign=1)
        self.vol_lbl.get_style_context().add_class("slider-val")
        vol_row.pack_start(self.vol_lbl, False, False, 0)
        self.pack_start(vol_row, False, False, 0)

        # Microphone Input
        mic_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        mic_row.get_style_context().add_class("slider-row")

        self.mic_btn = Gtk.Button(label="󰍭" if mic_mute else "󰍬")
        self.mic_btn.get_style_context().add_class("slider-icon-btn")
        self.mic_btn.connect("clicked", self.on_mic_mute_clicked)
        mic_row.pack_start(self.mic_btn, False, False, 0)

        self.mic_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.mic_scale.set_value(0 if mic_mute else mic_val)
        self.mic_scale.set_draw_value(False)
        self.mic_scale.connect("value-changed", self.on_mic_changed)
        mic_row.pack_start(self.mic_scale, True, True, 0)

        self.mic_lbl = Gtk.Label(label=f"{mic_val}%", xalign=1)
        self.mic_lbl.get_style_context().add_class("slider-val")
        mic_row.pack_start(self.mic_lbl, False, False, 0)
        self.pack_start(mic_row, False, False, 0)

        # Display Brightness
        br_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        br_row.get_style_context().add_class("slider-row")
        br_val = get_brightness()

        br_btn = Gtk.Button(label="󰃠")
        br_btn.get_style_context().add_class("slider-icon-btn")
        br_btn.get_style_context().add_class("slider-icon-bright")
        br_row.pack_start(br_btn, False, False, 0)

        self.br_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 5, 100, 1)
        self.br_scale.set_value(br_val)
        self.br_scale.set_draw_value(False)
        self.br_scale.connect("value-changed", self.on_brightness_changed)
        br_row.pack_start(self.br_scale, True, True, 0)

        self.br_lbl = Gtk.Label(label=f"{br_val}%", xalign=1)
        self.br_lbl.get_style_context().add_class("slider-val")
        br_row.pack_start(self.br_lbl, False, False, 0)
        self.pack_start(br_row, False, False, 0)

    def on_vol_mute_clicked(self, btn):
        toggle_sink_mute()
        muted = get_sink_mute()
        val = get_volume()
        self.vol_btn.set_label("󰝟" if muted else "󰕾")
        self.vol_scale.set_value(0 if muted else val)
        self.vol_lbl.set_text(f"{val}%")

    def on_vol_changed(self, scale):
        val = int(scale.get_value())
        set_volume(val)
        self.vol_lbl.set_text(f"{val}%")
        if val > 0:
            self.vol_btn.set_label("󰕾")

    def on_mic_mute_clicked(self, btn):
        toggle_mic_mute()
        muted = get_mic_mute()
        val = get_mic_volume()
        self.mic_btn.set_label("󰍭" if muted else "󰍬")
        self.mic_scale.set_value(0 if muted else val)
        self.mic_lbl.set_text(f"{val}%")

    def on_mic_changed(self, scale):
        val = int(scale.get_value())
        set_mic_volume(val)
        self.mic_lbl.set_text(f"{val}%")
        if val > 0:
            self.mic_btn.set_label("󰍬")

    def on_brightness_changed(self, scale):
        val = int(scale.get_value())
        set_brightness(val)
        self.br_lbl.set_text(f"{val}%")
