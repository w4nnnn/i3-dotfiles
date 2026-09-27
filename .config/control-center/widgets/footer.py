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

        r_lbl = Gtk.Label(label="Mod + C", xalign=1)
        r_lbl.get_style_context().add_class("footer-text")
        self.pack_start(r_lbl, False, False, 0)
