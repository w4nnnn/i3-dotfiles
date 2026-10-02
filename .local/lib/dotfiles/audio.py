"""
Audio output sink discovery, device switching, and audio chime feedback.
"""
import math
import struct
import subprocess
from .gtk_utils import notify

def play_test_chime():
    """Generates a pleasant 440+880Hz audio chime to test the active audio device."""
    try:
        sample_rate = 44100
        duration = 0.25
        samples = []
        for i in range(int(sample_rate * duration)):
            tm = i / sample_rate
            env = math.exp(-6 * tm)
            val = (math.sin(2 * math.pi * 523.25 * tm) * 0.6 + math.sin(2 * math.pi * 659.25 * tm) * 0.4) * env
            samples.append(int(val * 16383))

        raw_bytes = struct.pack("<" + "h" * len(samples), *samples)
        p = subprocess.Popen(
            ["paplay", "--raw", "--rate=44100", "--channels=1", "--format=s16le"],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        p.communicate(input=raw_bytes)
    except Exception:
        pass

def get_audio_outputs():
    try:
        out = subprocess.check_output(["pactl", "list", "sinks"], stderr=subprocess.DEVNULL, text=True)
        def_sink = subprocess.check_output(["pactl", "get-default-sink"], stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return []

    sinks = []
    curr = None
    in_ports = False

    for line in out.splitlines():
        line_s = line.strip()
        if line.startswith("Sink #"):
            if curr and "name" in curr:
                sinks.append(curr)
            curr = {"ports": {}}
            in_ports = False
        elif not curr:
            continue
        elif line_s.startswith("Name:"):
            curr["name"] = line_s.split(":", 1)[1].strip()
        elif line_s.startswith("Description:"):
            curr["desc"] = line_s.split(":", 1)[1].strip()
        elif line_s.startswith("Active Port:"):
            curr["active_port"] = line_s.split(":", 1)[1].strip()
            in_ports = False
        elif line_s.startswith("Ports:"):
            in_ports = True
        elif in_ports:
            if ":" in line_s:
                pname = line_s.split(":", 1)[0].strip()
                pdesc = line_s.split(":", 1)[1].strip().split("(")[0].strip()
                curr["ports"][pname] = pdesc
            else:
                in_ports = False

    if curr and "name" in curr:
        sinks.append(curr)

    outputs = []
    for s in sinks:
        sink_name = s.get("name", "")
        sink_desc = s.get("desc", sink_name)
        active_port = s.get("active_port", "")
        ports = s.get("ports", {})
        is_def_sink = (sink_name == def_sink)

        if len(ports) > 1:
            for pname, pdesc in ports.items():
                is_active = is_def_sink and (pname == active_port)
                icon = "󰓃"
                p_lower = pname.lower() + " " + pdesc.lower()
                category = "Speaker"
                if "headphone" in p_lower:
                    icon = "󰋋"
                    category = "Headphones"
                elif "speaker" in p_lower:
                    icon = "󰓃"
                    category = "Speakers"
                elif "hdmi" in p_lower or "displayport" in p_lower:
                    icon = "󰡁"
                    category = "Monitor / TV"
                elif "bluetooth" in p_lower or "bluez" in p_lower:
                    icon = "󰂯"
                    category = "Bluetooth Audio"

                clean_title = pdesc if pdesc else pname
                outputs.append({
                    "type": "port",
                    "sink_name": sink_name,
                    "port_name": pname,
                    "title": clean_title,
                    "subtitle": f"{sink_desc} • Port: {pname}",
                    "full_label": f"{sink_desc} ({clean_title})",
                    "icon": icon,
                    "category": category,
                    "is_active": is_active,
                })
        else:
            icon = "󰓃"
            s_lower = sink_name.lower() + " " + sink_desc.lower()
            category = "Audio Device"
            if "bluez" in s_lower or "bluetooth" in s_lower or "headset" in s_lower or "tws" in s_lower:
                icon = "󰂯"
                category = "Bluetooth Audio"
            elif "hdmi" in s_lower or "displayport" in s_lower:
                icon = "󰡁"
                category = "HDMI / DisplayPort"
            elif "headphone" in s_lower:
                icon = "󰋋"
                category = "Headphones"
            elif "usb" in s_lower:
                icon = "󰝚"
                category = "USB Audio Interface"

            short_name = sink_desc
            for rem in ["Analog Stereo", "Digital Stereo (HDMI)", "Digital Stereo", "Audio Controller"]:
                if rem in short_name and len(short_name) > len(rem) + 3:
                    short_name = short_name.replace(rem, "").strip()

            outputs.append({
                "type": "sink",
                "sink_name": sink_name,
                "port_name": None,
                "title": short_name,
                "subtitle": sink_desc,
                "full_label": sink_desc,
                "icon": icon,
                "category": category,
                "is_active": is_def_sink,
            })

    return outputs

def set_audio_output(output_info):
    sink_name = output_info["sink_name"]
    port_name = output_info.get("port_name")
    try:
        subprocess.run(["pactl", "set-default-sink", sink_name], stderr=subprocess.DEVNULL)
        if port_name:
            subprocess.run(["pactl", "set-sink-port", sink_name, port_name], stderr=subprocess.DEVNULL)
        # Migrate all active sink inputs
        inputs = subprocess.check_output(["pactl", "list", "short", "sink-inputs"], stderr=subprocess.DEVNULL, text=True)
        for line in inputs.splitlines():
            if line.strip():
                inp_id = line.split()[0]
                subprocess.run(["pactl", "move-sink-input", inp_id, sink_name], stderr=subprocess.DEVNULL)
    except Exception:
        pass

    icon = "audio-speakers"
    if "󰋋" in output_info.get("icon", ""):
        icon = "audio-headphones"
    elif "󰂯" in output_info.get("icon", ""):
        icon = "audio-headset"
    elif "󰡁" in output_info.get("icon", ""):
        icon = "video-display"

    notify("Audio", "Audio Output Switched", f"Active: {output_info.get('full_label', output_info.get('title'))}", icon=icon, tag="audio_sink")
