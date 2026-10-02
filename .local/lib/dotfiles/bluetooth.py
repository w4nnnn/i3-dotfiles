"""
Bluetooth backend via D-Bus (org.bluez) and bluetoothctl.
Handles adapter discovery, device parsing, connection, pairing, and disconnection.
"""
import subprocess
import time
import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

def get_device_icon(icon_str, name):
    name_lower = name.lower()
    if any(w in name_lower for w in ["headphone", "headset", "earphone", "buds", "airpod", "wh-", "wf-"]):
        return "󰋋"
    if any(w in name_lower for w in ["speaker", "soundbar", "audio", "jbl", "bose", "echo"]):
        return "󰓃"
    if any(w in name_lower for w in ["mouse", "trackpad"]):
        return "󰍽"
    if any(w in name_lower for w in ["keyboard", "keychron"]):
        return "󰌌"
    if any(w in name_lower for w in ["gamepad", "controller", "xbox", "ps4", "ps5", "dualshock"]):
        return "󰊴"
    if any(w in name_lower for w in ["phone", "galaxy", "iphone", "pixel", "redmi", "xiaomi"]):
        return "󰏲"
    if any(w in name_lower for w in ["watch", "band", "fit"]):
        return "󰂵"
    if any(w in name_lower for w in ["tv", "smart tv", "bravia", "roku", "basemen"]):
        return "󰍹"
    if any(w in name_lower for w in ["pc", "laptop", "desktop", "macbook"]):
        return "󰌢"

    if "audio" in icon_str or "headset" in icon_str:
        return "󰋋"
    if "input-mouse" in icon_str:
        return "󰍽"
    if "input-keyboard" in icon_str:
        return "󰌌"
    if "input-gaming" in icon_str:
        return "󰊴"
    if "phone" in icon_str:
        return "󰏲"
    if "computer" in icon_str:
        return "󰌢"

    return "󰂯"

def fetch_bluetooth_state(bus):
    powered = False
    adapter_path = None
    devices = []

    if bus:
        try:
            om = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.bluez", "/", "org.freedesktop.DBus.ObjectManager", None
            )
            managed = om.GetManagedObjects()

            for path, ifaces in managed.items():
                if "org.bluez.Adapter1" in ifaces:
                    adapter_path = path
                    powered = bool(ifaces["org.bluez.Adapter1"].get("Powered", False))
                    break

            for path, ifaces in managed.items():
                if "org.bluez.Device1" in ifaces:
                    d = ifaces["org.bluez.Device1"]
                    bat = ifaces.get("org.bluez.Battery1", {}).get("Percentage", None)
                    name = d.get("Alias", d.get("Name", d.get("Address", "Unknown")))
                    addr = d.get("Address", "")
                    paired = bool(d.get("Paired", False))
                    connected = bool(d.get("Connected", False))
                    trusted = bool(d.get("Trusted", False))
                    icon_name = d.get("Icon", "bluetooth")
                    rssi = d.get("RSSI", 0)

                    devices.append({
                        "path": path,
                        "name": name,
                        "address": addr,
                        "paired": paired,
                        "connected": connected,
                        "trusted": trusted,
                        "icon": icon_name,
                        "rssi": rssi,
                        "battery": bat,
                    })
        except Exception:
            pass

    if not adapter_path:
        try:
            out = subprocess.check_output(["bluetoothctl", "show"], stderr=subprocess.DEVNULL, text=True)
            powered = "Powered: yes" in out
        except Exception:
            powered = False

    devices.sort(key=lambda x: (not x["connected"], not x["paired"], -x["rssi"]))
    return powered, adapter_path, devices

def connect_device(bus, dev):
    success = False
    if bus and dev.get("path"):
        try:
            d_proxy = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.bluez", dev["path"], "org.bluez.Device1", None
            )
            d_proxy.Connect()
            success = True
        except Exception:
            pass

    if not success:
        res = subprocess.run(["bluetoothctl", "connect", dev["address"]], capture_output=True, text=True)
        success = "Connection successful" in res.stdout or res.returncode == 0
    return success

def pair_device(dev):
    subprocess.run(["bluetoothctl", "trust", dev["address"]], capture_output=True)
    res_pair = subprocess.run(["bluetoothctl", "pair", dev["address"]], capture_output=True, text=True)
    res_conn = subprocess.run(["bluetoothctl", "connect", dev["address"]], capture_output=True, text=True)
    return "successful" in res_conn.stdout or "Connection successful" in res_pair.stdout or res_conn.returncode == 0

def disconnect_device(bus, dev):
    success = False
    if bus and dev.get("path"):
        try:
            d_proxy = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.bluez", dev["path"], "org.bluez.Device1", None
            )
            d_proxy.Disconnect()
            success = True
        except Exception:
            pass

    if not success:
        subprocess.run(["bluetoothctl", "disconnect", dev["address"]], stderr=subprocess.DEVNULL)
    return True

def set_adapter_discovery(bus, adapter_path, enable):
    if bus and adapter_path:
        try:
            adapter = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.bluez", adapter_path, "org.bluez.Adapter1", None
            )
            if enable:
                adapter.StartDiscovery()
            else:
                adapter.StopDiscovery()
            return
        except Exception:
            pass

    if enable:
        subprocess.Popen(["bluetoothctl", "--timeout", "15", "scan", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["bluetoothctl", "scan", "off"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def set_adapter_power(bus, adapter_path, target):
    if target:
        subprocess.run(["rfkill", "unblock", "bluetooth"], stderr=subprocess.DEVNULL)
        time.sleep(0.1)

    if bus and adapter_path:
        try:
            adapter_prop = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.bluez", adapter_path, "org.freedesktop.DBus.Properties", None
            )
            adapter_prop.Set("(ssv)", "org.bluez.Adapter1", "Powered", GLib.Variant.new_boolean(target))
            return
        except Exception:
            pass

    cmd = "on" if target else "off"
    subprocess.run(["bluetoothctl", "power", cmd], stderr=subprocess.DEVNULL)
