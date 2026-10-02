"""
Bluetooth service via native D-Bus (org.bluez) and rfkill.
"""
import subprocess
import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

def get_bluetooth_status():
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        om = Gio.DBusProxy.new_sync(
            bus, Gio.DBusProxyFlags.NONE, None,
            "org.bluez", "/", "org.freedesktop.DBus.ObjectManager", None
        )
        for path, ifaces in om.GetManagedObjects().items():
            if "org.bluez.Adapter1" in ifaces:
                return bool(ifaces["org.bluez.Adapter1"].get("Powered", False))
    except Exception:
        pass

    try:
        out = subprocess.check_output(["bluetoothctl", "show"], stderr=subprocess.DEVNULL, text=True)
        return "Powered: yes" in out
    except Exception:
        return False

def toggle_bluetooth():
    is_on = get_bluetooth_status()
    target_state = not is_on

    if target_state:
        subprocess.run(["rfkill", "unblock", "bluetooth"], stderr=subprocess.DEVNULL)

    try:
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        om = Gio.DBusProxy.new_sync(
            bus, Gio.DBusProxyFlags.NONE, None,
            "org.bluez", "/", "org.freedesktop.DBus.ObjectManager", None
        )
        for path, ifaces in om.GetManagedObjects().items():
            if "org.bluez.Adapter1" in ifaces:
                adapter = Gio.DBusProxy.new_sync(
                    bus, Gio.DBusProxyFlags.NONE, None,
                    "org.bluez", path, "org.freedesktop.DBus.Properties", None
                )
                adapter.Set("(ssv)", "org.bluez.Adapter1", "Powered", GLib.Variant.new_boolean(target_state))
                return target_state
    except Exception:
        pass

    cmd = "on" if target_state else "off"
    subprocess.run(["bluetoothctl", "power", cmd], stderr=subprocess.DEVNULL)
    return target_state
