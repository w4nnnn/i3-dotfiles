"""
Display brightness control service via brightnessctl / xbacklight / sysfs.
"""
import glob
import os
import subprocess

def get_brightness():
    try:
        out = subprocess.check_output(["brightnessctl", "g"], stderr=subprocess.DEVNULL, text=True).strip()
        max_b = subprocess.check_output(["brightnessctl", "m"], stderr=subprocess.DEVNULL, text=True).strip()
        if out and max_b:
            cur = int(out)
            mx = int(max_b)
            return int((cur / mx) * 100)
    except Exception:
        pass

    for path in glob.glob("/sys/class/backlight/*"):
        try:
            with open(os.path.join(path, "brightness")) as f:
                cur = int(f.read().strip())
            with open(os.path.join(path, "max_brightness")) as f:
                mx = int(f.read().strip())
            return int((cur / mx) * 100)
        except Exception:
            pass

    return 75

def set_brightness(val):
    val = max(1, min(100, int(val)))
    try:
        subprocess.run(["brightnessctl", "s", f"{val}%"], stderr=subprocess.DEVNULL)
        return
    except Exception:
        pass

    try:
        subprocess.run(["xbacklight", "-set", str(val)], stderr=subprocess.DEVNULL)
    except Exception:
        pass
