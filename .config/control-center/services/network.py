"""
Wi-Fi networking service via nmcli / rfkill.
"""
import glob
import os
import subprocess

def get_wifi_status():
    try:
        out = subprocess.check_output(["nmcli", "radio", "wifi"], stderr=subprocess.DEVNULL, text=True).strip()
        return out.lower() == "enabled"
    except Exception:
        pass

    for path in glob.glob("/sys/class/rfkill/rfkill*"):
        try:
            with open(os.path.join(path, "type")) as f:
                if f.read().strip() == "wlan":
                    with open(os.path.join(path, "soft")) as sf:
                        s = sf.read().strip() == "1"
                    with open(os.path.join(path, "hard")) as hf:
                        h = hf.read().strip() == "1"
                    return not (s or h)
        except Exception:
            pass
    return True

def toggle_wifi():
    is_on = get_wifi_status()
    cmd = "off" if is_on else "on"
    subprocess.run(["nmcli", "radio", "wifi", cmd], stderr=subprocess.DEVNULL)
    return not is_on
