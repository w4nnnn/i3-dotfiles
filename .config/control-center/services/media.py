"""
Media player telemetry and control service via playerctl MPRIS.
"""
import subprocess

def get_media_info():
    try:
        status = subprocess.check_output(["playerctl", "status"], stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        status = "Stopped"

    if status in ("Playing", "Paused"):
        try:
            out = subprocess.check_output(
                ["playerctl", "metadata", "--format", "{{playerName}}|{{title}}|{{artist}}|{{mpris:artUrl}}|{{mpris:length}}"],
                stderr=subprocess.DEVNULL, text=True
            ).strip()
            parts = out.split("|")
            player = parts[0] if len(parts) > 0 and parts[0] else "MPRIS"
            title = parts[1] if len(parts) > 1 and parts[1] else "Unknown Title"
            artist = parts[2] if len(parts) > 2 and parts[2] else "Unknown Artist"
            art_url = parts[3] if len(parts) > 3 else ""
            length_us = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
            duration_sec = length_us // 1000000
        except Exception:
            player = "MPRIS"
            title = "Playing"
            artist = ""
            art_url = ""
            duration_sec = 0

        try:
            pos_out = subprocess.check_output(["playerctl", "position"], stderr=subprocess.DEVNULL, text=True).strip()
            pos_sec = int(float(pos_out))
        except Exception:
            pos_sec = 0

        return {
            "status": status,
            "player": player,
            "title": title,
            "artist": artist,
            "art_url": art_url,
            "position": pos_sec,
            "duration": duration_sec
        }

    return {
        "status": "Stopped",
        "player": "MPRIS",
        "title": "No media playing",
        "artist": "Desktop Audio · Idle",
        "art_url": "",
        "position": 0,
        "duration": 0
    }

def format_time(sec):
    sec = max(0, int(sec))
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"
