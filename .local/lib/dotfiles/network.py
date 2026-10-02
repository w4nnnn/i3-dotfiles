"""
Wi-Fi networking backend via NetworkManager nmcli.
Handles network scanning, connection, password authentication, and radio toggle.
"""
import os
import re
import shutil
import subprocess

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return ""

def scan_networks(rescan=False):
    devs = run_cmd(["nmcli", "-t", "-f", "DEVICE,TYPE,STATE,CONNECTION", "dev"]).splitlines()
    wifi_dev = ""
    active_ssid = ""
    active_ip = ""

    for line in devs:
        parts = line.split(":")
        if len(parts) >= 2 and parts[1] == "wifi":
            wifi_dev = parts[0]
            if len(parts) >= 4 and parts[2] == "connected":
                active_ssid = parts[3]
            break

    radio_state = run_cmd(["nmcli", "radio", "wifi"]) == "enabled"

    if active_ssid and wifi_dev:
        ip_out = run_cmd(["ip", "-4", "addr", "show", wifi_dev])
        m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", ip_out)
        if m:
            active_ip = m.group(1)

    nets = []
    if radio_state and wifi_dev:
        if rescan:
            run_cmd(["nmcli", "dev", "wifi", "rescan"])
        raw_out = run_cmd(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY,CHAN", "dev", "wifi", "list", "--rescan", "no"])
        if not raw_out.strip():
            raw_out = run_cmd(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY,CHAN", "dev", "wifi", "list"])

        raw_nets = {}
        for line in raw_out.splitlines():
            if not line:
                continue
            p = line.split(":")
            if len(p) < 5:
                continue
            in_use = p[0].strip() == "*"
            ssid = p[1].strip()
            if not ssid:
                continue
            sig_int = int(p[2]) if p[2].isdigit() else 0
            sec = p[3].strip()
            chan_int = int(p[4]) if p[4].isdigit() else 1

            if ssid not in raw_nets or in_use or sig_int > raw_nets[ssid]["signal"]:
                raw_nets[ssid] = {
                    "in_use": in_use,
                    "ssid": ssid,
                    "signal": sig_int,
                    "security": sec,
                    "chan": chan_int,
                }

        nets = sorted(raw_nets.values(), key=lambda x: (not x["in_use"], -x["signal"]))

    return wifi_dev, radio_state, active_ssid, active_ip, nets

def connect_saved_or_open(target, is_open):
    saved = run_cmd(["nmcli", "-t", "-f", "NAME", "c", "show"]).splitlines()
    if target in saved:
        res = subprocess.run(["nmcli", "con", "up", "id", target], capture_output=True)
        return res.returncode == 0, "saved"
    elif is_open:
        res = subprocess.run(["nmcli", "dev", "wifi", "connect", target], capture_output=True)
        if res.returncode == 0:
            portal_bin = shutil.which("portal-login") or os.path.expanduser("~/.local/bin/portal-login")
            if os.path.exists(portal_bin):
                subprocess.Popen([portal_bin, "--auto"])
            return True, "open"
        return False, "open"
    return None, "requires_password"

def connect_with_password(target, password):
    cmd = ["nmcli", "dev", "wifi", "connect", target, "password", password]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, res.stderr or res.stdout

def disconnect_active(active_ssid):
    if active_ssid:
        subprocess.run(["nmcli", "con", "down", "id", active_ssid], stderr=subprocess.DEVNULL)

def toggle_wifi_radio(current_state):
    target = "off" if current_state else "on"
    subprocess.run(["nmcli", "radio", "wifi", target], stderr=subprocess.DEVNULL)
    return not current_state

def open_captive_portal():
    portal_bin = shutil.which("portal-login") or os.path.expanduser("~/.local/bin/portal-login")
    if os.path.exists(portal_bin):
        subprocess.Popen([portal_bin])
