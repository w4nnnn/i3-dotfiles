import os
import time
import math
import subprocess
import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Gdk, Pango, PangoCairo, GdkPixbuf
from services import get_media_info, format_time
from config import hex_to_rgb

class PlayerWidget(Gtk.Box):
    def __init__(self, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.window = window
        self.get_style_context().add_class("music-widget")

        self.media_data = get_media_info()
        self.album_pixbuf = None
        self.is_scrubbing = False

        self._build_ui()
        self.load_album_art()

    def _build_ui(self):
        # Top row: Cover art & track metadata
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        top_row.set_valign(Gtk.Align.CENTER)

        self.cover_area = Gtk.DrawingArea()
        self.cover_area.set_size_request(46, 46)
        self.cover_area.connect("draw", self.on_album_cover_draw)
        top_row.pack_start(self.cover_area, False, False, 0)

        meta_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        meta_box.set_valign(Gtk.Align.CENTER)

        # Source badge
        badge_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        dot_lbl = Gtk.Label(label="●")
        dot_lbl.get_style_context().add_class("source-badge")
        self.source_lbl = Gtk.Label(label=f"{self.media_data['player'].upper()} (MPRIS)", xalign=0)
        self.source_lbl.get_style_context().add_class("source-badge")
        badge_box.pack_start(dot_lbl, False, False, 0)
        badge_box.pack_start(self.source_lbl, False, False, 0)
        meta_box.pack_start(badge_box, False, False, 0)

        self.track_title_lbl = Gtk.Label(label=self.media_data["title"], xalign=0)
        self.track_title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        self.track_title_lbl.set_max_width_chars(28)
        self.track_title_lbl.get_style_context().add_class("track-title")
        meta_box.pack_start(self.track_title_lbl, False, False, 0)

        self.track_artist_lbl = Gtk.Label(label=self.media_data["artist"], xalign=0)
        self.track_artist_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        self.track_artist_lbl.set_max_width_chars(28)
        self.track_artist_lbl.get_style_context().add_class("track-artist")
        meta_box.pack_start(self.track_artist_lbl, False, False, 0)

        top_row.pack_start(meta_box, True, True, 0)
        self.pack_start(top_row, False, False, 0)

        # Scrubber seek bar
        scrub_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dur = max(1, self.media_data["duration"])
        pos = min(self.media_data["position"], dur)
        self.scrubber = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, dur, 1)
        self.scrubber.set_value(pos)
        self.scrubber.set_draw_value(False)
        self.scrubber.connect("button-press-event", self.on_scrubber_press)
        self.scrubber.connect("button-release-event", self.on_scrubber_release)
        self.scrubber.connect("value-changed", self.on_scrubber_changed)
        scrub_box.pack_start(self.scrubber, False, False, 0)

        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.time_cur_lbl = Gtk.Label(label=format_time(pos), xalign=0)
        self.time_cur_lbl.get_style_context().add_class("time-label")
        self.time_dur_lbl = Gtk.Label(label=format_time(self.media_data["duration"]), xalign=1)
        self.time_dur_lbl.get_style_context().add_class("time-label")
        time_box.pack_start(self.time_cur_lbl, True, True, 0)
        time_box.pack_start(self.time_dur_lbl, False, False, 0)
        scrub_box.pack_start(time_box, False, False, 0)

        self.pack_start(scrub_box, False, False, 0)

        # Controls row
        ctrls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        ctrls_box.set_homogeneous(True)
        ctrls_box.set_valign(Gtk.Align.CENTER)

        # Shuffle
        self.shuffle_btn = Gtk.Button(label="󰒟")
        self.shuffle_btn.get_style_context().add_class("ctrl-btn")
        self.shuffle_btn.connect("clicked", self.on_shuffle_clicked)
        ctrls_box.pack_start(self.shuffle_btn, True, True, 0)

        # Previous
        prev_btn = Gtk.Button(label="󰒮")
        prev_btn.get_style_context().add_class("ctrl-btn")
        prev_btn.connect("clicked", self.on_media_prev)
        ctrls_box.pack_start(prev_btn, True, True, 0)

        # Play / Pause (Prominent center button)
        self.play_btn = Gtk.Button(label="󰏤" if self.media_data["status"] == "Playing" else "󰐊")
        self.play_btn.get_style_context().add_class("play-btn")
        self.play_btn.connect("clicked", self.on_media_play)
        ctrls_box.pack_start(self.play_btn, True, True, 0)

        # Next
        next_btn = Gtk.Button(label="󰒭")
        next_btn.get_style_context().add_class("ctrl-btn")
        next_btn.connect("clicked", self.on_media_next)
        ctrls_box.pack_start(next_btn, True, True, 0)

        # Repeat / Loop
        self.repeat_btn = Gtk.Button(label="󰑖")
        self.repeat_btn.get_style_context().add_class("ctrl-btn")
        self.repeat_btn.connect("clicked", self.on_repeat_clicked)
        ctrls_box.pack_start(self.repeat_btn, True, True, 0)

        self.pack_start(ctrls_box, False, False, 0)

        # Equalizer visualizer strip (Cava emulation)
        self.vis_area = Gtk.DrawingArea()
        self.vis_area.set_size_request(-1, 12)
        self.vis_area.connect("draw", self.on_visualizer_draw)
        self.pack_start(self.vis_area, False, False, 0)

    def load_album_art(self):
        url = self.media_data.get("art_url", "")
        self.album_pixbuf = None
        if url.startswith("file://"):
            p = url[7:]
            if os.path.isfile(p):
                try:
                    self.album_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(p, 46, 46, False)
                except Exception:
                    self.album_pixbuf = None
        elif url.startswith("/") and os.path.isfile(url):
            try:
                self.album_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(url, 46, 46, False)
            except Exception:
                self.album_pixbuf = None

    def on_album_cover_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        r = 8

        cr.new_sub_path()
        cr.arc(w - r, r, r, -math.pi / 2, 0)
        cr.arc(w - r, h - r, r, 0, math.pi / 2)
        cr.arc(r, h - r, r, math.pi / 2, math.pi)
        cr.arc(r, r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()
        cr.clip()

        if self.album_pixbuf:
            Gdk.cairo_set_source_pixbuf(cr, self.album_pixbuf, 0, 0)
            cr.paint()
        else:
            pat = cairo.LinearGradient(0, 0, w, h)
            c1 = self.window.current_theme.get("cover_grad1", "#4338ca")
            c2 = self.window.current_theme.get("cover_grad2", "#6d28d9")
            r1, g1, b1 = hex_to_rgb(c1)
            r2, g2, b2 = hex_to_rgb(c2)
            pat.add_color_stop_rgb(0, r1, g1, b1)
            pat.add_color_stop_rgb(1, r2, g2, b2)
            cr.set_source(pat)
            cr.paint()

            layout = self.create_pango_layout("󰎆")
            desc = Pango.FontDescription("JetBrainsMono Nerd Font 16")
            layout.set_font_description(desc)
            ink, log = layout.get_pixel_extents()
            cr.set_source_rgba(1, 1, 1, 0.95)
            cr.move_to((w - log.width) / 2, (h - log.height) / 2)
            PangoCairo.show_layout(cr, layout)

    def on_visualizer_draw(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        num_bars = 18
        gap = 4
        bar_w = max(2.0, (w - (num_bars - 1) * gap) / num_bars)

        r, g, b = self.window.current_theme.get("accent_rgb", (0.8, 0.65, 0.97))
        cr.set_source_rgba(r, g, b, 0.85)

        now = time.time()
        for i in range(num_bars):
            if self.media_data["status"] == "Playing":
                s1 = math.sin(now * 8.0 + i * 0.65)
                s2 = math.cos(now * 11.5 + i * 1.25)
                val = (s1 * 0.5 + 0.5) * 0.6 + (s2 * 0.5 + 0.5) * 0.4
                bar_h = max(2.5, val * (h - 2) + 2)
            else:
                bar_h = 2.5

            bx = i * (bar_w + gap)
            by = h - bar_h
            rad = min(bar_w / 2.0, 1.5)
            cr.new_sub_path()
            cr.arc(bx + rad, by + rad, rad, math.pi, 3 * math.pi / 2)
            cr.arc(bx + bar_w - rad, by + rad, rad, 3 * math.pi / 2, 2 * math.pi)
            cr.arc(bx + bar_w - rad, h - rad, rad, 0, math.pi / 2)
            cr.arc(bx + rad, h - rad, rad, math.pi / 2, math.pi)
            cr.close_path()
            cr.fill()

    def on_visualizer_tick(self):
        if self.media_data["status"] == "Playing":
            self.vis_area.queue_draw()
        return True

    def on_media_tick(self):
        self.update_media_state()
        return True

    def update_media_state(self):
        old_url = self.media_data.get("art_url", "")
        self.media_data = get_media_info()
        self.source_lbl.set_text(f"{self.media_data['player'].upper()} (MPRIS)")
        self.track_title_lbl.set_text(self.media_data["title"])
        self.track_artist_lbl.set_text(self.media_data["artist"])
        self.play_btn.set_label("󰏤" if self.media_data["status"] == "Playing" else "󰐊")

        if self.media_data.get("art_url") != old_url:
            self.load_album_art()
            self.cover_area.queue_draw()

        if not self.is_scrubbing:
            dur = max(1, self.media_data["duration"])
            pos = min(self.media_data["position"], dur)
            self.scrubber.set_range(0, dur)
            self.scrubber.set_value(pos)
            self.time_cur_lbl.set_text(format_time(pos))
            self.time_dur_lbl.set_text(format_time(self.media_data["duration"]))

    def on_scrubber_press(self, widget, event):
        self.is_scrubbing = True
        return False

    def on_scrubber_release(self, widget, event):
        val = int(self.scrubber.get_value())
        subprocess.run(["playerctl", "position", str(val)], stderr=subprocess.DEVNULL)
        self.is_scrubbing = False
        return False

    def on_scrubber_changed(self, scale):
        if self.is_scrubbing:
            val = int(scale.get_value())
            self.time_cur_lbl.set_text(format_time(val))

    def on_media_play(self, btn):
        subprocess.run(["playerctl", "play-pause"], stderr=subprocess.DEVNULL)
        self.update_media_state()

    def on_media_prev(self, btn):
        subprocess.run(["playerctl", "previous"], stderr=subprocess.DEVNULL)
        self.update_media_state()

    def on_media_next(self, btn):
        subprocess.run(["playerctl", "next"], stderr=subprocess.DEVNULL)
        self.update_media_state()

    def on_shuffle_clicked(self, btn):
        subprocess.run(["playerctl", "shuffle", "toggle"], stderr=subprocess.DEVNULL)
        try:
            out = subprocess.check_output(["playerctl", "shuffle"], stderr=subprocess.DEVNULL, text=True).strip()
            if out.lower() == "on":
                btn.get_style_context().add_class("active")
            else:
                btn.get_style_context().remove_class("active")
        except Exception:
            pass

    def on_repeat_clicked(self, btn):
        try:
            mode = subprocess.check_output(["playerctl", "loop"], stderr=subprocess.DEVNULL, text=True).strip()
            new_mode = "Track" if mode == "None" else ("Playlist" if mode == "Track" else "None")
            subprocess.run(["playerctl", "loop", new_mode], stderr=subprocess.DEVNULL)
            if new_mode in ("Track", "Playlist"):
                btn.get_style_context().add_class("active")
            else:
                btn.get_style_context().remove_class("active")
        except Exception:
            pass
