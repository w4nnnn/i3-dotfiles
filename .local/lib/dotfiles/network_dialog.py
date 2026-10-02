"""
GTK3 UI components and helpers for Wi-Fi Network Menu:
Password Prompt modal view and Network List item renderer.
"""
import html
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
from gi.repository import Gtk, Pango

def build_network_row(net):
    row = Gtk.ListBoxRow()
    row.net_data = net
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    box.get_style_context().add_class("element-row")
    if net["in_use"]:
        box.get_style_context().add_class("connected")

    # Signal Icon
    sig = net["signal"]
    if net["in_use"]:
        s_icon = "󰖩"
    elif sig >= 70:
        s_icon = "󰤨"
    elif sig >= 50:
        s_icon = "󰤥"
    elif sig >= 25:
        s_icon = "󰤢"
    else:
        s_icon = "󰤟"

    icon_lbl = Gtk.Label(label=s_icon)
    icon_lbl.get_style_context().add_class("element-text")
    box.pack_start(icon_lbl, False, False, 0)

    # SSID
    ssid_lbl = Gtk.Label(label=f"<b>{html.escape(net['ssid'])}</b>", xalign=0)
    ssid_lbl.set_use_markup(True)
    ssid_lbl.get_style_context().add_class("element-text")
    ssid_lbl.set_ellipsize(Pango.EllipsizeMode.END)
    ssid_lbl.set_max_width_chars(28)
    box.pack_start(ssid_lbl, True, True, 0)

    # Badges
    if net["in_use"]:
        badge = Gtk.Label(label="CONNECTED")
        badge.get_style_context().add_class("badge-connected")
        box.pack_start(badge, False, False, 0)

    band_txt = "5GHz" if net["chan"] > 14 else "2.4G"
    band_lbl = Gtk.Label(label=band_txt)
    band_lbl.get_style_context().add_class("badge-band")
    box.pack_start(band_lbl, False, False, 0)

    is_open = not net["security"] or net["security"] == "--"
    sec_txt = "OPEN" if is_open else "SEC"
    sec_lbl = Gtk.Label(label=sec_txt)
    sec_lbl.get_style_context().add_class("badge-sec")
    if is_open:
        sec_lbl.get_style_context().add_class("open")
    box.pack_start(sec_lbl, False, False, 0)

    sig_lbl = Gtk.Label(label=f"{sig:>3}%")
    sig_lbl.get_style_context().add_class("badge-sig")
    box.pack_start(sig_lbl, False, False, 0)

    row.add(box)
    return row

class PasswordPromptBox(Gtk.Box):
    def __init__(self, on_connect_cb, on_cancel_cb):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.set_size_request(440, -1)
        self.on_connect_cb = on_connect_cb
        self.on_cancel_cb = on_cancel_cb
        self.target_ssid = ""

        # Lock Icon
        pwd_icon = Gtk.Label(label="󰌾")
        pwd_icon.set_name("pwd-icon")
        self.pack_start(pwd_icon, False, False, 0)

        # Title & Subtitle
        self.title_lbl = Gtk.Label(label="Connect to Wi-Fi")
        self.title_lbl.set_name("pwd-title")
        self.title_lbl.set_use_markup(True)
        self.pack_start(self.title_lbl, False, False, 0)

        self.sub_lbl = Gtk.Label(label="Enter security key to join this network")
        self.sub_lbl.set_name("pwd-subtitle")
        self.pack_start(self.sub_lbl, False, False, 0)

        # Password Entry Container
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        entry_box.set_name("pwd-entry-container")

        self.entry = Gtk.Entry()
        self.entry.set_name("pwd-entry")
        self.entry.set_visibility(False)
        self.entry.set_placeholder_text("Password...")
        self.entry.connect("activate", lambda e: self.on_connect_cb())
        entry_box.pack_start(self.entry, True, True, 0)

        self.eye_btn = Gtk.Button(label="󰈈")
        self.eye_btn.get_style_context().add_class("pwd-eye-btn")
        self.eye_btn.set_tooltip_text("Show Password")
        self.eye_btn.connect("clicked", self.toggle_visibility)
        entry_box.pack_start(self.eye_btn, False, False, 0)

        self.pack_start(entry_box, False, False, 0)

        # Error message
        self.error_lbl = Gtk.Label(label="")
        self.error_lbl.set_name("pwd-error")
        self.pack_start(self.error_lbl, False, False, 0)

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.set_margin_top(10)

        self.cancel_btn = Gtk.Button(label="Cancel")
        self.cancel_btn.get_style_context().add_class("pwd-btn")
        self.cancel_btn.get_style_context().add_class("cancel")
        self.cancel_btn.connect("clicked", lambda w: self.on_cancel_cb())
        btn_box.pack_start(self.cancel_btn, False, False, 0)

        self.connect_btn = Gtk.Button(label="󰖩 Connect")
        self.connect_btn.get_style_context().add_class("pwd-btn")
        self.connect_btn.get_style_context().add_class("connect")
        self.connect_btn.connect("clicked", lambda w: self.on_connect_cb())
        btn_box.pack_start(self.connect_btn, False, False, 0)

        self.pack_start(btn_box, False, False, 0)

    def prepare_for_network(self, ssid):
        self.target_ssid = ssid
        self.title_lbl.set_markup(f"Connect to <b>{html.escape(ssid)}</b>")
        self.sub_lbl.set_text("Enter security key to join this network")
        self.entry.set_text("")
        self.entry.set_visibility(False)
        self.eye_btn.set_label("󰈈")
        self.error_lbl.set_text("")
        self.connect_btn.set_sensitive(True)
        self.cancel_btn.set_sensitive(True)
        self.connect_btn.set_label("󰖩 Connect")

    def toggle_visibility(self, btn=None):
        is_vis = self.entry.get_visibility()
        self.entry.set_visibility(not is_vis)
        self.eye_btn.set_label("󰈉" if not is_vis else "󰈈")
        self.eye_btn.set_tooltip_text("Hide Password" if not is_vis else "Show Password")

    def set_loading(self, loading=True):
        self.connect_btn.set_sensitive(not loading)
        self.cancel_btn.set_sensitive(not loading)
        self.connect_btn.set_label("󰑐 Connecting..." if loading else "󰖩 Connect")

    def set_error(self, err_msg):
        self.error_lbl.set_text(f"󰅖 {err_msg}")
        self.entry.grab_focus()
        self.entry.select_region(0, -1)
