import os
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FooterWidget(Gtk.Box):
    def __init__(self, window=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.window = window
        self.get_style_context().add_class("panel-footer")
        self._build_ui()

    def _build_ui(self):
        l_lbl = Gtk.Label(label="i3wm · X11", xalign=0)
        l_lbl.get_style_context().add_class("footer-text")
        self.pack_start(l_lbl, True, True, 0)

        # Interactive Keybindings button / link
        keybind_btn = Gtk.Button(label="⌨ Keybinds")
        keybind_btn.get_style_context().add_class("footer-btn")
        keybind_btn.set_tooltip_text("Open Keybindings Cheatsheet (Super + /)")
        keybind_btn.connect("clicked", self.on_keybinds_clicked)
        self.pack_start(keybind_btn, False, False, 0)

    def on_keybinds_clicked(self, btn):
        bin_dir = os.path.expanduser("~/.local/bin")
        if self.window:
            self.window.close_and_exit()
        subprocess.Popen([os.path.join(bin_dir, "keybinds-viewer")])
