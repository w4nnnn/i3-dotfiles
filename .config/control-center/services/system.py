"""
System identity, uptime, and hardware telemetry services.
"""
import os
import socket

_prev_idle = 0
_prev_total = 0

def get_username():
    return os.getenv("USER", "user")

def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "archlinux"

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            up_sec = int(float(f.readline().split()[0]))
        days = up_sec // 86400
        hours = (up_sec % 86400) // 3600
        mins = (up_sec % 3600) // 60
        res = []
        if days > 0:
            res.append(f"{days}d")
        if hours > 0:
            res.append(f"{hours}h")
        res.append(f"{mins}m")
        return " ".join(res)
    except Exception:
        return "Active"

def get_cpu_info():
    global _prev_idle, _prev_total
    try:
        with open("/proc/stat") as f:
            fields = [float(x) for x in f.readline().strip().split()[1:]]
        idle = fields[3] + fields[4]
        total = sum(fields)
        if _prev_total > 0:
            d_idle = idle - _prev_idle
            d_total = total - _prev_total
            usage = int((1.0 - d_idle / d_total) * 100) if d_total > 0 else 0
        else:
            usage = 18
        _prev_idle, _prev_total = idle, total
        usage = max(0, min(100, usage))
    except Exception:
        usage = 20

    cpu_brand = "CPU"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    m = line.split(":", 1)[1].strip()
                    if "Intel" in m:
                        cpu_brand = "Intel"
                    elif "AMD" in m:
                        cpu_brand = "AMD"
                    else:
                        cpu_brand = m.split()[0]
                    break
    except Exception:
        pass
    return usage, cpu_brand

def get_ram_info():
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem[parts[0].strip()] = int(parts[1].strip().split()[0])
        total = mem.get("MemTotal", 1) / (1024 * 1024)
        avail = mem.get("MemAvailable", mem.get("MemFree", 0)) / (1024 * 1024)
        used = total - avail
        pct = int((used / total) * 100) if total > 0 else 0
        return f"{used:.1f} GB", pct, used / total
    except Exception:
        return "2.0 GB", 25, 0.25

def get_battery_and_temp():
    bat_cap = 100
    bat_stat = "Full"
    has_bat = False
    ps = "/sys/class/power_supply"
    if os.path.exists(ps):
        for entry in sorted(os.listdir(ps)):
            if entry.startswith("BAT"):
                try:
                    cap_f = os.path.join(ps, entry, "capacity")
                    stat_f = os.path.join(ps, entry, "status")
                    if os.path.exists(cap_f):
                        bat_cap = int(open(cap_f).read().strip())
                        has_bat = True
                    if os.path.exists(stat_f):
                        bat_stat = open(stat_f).read().strip()
                    break
                except Exception:
                    pass

    temp_c = 45
    tz = "/sys/class/thermal"
    if os.path.exists(tz):
        for zone in os.listdir(tz):
            if zone.startswith("thermal_zone"):
                try:
                    t = int(open(os.path.join(tz, zone, "temp")).read().strip()) // 1000
                    if 20 <= t <= 115:
                        temp_c = t
                        break
                except Exception:
                    pass

    return has_bat, bat_cap, bat_stat, temp_c
