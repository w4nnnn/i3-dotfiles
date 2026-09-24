#!/usr/bin/env bash

export PATH="$HOME/.local/bin:$PATH"

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

# Launch Polybar, using default config location ~/.config/polybar/config.ini
polybar main >> /tmp/polybar.log 2>&1 &

# Calculate dynamic screen viewport dimensions for xcorners
SCREEN_H=$(xrandr --current 2>/dev/null | grep '\*' | awk '{print $1}' | cut -d'x' -f2 | head -n 1)
SCREEN_W=$(xrandr --current 2>/dev/null | grep '\*' | awk '{print $1}' | cut -d'x' -f1 | head -n 1)
SCREEN_H=${SCREEN_H:-768}
SCREEN_W=${SCREEN_W:-1366}
BAR_H=36
CORNER_H=$((SCREEN_H - BAR_H))

# Launch xcorners for rounded screen viewport corners (radius matches window corner-radius: 12)
"$HOME/.local/bin/xcorners" -W "$SCREEN_W" -H "$CORNER_H" -y "$BAR_H" -r 12 -c 1e1e2eff -t -b -1 >/dev/null 2>&1 &
