#!/usr/bin/env bash

export PATH="$HOME/.local/bin:$PATH"
unset DESKTOP_STARTUP_ID

# Terminate already running bar and corner instances
killall -q polybar
killall -q xcorners

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 0.2; done

# Auto-detect battery and adapter for laptop support
BAT_DEV=""
for b in /sys/class/power_supply/BAT* /sys/class/power_supply/battery*; do
    if [ -d "$b" ] && [ "$(cat "$b/type" 2>/dev/null)" = "Battery" ]; then
        BAT_DEV="$(basename "$b")"
        break
    fi
done

ADAP_DEV=""
for a in /sys/class/power_supply/AC* /sys/class/power_supply/ADP* /sys/class/power_supply/acad*; do
    if [ -d "$a" ]; then
        ADAP_DEV="$(basename "$a")"
        break
    fi
done

if [ -n "$BAT_DEV" ]; then
    export POLYBAR_BATTERY="$BAT_DEV"
    export POLYBAR_ADAPTER="${ADAP_DEV:-ACAD}"
    # Start battery alert daemon for laptops if not running
    if ! pgrep -f "battery-alert" >/dev/null 2>&1; then
        "$HOME/.local/bin/battery-alert" &
    fi
else
    export POLYBAR_BATTERY="NONE"
    export POLYBAR_ADAPTER="NONE"
fi

# Launch Polybar for each connected monitor (or single fallback)
if command -v xrandr >/dev/null 2>&1; then
    for m in $(polybar -m 2>/dev/null | cut -d":" -f1); do
        MONITOR=$m polybar main >> /tmp/polybar.log 2>&1 &
    done
else
    polybar main >> /tmp/polybar.log 2>&1 &
fi

# Read dynamic base background color from colors.ini for xcorners
BASE_HEX="1e1e2e"
if [ -f "$HOME/.config/polybar/colors.ini" ]; then
    DETECTED_HEX=$(grep -E '^[[:space:]]*base[[:space:]]*=' "$HOME/.config/polybar/colors.ini" | head -n 1 | awk '{print $3}' | tr -d '#' | tr -d ' ')
    if [ -n "$DETECTED_HEX" ]; then
        BASE_HEX="$DETECTED_HEX"
    fi
fi
CORNER_COLOR="${BASE_HEX}ff"

# Launch xcorners dynamically for all connected monitors (supports 768p, 1080p, 2K, 4K, & multi-monitor)
CORNERS_LAUNCHED=0
while IFS= read -r line; do
    if [[ "$line" =~ ([^:]+):[[:space:]]*([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+) ]]; then
        M_NAME="${BASH_REMATCH[1]}"
        M_W="${BASH_REMATCH[2]}"
        M_H="${BASH_REMATCH[3]}"
        M_X="${BASH_REMATCH[4]}"
        M_Y="${BASH_REMATCH[5]}"
        VIEWPORT_H=$((M_H - 36))
        VIEWPORT_Y=$((M_Y + 36))

        "$HOME/.local/bin/xcorners" -x "$M_X" -y "$VIEWPORT_Y" -W "$M_W" -H "$VIEWPORT_H" -r 12 -c "$CORNER_COLOR" -t -b >/dev/null 2>&1 &
        CORNERS_LAUNCHED=1
    fi
done < <(polybar -m 2>/dev/null)

# Fallback if polybar -m is unavailable
if [ "$CORNERS_LAUNCHED" -eq 0 ]; then
    SCREEN_W=$(xrandr --current 2>/dev/null | grep -oP '\d+(?=x\d+\s+.*\*)' | head -n 1)
    SCREEN_H=$(xrandr --current 2>/dev/null | grep -oP '\d+x\K\d+(?=\s+.*\*)' | head -n 1)
    SCREEN_W="${SCREEN_W:-1366}"
    SCREEN_H="${SCREEN_H:-768}"
    VIEWPORT_H=$((SCREEN_H - 36))
    "$HOME/.local/bin/xcorners" -W "$SCREEN_W" -H "$VIEWPORT_H" -y 36 -r 12 -c "$CORNER_COLOR" -t -b -1 >/dev/null 2>&1 &
fi
