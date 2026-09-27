import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from services import get_power_profile, set_power_profile

class PowerProfilesWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.window = window
        self.get_style_context().add_class("power-profiles")
        self.set_homogeneous(True)
        self._build_ui()

    def _build_ui(self):
        current_prof = get_power_profile()

        self.prof_perf_btn = Gtk.Button(label="Performance")
        self.prof_perf_btn.get_style_context().add_class("profile-pill")
        if current_prof == "performance":
            self.prof_perf_btn.get_style_context().add_class("active")
        self.prof_perf_btn.connect("clicked", lambda w: self.on_profile_set("performance"))
        self.pack_start(self.prof_perf_btn, True, True, 0)

        self.prof_bal_btn = Gtk.Button(label="Balanced")
        self.prof_bal_btn.get_style_context().add_class("profile-pill")
        if current_prof == "balanced":
            self.prof_bal_btn.get_style_context().add_class("active")
        self.prof_bal_btn.connect("clicked", lambda w: self.on_profile_set("balanced"))
        self.pack_start(self.prof_bal_btn, True, True, 0)

        self.prof_sav_btn = Gtk.Button(label="Power Saver")
        self.prof_sav_btn.get_style_context().add_class("profile-pill")
        if current_prof == "power-saver":
            self.prof_sav_btn.get_style_context().add_class("active")
        self.prof_sav_btn.connect("clicked", lambda w: self.on_profile_set("power-saver"))
        self.pack_start(self.prof_sav_btn, True, True, 0)

    def on_profile_set(self, profile):
        set_power_profile(profile)
        for b in (self.prof_perf_btn, self.prof_bal_btn, self.prof_sav_btn):
            b.get_style_context().remove_class("active")

        if profile == "performance":
            self.prof_perf_btn.get_style_context().add_class("active")
        elif profile == "balanced":
            self.prof_bal_btn.get_style_context().add_class("active")
        elif profile == "power-saver":
            self.prof_sav_btn.get_style_context().add_class("active")
