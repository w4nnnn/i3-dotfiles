"""
Audio volume, microphone, and mute services via PulseAudio / PipeWire pactl & pamixer.
"""
import re
import subprocess
import concurrent.futures

def get_volume():
    try:
        out = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
        m = re.search(r'/\s*(\d+)%', out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 50

def get_sink_mute():
    try:
        out = subprocess.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
        return "yes" in out.lower()
    except Exception:
        return False

def set_volume(val):
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{int(val)}%"], stderr=subprocess.DEVNULL)

def toggle_sink_mute():
    subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"], stderr=subprocess.DEVNULL)

toggle_mute = toggle_sink_mute

def get_mic_volume():
    try:
        out = subprocess.check_output(["pamixer", "--default-source", "--get-volume"], stderr=subprocess.DEVNULL, text=True).strip()
        if out.isdigit():
            return int(out)
    except Exception:
        pass
    try:
        out = subprocess.check_output(["pactl", "get-source-volume", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
        m = re.search(r'/\s*(\d+)%', out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 60

def get_mic_mute():
    try:
        out = subprocess.check_output(["pamixer", "--default-source", "--get-mute"], stderr=subprocess.DEVNULL, text=True).strip()
        return "true" in out.lower()
    except Exception:
        pass
    try:
        out = subprocess.check_output(["pactl", "get-source-mute", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
        return "yes" in out.lower()
    except Exception:
        return False

def set_mic_volume(val):
    val = int(val)
    subprocess.run(["pamixer", "--default-source", "--set-volume", str(val)], stderr=subprocess.DEVNULL)
    subprocess.run(["pactl", "set-source-volume", "@DEFAULT_SOURCE@", f"{val}%"], stderr=subprocess.DEVNULL)

def toggle_mic_mute():
    subprocess.run(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "toggle"], stderr=subprocess.DEVNULL)

def get_initial_audio():
    def get_sv():
        try:
            out = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
            m = re.search(r'/\s*(\d+)%', out)
            return int(m.group(1)) if m else 50
        except Exception:
            return 50

    def get_sm():
        try:
            out = subprocess.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL, text=True)
            return "yes" in out.lower()
        except Exception:
            return False

    def get_mv():
        try:
            out = subprocess.check_output(["pactl", "get-source-volume", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
            m = re.search(r'/\s*(\d+)%', out)
            return int(m.group(1)) if m else 80
        except Exception:
            return 80

    def get_mm():
        try:
            out = subprocess.check_output(["pactl", "get-source-mute", "@DEFAULT_SOURCE@"], stderr=subprocess.DEVNULL, text=True)
            return "yes" in out.lower()
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        f_sv = ex.submit(get_sv)
        f_sm = ex.submit(get_sm)
        f_mv = ex.submit(get_mv)
        f_mm = ex.submit(get_mm)
        return f_sv.result(), f_sm.result(), f_mv.result(), f_mm.result()
