# Dotfiles Potential Issues & Bug Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve identified edge cases and bugs across i3wm configuration, GTK popups, threading, resolution detection, dependencies, and polybar font handling.

**Architecture:**
- Align window title rules in i3 config and picom rules for `AudioSelectorMenu` and `CatppuccinBluetoothMenu`.
- Make `network-menu` row activation asynchronous using worker thread to avoid blocking the GTK UI loop on `nmcli`.
- Detect active display resolution dynamically via `xrandr` in `lockscreen` and `wallpaper-selector` instead of hardcoding 1080p.
- Clean up `toggle-scratchpad` to use native i3 scratchpad show/hide IPC without fragile `xdotool` logic, and add missing packages (`dex`, `xdotool`, `noto-fonts-emoji`) to `install.sh`.
- Configure `Noto Color Emoji` fallback font in Polybar.
- Add `grab_seat` / `is_click_outside` to `calendar-popup` so clicking desktop or polybar dismisses it.

**Tech Stack:** i3wm, Python 3 / GTK3, Bash, Picom, Polybar, ImageMagick, NetworkManager.

## Global Constraints
- All modified and created files must remain strictly under 500 lines of code.
- Must verify syntax and run unit/sanity checks on each modified component before committing.

---

### Task 1: Fix Window Rules (`AudioSelectorMenu` & `CatppuccinBluetoothMenu`)

**Files:**
- Modify: `.config/i3/config`
- Modify: `.config/picom/picom.conf`

- [ ] **Step 1: Update `.config/i3/config` for `AudioSelectorMenu`**
  Change line `for_window [title="AudioOutputSelector"] floating enable, border none` to support `AudioSelectorMenu` (or regex `(?i)(AudioOutputSelector|AudioSelectorMenu)`). Also preserve Tauon / VSCode / Steam border pixel rules.

- [ ] **Step 2: Update `.config/picom/picom.conf` for `CatppuccinBluetoothMenu`**
  Add `name = 'CatppuccinBluetoothMenu'` to the corner-radius exclusion rule in `picom.conf`.

- [ ] **Step 3: Verify syntax**
  Run: `i3 -C -c .config/i3/config`
  Expected: exit 0.

---

### Task 2: Asynchronous Wi-Fi Connection in `network-menu`

**Files:**
- Modify: `.local/bin/network-menu`

- [ ] **Step 1: Wrap `connect_saved_or_open` in a worker thread**
  In `on_row_activated` of `RofiStyleNetworkWindow`, run the connection call inside `threading.Thread(target=worker, daemon=True).start()`. Dispatch notifications and `refresh_state()` back to the GTK main loop using `GLib.idle_add`.

- [ ] **Step 2: Verify Python compilation**
  Run: `python3 -m py_compile .local/bin/network-menu`
  Expected: exit 0.

---

### Task 3: Dynamic Display Resolution in Lockscreen & Wallpaper Blur

**Files:**
- Modify: `.local/bin/lockscreen`
- Modify: `.local/bin/wallpaper-selector`

- [ ] **Step 1: Dynamically determine resolution in `.local/bin/lockscreen`**
  Query `xrandr --current` for active resolution (e.g. `1366x768`), falling back to `1920x1080` if unavailable, and pass `${SCREEN_W}x${SCREEN_H}` to `magick`.

- [ ] **Step 2: Dynamically determine resolution in `.local/bin/wallpaper-selector`**
  Similarly query `xrandr --current` before pre-rendering `lockscreen_blur.png`.

- [ ] **Step 3: Verify bash syntax**
  Run: `bash -n .local/bin/lockscreen && bash -n .local/bin/wallpaper-selector`
  Expected: exit 0.

---

### Task 4: Robust Scratchpad Toggle & Package List Updates

**Files:**
- Modify: `.local/bin/toggle-scratchpad`
- Modify: `install.sh`

- [ ] **Step 1: Refactor `.local/bin/toggle-scratchpad`**
  Use `i3-msg '[instance="scratchpad_term"] scratchpad show'` directly. If exit code/IPC indicates no such container exists, spawn `kitty --name scratchpad_term &`.

- [ ] **Step 2: Add missing packages to `install.sh`**
  Add `dex`, `xdotool`, and `noto-fonts-emoji` to `install.sh` `PACKAGES` array.

- [ ] **Step 3: Verify script syntax**
  Run: `bash -n .local/bin/toggle-scratchpad && bash -n install.sh`
  Expected: exit 0.

---

### Task 5: Fallback Emoji Font in Polybar

**Files:**
- Modify: `.config/polybar/config.ini`

- [ ] **Step 1: Add `font-5 = "Noto Color Emoji:scale=10;3"` to `.config/polybar/config.ini`**
  Place fallback emoji font in `[bar/main]`.

- [ ] **Step 2: Verify polybar configuration**
  Run: `polybar -c .config/polybar/config.ini -m`
  Expected: no syntax error.

---

### Task 6: Seat Grab and Click-Outside in `calendar-popup`

**Files:**
- Modify: `.local/bin/calendar-popup`

- [ ] **Step 1: Import `grab_seat`, `ungrab_seat`, `is_click_outside` from `dotfiles.gtk_utils`**
  In `calendar-popup`, connect `map-event` to `grab_seat(self)`, and `button-press-event` to `is_click_outside(self, event) -> self.close_and_exit()`. Ensure `ungrab_seat()` is called in `close_and_exit()`.

- [ ] **Step 2: Verify Python compilation**
  Run: `python3 -m py_compile .local/bin/calendar-popup`
  Expected: exit 0.

---

### Task 7: Full Verification & Line Count Checks

- [ ] **Step 1: Check line counts**
  Ensure all touched files are strictly under 500 lines.

- [ ] **Step 2: Reload i3 and services**
  Run `i3-msg reload` and test execution of all modified scripts.
