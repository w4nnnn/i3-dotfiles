#!/usr/bin/env bash

export PATH="$HOME/.local/bin:$PATH"

# Terminate already running bar and corner instances
killall -q polybar
killall -q xcorners

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 0.2; done

# Launch Polybar, using default config location ~/.config/polybar/config.ini
polybar main >> /tmp/polybar.log 2>&1 &

# Launch xcorners for rounded screen viewport corners (radius matches picom corner-radius: 12)
"$HOME/.local/bin/xcorners" -y 36 -H 1044 -r 12 -c 1e1e2eff -t -b -1 >/dev/null 2>&1 &
