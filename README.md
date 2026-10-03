# ☕ Catppuccin Mocha i3wm Dotfiles

A modern, cohesive, and aesthetic **i3wm** rice built on **Arch Linux** themed in **Catppuccin Mocha (Mauve accent)** with comprehensive multi-theme support. Designed with fluid animations, interactive system menus, modular architecture (< 500 LOC per file), and Hyprland-inspired dynamic tiling.

---

## ✨ Features & Highlights

- **Window Manager**: `i3wm` with static minimal gaps (`6px inner`, `2px outer`), rounded corners (`12px`), and smart auto-tiling (`i3-autotile` Fibonacci/spiral split like Hyprland).
- **Responsive Dynamic File Dialog Sizing**: Real-time display geometry detection via i3 IPC in `i3-autotile`. Floating file pickers and save dialogs (`GtkFileChooserDialog`, `xdg-desktop-portal`, etc.) automatically scale proportionally (~62% width clamped to 700–1280px, ~68% height clamped to 460–800px) and center on the active monitor, preventing oversized overflow or hidden action buttons on laptop screens (720p/768p) and multi-monitor setups.
- **Isolated Workspace App Launching**: Clean environment isolation (`--no-startup-id` across all keybindings and automatic `DESKTOP_STARTUP_ID` sanitization) ensuring external apps (Brave, Steam, Nemo, Kitty, etc.) always spawn on the currently focused workspace instead of locking to Workspace 1.
- **System-Wide Dark & Light Theme Categorization**:
  - Themes are grouped into **Dark Mode** (9 themes) and **Light Mode** (Paper Light).
  - Automatically synchronizes `org.gnome.desktop.interface color-scheme` (`prefer-dark` vs `prefer-light`), GTK themes (`catppuccin-mocha` vs `Adwaita`), icon themes (`Papirus-Dark` vs `Papirus-Light`), and browser native Classic engine (Brave / Chromium) to avoid broken CSS and white-on-white text glitches.
- **Inverted Screen Corners**: Custom Cairo/XFixes utility (`xcorners`) providing concave rounded screen corners underneath the docked top bar, synchronized dynamically with active theme colors.
- **Top Status Bar**: `Polybar` configured with dynamic multi-monitor support and interactive modules:
  - **Arch Launcher (`󰣇`)**: Click to open Windows 11-style Start Menu (`win11-start`).
  - **Workspaces (`i3`)**: Dynamic workspaces with focused accent contrast and urgent indicators.
  - **Window Title (`xwindow`)**: Clean active window title with truncation (`30 chars`) or "Desktop" indicator.
  - **Date / Time (`date`)**: Lucide calendar (``) & clock (``). Click to open interactive floating `calendar-popup`.
  - **Network (`network`)**: Real-time link speed and status (`network-status-bar`). Left-click opens Modern GTK3 Network Manager (`network-menu`), middle-click triggers IP address notification (`network-info`), right-click opens `nmtui` in terminal.
  - **Battery (`battery`)**: Dynamic Lucide battery indicator with charging state (``) and capacity levels (``, ``). Click to open detailed battery statistics (`battery-info`). Paired with background alert daemon (`battery-alert`).
  - **System Tray (`tray`)**: Native system tray support for background apps (Discord, Steam, 9router, etc.) pinned to primary monitor.
  - **Control Center (`controlcenter`)**: Lucide slider icon (``). Click to open Quick Settings Control Center (`control-center`).
- **Control Center (Quick Settings)**: Floating GTK3 card (`Super + c`) inspired by Android / Windows 11:
  - Interactive volume & brightness sliders with live feedback.
  - Quick toggle tiles: Network (`󰤨`), Bluetooth (`󰂯`), DND (`󰂛`), Caffeine (``), Night Light (`󰖔`), Game Mode (`󰊴`), Project (``), Screenshot (`󰹑`), and Wallpaper (`󰸉`).
  - Mini media player with album/title controls (`playerctl`).
  - Interactive Theme Switcher button (``), Keybindings Cheatsheet button (`[⌨ Keybinds]`), and quick Power buttons.
- **Caffeine Anti-Sleep & Safe Shutdown**:
  - Keeps display and system awake by inhibiting only `idle:sleep` without blocking system poweroff or reboot.
  - Automatically turns off caffeine mode cleanly before shutdown and reboot in `powermenu`.
- **Audio Output Device Selector**: Standalone GTK3 quick switcher (`Super + Shift + a` or `Super + Alt + v` or Right-Click on Polybar / Control Center volume) to switch seamlessly between Internal Speakers, Headphones, Bluetooth TWS/Headsets, HDMI/DisplayPort TV/Monitors, and USB Audio DACs with automatic active stream migration and test chime.
- **Bluetooth Device Manager**: Standalone GTK3 modal (`Super + Shift + b` or Control Center tile) for scanning, pairing, connecting, trusting, and removing Bluetooth devices with D-Bus integration.
- **Screen Projection & Wireless Cast (Win+P Style)**: Dedicated presentation and display manager (`Super + p` / `XF86Display`):
  - Cable projection modes for projector/TV: `PC Screen Only`, `Duplicate / Mirror`, `Extend Right`, `Extend Left`, and `Second Screen Only`.
  - Built-in **Wireless Web Cast Server** streaming real-time desktop view over local Wi-Fi to any Smart TV, iPad, or browser via HTTP/MJPEG.
  - Automatic display rescan, polybar multi-monitor reload, GTK file chooser geometry sync, and wallpaper restoration upon display changes.
- **Windows 11-Style Start Menu**: Modern floating GTK3 App Launcher (`Super + a` / `Super + d`) with instant search filter, pinned apps, scrollable app grid, and power controls.
- **Modern GTK3 Wi-Fi Manager**: Clean network menu (`Super + n`) matching the desktop design system:
  - Pure SSID list with live signal strength, frequency tags (`2.4G` / `5GHz`), security flags (`SEC` / `OPEN`), and `CONNECTED` status badge.
  - Dedicated interactive action toolbar in the footer (`󰖟 Portal`, `󰅖 Disconnect`, `󰑐 Rescan`, `󰢻 Settings`, and dynamic `󰤮 Wifi Off` / `󰤨 Wifi On`).
  - In-place elegant password authentication modal with reveal eye toggle (`󰈈` / `󰈉`), error feedback, and background threading.
  - Global pointer seat grab with instant click-outside auto-dismissal.
- **On-Screen Display (OSD) Notifications**: Sleek progress bar overlay notifications for Volume and Brightness adjustments via Dunst. Notifications can be dismissed instantly with a right-click.
- **Dropdown Scratchpad Terminal**: Quick toggle floating terminal (`Super + \`` / `Super + -`) for instant command execution.
- **Wallpaper & Lockscreen Sync**: Dynamic wallpaper selector (`Super + Shift + w`) via Rofi with live thumbnails that automatically syncs the active desktop, pre-renders a **50% Gaussian blur** lockscreen canvas, and updates SDDM login background.
- **Lockscreen & Auto-Lock**: `i3lock-color` featuring Gaussian blurred wallpaper, high-contrast clock, responsive feedback indicator ring, and automatic locking after **5 minutes** of inactivity (AFK) via `xss-lock`.
- **Shell & Modern Terminal Stack (HyDE Inspired)**:
  - `ZSH` with `zsh-autosuggestions`, `zsh-syntax-highlighting`, and `fzf` history search.
  - `Starship` prompt customized with Catppuccin pastel colors and Arch glyphs (`󰣇`).
  - `Fastfetch` system information banner on terminal startup.
  - Modern CLI tools: `eza` (modern ls with icons), `bat` (syntax highlighting cat).
- **Terminal Emulator**: `Kitty` running Zsh with `JetBrainsMono Nerd Font`, 0.92 opacity, and full Catppuccin Mocha palette.
- **Compositor**: `Picom` with dual-kawase blur, rounded corners (`12px`), drop shadows, and smooth **Zoom / Scale Pop** workspace transitions.
- **Interactive Keybinds Viewer**: Searchable cheatsheet popup (`Super + /` / `Super + ?`) displaying all categorized system shortcuts.
- **Display Manager**: `SDDM` running the [SilentSDDM](https://github.com/uiriansan/SilentSDDM) theme (Catppuccin Mocha preset, matching blurred wallpaper, and persistent auto-sync with the wallpaper selector).
- **Modular Codebase (< 500 LOC)**: Refactored modular shared library in `.local/lib/dotfiles/` and componentized `.config/control-center/` widgets and services ensuring high maintainability and testability.

---

## ⌨️ Keybindings Cheat Sheet

### Application Launchers & Menus
| Keybinding | Action |
| :--- | :--- |
| **`Super + t`** / **`Super + Enter`** | Launch Kitty Terminal |
| **`Super + b`** | Launch Brave Browser |
| **`Super + e`** | Launch Nemo File Manager |
| **`Super + a`** / **`Super + d`** | Open Windows 11-Style Start Menu (App Launcher) |
| **`Super + Shift + d`** | Open Rofi Command Runner (`run`) |
| **`Super + v`** | Open Clipboard History (Greenclip + Rofi) |
| **`Super + Shift + v`** | Clear Clipboard History |
| **`Super + n`** | Open Modern GTK3 Network Manager |
| **`Super + Shift + n`** | Open Advanced Network Settings (nmtui in floating terminal) |
| **`Super + Shift + b`** | Open Bluetooth Device Manager (GTK3 Floating Modal) |
| **`Super + Shift + a`** / **`Super + Alt + v`** | Open Audio Output Device Selector |
| **`Super + p`** / **`XF86Display`** | Open Screen Project & Wireless Cast Menu |
| **`Super + c`** | Toggle Control Center (Quick Settings) |
| **`Super + Shift + m`** | Toggle Do Not Disturb (DND) |
| **`Super + Shift + w`** | Open Wallpaper Selector |
| **`Super + Shift + t`** | Open Global Theme Switcher |
| **`Super + /`** / **`Super + ?`** | Open Keybindings Cheatsheet Viewer |
| **`Super + \``** / **`Super + -`** | Toggle Dropdown Scratchpad Terminal |
| **`Super + Shift + -`** | Move focused window to Scratchpad |
| **`Super + Escape`** | Lock Screen (`i3lock-color`) |
| **`Super + Shift + e`** | Open Power Menu (Lock, Suspend, Logout, Reboot, Shutdown) |

### Window Management & Tiling
| Keybinding | Action |
| :--- | :--- |
| **`Super + q`** / **`Super + Shift + q`** | Close focused window |
| **`Super + f`** | Toggle Fullscreen |
| **`Super + Shift + Space`** | Toggle Floating window mode |
| **`Super + Space`** | Toggle focus between floating & tiled windows |
| **`Super + Tab`** | Switch between open windows (Rofi window switcher) |
| **`Super + h`** | Split layout horizontally |
| **`Super + Shift + h`** | Split layout vertically |
| **`Super + s`** | Switch layout to Stacking |
| **`Super + w`** | Switch layout to Tabbed |
| **`Super + x`** | Toggle split layout |
| **`Super + [Arrow Keys]`** / **`Super + j/k/l/;`** | Change window focus (Left, Down, Up, Right) |
| **`Super + Shift + [Arrow Keys]`** / **`Super + Shift + j/k/l/;`** | Move window container (Left, Down, Up, Right) |
| **`Super + 1 .. 0`** | Switch to Workspace 1 – 10 |
| **`Super + Shift + 1 .. 0`** | Move focused window to Workspace 1 – 10 |
| **`Super + r`** | Enter Resize mode (`Arrow Keys` or `j/k/l/;` to resize, `Esc`/`Enter` to exit) |
| **`Super + Shift + r`** | In-place Restart i3wm |
| **`Super + Shift + c`** | In-place Reload i3wm config |

### Hardware & Media Controls
| Keybinding | Action |
| :--- | :--- |
| **`XF86AudioRaiseVolume`** | Increase volume (+5%) with Dunst OSD |
| **`XF86AudioLowerVolume`** | Decrease volume (-5%) with Dunst OSD |
| **`XF86AudioMute`** | Toggle audio mute with Dunst OSD |
| **`XF86AudioMicMute`** | Toggle microphone mute |
| **`XF86MonBrightnessUp`** | Increase display brightness (+5%) with Dunst OSD |
| **`XF86MonBrightnessDown`** | Decrease display brightness (-5%) with Dunst OSD |
| **`XF86AudioPlay`** | Play / Pause media playback (`playerctl`) |
| **`XF86AudioNext`** | Next track (`playerctl`) |
| **`XF86AudioPrev`** | Previous track (`playerctl`) |
| **`Print`** | Screenshot selected area (saves to `~/Pictures/Screenshots` & clipboard) |
| **`Shift + Print`** | Screenshot entire screen |
| **`Ctrl + Print`** | Screenshot focused window |
| **`Alt + Print`** | Screenshot with 3-second delay |

---

## 🎨 Global Desktop Themes

Synchronize your entire desktop color scheme with a single click or shortcut. The theme switcher coordinates **Polybar**, **Rofi menus**, **i3wm window borders & indicators**, **Kitty terminal colors**, **Dunst notification frames**, **Control Center**, **Start Menu**, **Network Menu**, **GTK 2/3/4 themes**, **System Color Scheme (`prefer-dark` / `prefer-light`)**, **Browser Classic Mode (Brave/Chromium)**, and **Screen Corner Overlays (`xcorners`)**.

### 🌟 10 Available Themes & Categories:

| Theme Key | Theme Name | Category | Accent Color | Mood & Palette |
| :--- | :--- | :--- | :--- | :--- |
| **`catppuccin`** | **Catppuccin Mocha** (Default) | 🌙 Dark | `#cba6f7` (Mauve) | Soothing warm pastel dark |
| **`tokyo-night`** | **Tokyo Night** | 🌙 Dark | `#7aa2f7` (Neon Blue) | Clean cyber night neon |
| **`nord`** | **Nordic Frost** | 🌙 Dark | `#88c0d0` (Frost Blue) | Arctic cool aesthetic |
| **`oled`** | **OLED Pitch Black** | 🌙 Dark | `#38bdf8` (Sky Blue) | Infinite deep pure black |
| **`dracula`** | **Dracula** | 🌙 Dark | `#bd93f9` (Purple) | Classic vampire neon pastel |
| **`gruvbox`** | **Gruvbox Dark** | 🌙 Dark | `#fe8019` (Orange) | Warm retro groovy palette |
| **`rose-pine`** | **Rosé Pine** | 🌙 Dark | `#ebbcba` (Rose) | Natural soft vintage pine |
| **`everforest`** | **Everforest Dark** | 🌙 Dark | `#a7c080` (Green) | Calming earthy forest green |
| **`cyberpunk`** | **Cyberpunk Neon** | 🌙 Dark | `#00f0ff` (Cyan) | High-contrast electric neon |
| **`light`** | **Paper Light** | ☀️ Light | `#0284c7` (Ocean Blue) | Crisp daylight paper aesthetic |

### 🌗 Dark & Light Mode Synchronization:
- **Dark Mode Themes** (`catppuccin`, `tokyo-night`, `nord`, `oled`, `dracula`, `gruvbox`, `rose-pine`, `everforest`, `cyberpunk`):
  - `org.gnome.desktop.interface color-scheme` set to `'prefer-dark'`
  - GTK theme: `catppuccin-mocha-mauve-standard+default`
  - Icon theme: `Papirus-Dark`
  - `gtk-application-prefer-dark-theme = 1` across GTK-2.0, GTK-3.0, and GTK-4.0
  - Browser (Brave / Chromium): Native Classic engine renders rich dark mode with optimal contrast.
- **Light Mode Theme** (`light` / Paper Light):
  - `org.gnome.desktop.interface color-scheme` set to `'prefer-light'`
  - GTK theme: `Adwaita`
  - Icon theme: `Papirus-Light`
  - `gtk-application-prefer-dark-theme = 0` across GTK-2.0, GTK-3.0, and GTK-4.0
  - Browser (Brave / Chromium): Native Classic engine renders crisp light mode with high-contrast text (no white-on-white CSS glitches).

### 🚀 How to Switch Themes:
1. **Shortcut**: Press **`Super + Shift + t`** to launch the interactive Rofi theme selector.
2. **Control Center**: Press **`Super + c`** and click the theme palette button (``) in the header.
3. **CLI**: Run `theme-switcher <theme-key>` (e.g., `theme-switcher tokyo-night`, `theme-switcher light`).

---

## 🖼️ Wallpaper Management

### 1. How to Change Wallpaper
There are two fast ways to switch wallpapers:
- **Shortcut**: Press **`Super + Shift + w`** to open the Rofi Wallpaper Selector.
- **Control Center**: Press **`Super + c`** (or click the slider icon `` on Polybar) and click the **`Wallpaper`** tile.

A menu will appear displaying all available wallpapers with live image thumbnails. Select your wallpaper using the arrow keys or mouse and press `Enter`. It will instantly:
1. Apply to your current desktop via `feh`.
2. Automatically pre-render a clean **50% Gaussian blur** version for the lockscreen (`~/.cache/lockscreen_blur.png`).
3. Save the active choice persistently across reboots (`~/.cache/current_wallpaper`).
4. Update SDDM display manager background image (`/usr/share/sddm/themes/silent/backgrounds/wallpaper.jpg`).

### 2. How to Add New Wallpapers
The selector script dynamically reads files, so adding wallpapers requires zero configuration:
1. Copy or download any image file (`.jpg`, `.png`, `.jpeg`, or `.webp`) into:
   ```bash
   ~/Pictures/Wallpapers/
   ```
2. Press **`Super + Shift + w`** — your new image will immediately show up in the menu!

---

## 📦 Requirements & Dependencies

The installer will automatically handle all dependencies on **Arch Linux**:

- **Core Window Management**: `i3-wm`, `polybar`, `picom`, `kitty`, `rofi`, `feh`, `dunst`, `libnotify`
- **Shell & CLI**: `zsh`, `starship`, `fastfetch`, `eza`, `bat`, `fzf`, `zsh-autosuggestions`, `zsh-syntax-highlighting`
- **Audio & Media**: `pamixer`, `playerctl`, `brightnessctl`
- **Network**: `networkmanager`, `network-manager-applet`, `networkmanager-dmenu`
- **File Manager & Archiving**: `nemo`, `file-roller`, `nemo-fileroller`, `7zip`, `unrar`, `nemo-terminal`, `ffmpegthumbnailer`, `tumbler`, `webp-pixbuf-loader`, `poppler-glib`
- **X11 & Utilities**: `maim`, `slop`, `xclip`, `htop`, `imagemagick`, `bc`, `xorg-xrandr`, `xorg-xset`, `xorg-xrdb`, `xss-lock`, `polkit-gnome`
- **Fonts & Emojis**: `noto-fonts-emoji` (full-color emoji), `inter-font` (UI font), `noto-fonts`, `noto-fonts-cjk` (East Asian glyphs), `JetBrainsMono Nerd Font`, `lucide`
- **GTK & Python**: `python`, `python-gobject`, `gtk3`, `cairo`, `papirus-icon-theme`, `gcc`, `make`, `pkgconf`, `libx11`, `libxfixes`, `libxcursor`
- **Display Manager**: `sddm`, `qt6-svg`, `qt6-virtualkeyboard`, `qt6-multimedia-ffmpeg`, `qt6-imageformats`
- **AUR Packages**: `sddm-silent-theme`, `i3lock-color`, `betterlockscreen`, `nemo-preview`, `rofi-greenclip` *(optional fallback binary automatically fetched if AUR is unavailable)*

---

## 🚀 Installation

> [!IMPORTANT]
> **Do NOT run the script with `sudo`!** Run it as your normal user: `./install.sh`.  
> The script will automatically ask for your `sudo` password only when required (e.g. for `pacman` and system services).
> 
> **You do NOT need to install dependencies manually** (like Polybar, Picom, Pamixer, etc.). The script automatically detects, downloads, and installs everything for you!

### 1. Clone the repository
```bash
git clone https://github.com/w4nnnn/i3-dotfiles.git ~/dotfiles
cd ~/dotfiles
```

### 2. Run the automated installer
```bash
chmod +x install.sh
./install.sh
```

The script will automatically:
1. Synchronize package databases and install all official packages via `pacman`.
2. Bootstrap `yay` automatically (if no AUR helper exists) and install AUR packages (`sddm-silent-theme`, `i3lock-color`, `nemo-preview`, `betterlockscreen`, `rofi-greenclip`).
3. Download and register `JetBrainsMono Nerd Font` and `Lucide` icons into the font cache.
4. Download and setup the official `Catppuccin Mocha` GTK and Cursor themes.
5. Compile C helper utilities (`xcorners`, `set-root-cursor`, & `gtk_popup_rgba`).
6. Deploy all `.config/`, `.local/bin/`, `.local/lib/`, wallpapers, and home files (`.xinitrc`, `.xprofile`, `.zshrc`, etc.).
7. Setup and enable `SilentSDDM` with matching blurred wallpaper and auto-sync.
8. Restart `i3wm` with the new configuration.

---

## 📂 Repository Structure

```
dotfiles/
├── .config/
│   ├── betterlockscreen/       # Betterlockscreen configuration
│   ├── control-center/         # Modular GTK3 Quick Settings Control Center
│   │   ├── services/           # Backend services (audio, bluetooth, brightness, media, network, power, system)
│   │   ├── widgets/            # UI components (footer, header, player, power, sliders, telemetry, toggles)
│   │   ├── config.py           # Layout definitions & styling parameters
│   │   ├── styles.py           # CSS theme rules & widget appearance
│   │   └── window.py           # Main floating window & seat grabbing logic
│   ├── dunst/                  # Notification daemon styling (dunstrc, OSD volume/brightness)
│   ├── fastfetch/              # Fastfetch system info banner (config.jsonc)
│   ├── fontconfig/             # Font fallback & Noto Color Emoji configuration (fonts.conf)
│   ├── greenclip.toml          # Greenclip clipboard manager settings
│   ├── gtk-3.0/                # GTK 3.0 theme & font settings (settings.ini)
│   ├── gtk-4.0/                # GTK 4.0 theme & font settings (settings.ini)
│   ├── i3/                     # i3wm config, keybindings, lock-colors & dynamic theme.conf
│   ├── kitty/                  # Kitty terminal configuration (kitty.conf & theme.conf)
│   ├── networkmanager-dmenu/   # NetworkManager dmenu configuration (config.ini)
│   ├── picom/                  # Picom compositor (blur, animations, shadows)
│   ├── polybar/                # Polybar config, multi-monitor launch & colors.ini
│   ├── rofi/                   # Rofi configs (clipboard, colors, config, keybinds, network, powermenu, wallpaper)
│   └── starship.toml           # Starship prompt configuration
├── .local/
│   ├── bin/                    # Custom utility scripts & launchers
│   │   ├── audio-selector      # GTK3 Audio Output Device Selector
│   │   ├── battery-alert       # Background daemon for battery low & charging alerts
│   │   ├── battery-info        # Detailed battery statistics & health notifier
│   │   ├── bluetooth-menu      # Modern GTK3 Bluetooth Manager floating modal
│   │   ├── brightness-control  # Brightness OSD notifier with Dunst
│   │   ├── calendar-popup      # Interactive floating calendar widget
│   │   ├── clipboard           # Greenclip rofi clipboard manager helper
│   │   ├── control-center      # GTK3 Quick Settings control center
│   │   ├── generate-lock-bg    # Lockscreen canvas renderer
│   │   ├── i3-autotile         # Hyprland-style auto-tiling & dynamic dialog resizer
│   │   ├── keybinds-viewer     # Interactive keybindings cheatsheet viewer
│   │   ├── lockscreen          # Lockscreen launcher (i3lock-color)
│   │   ├── network-info        # Network details notifier
│   │   ├── network-menu        # Modern GTK3 Network Manager with action toolbar
│   │   ├── network-status-bar  # Dynamic Polybar network speed helper
│   │   ├── portal-login        # Captive portal detection & browser login assistant
│   │   ├── powermenu           # Horizontal rofi power menu with auto-caffeine teardown
│   │   ├── screen-project      # GTK3 Screen Project & Cast Manager (Win+P style)
│   │   ├── screenshot          # maim + slop screenshot helper
│   │   ├── theme-switcher      # Global 10-theme desktop synchronizer
│   │   ├── toggle-caffeine     # Anti-sleep & safe idle:sleep keep-awake toggle
│   │   ├── toggle-dnd          # Quick Do Not Disturb (DND) toggle
│   │   ├── toggle-htop         # Smart toggle for floating task manager
│   │   ├── toggle-scratchpad   # Floating dropdown terminal scratchpad
│   │   ├── volume-control      # Volume OSD notifier with Dunst
│   │   ├── wallpaper-selector  # Dynamic wallpaper selector with thumbnails
│   │   ├── web-screen-share    # Lightweight wireless presentation streaming server
│   │   ├── win11-start         # Modern Windows 11-style GTK3 Start Menu
│   │   └── src/                # C source code for compiled helpers
│   │       ├── gtk_popup_rgba.c # GTK3 popup menu RGBA visual module
│   │       ├── set-root-cursor.c # Root window X11 cursor initializer
│   │       └── xcorners.c      # Cairo concave rounded screen corner overlays
│   └── lib/dotfiles/           # Shared Python libraries (< 500 LOC modular modules)
│       ├── apps.py             # App scanner & workspace-isolated launch helper
│       ├── audio.py            # Audio device switching & sound cues
│       ├── bluetooth.py        # D-Bus Bluetooth device discovery & pairing manager
│       ├── displays.py         # Multi-monitor modes & file chooser geometry sync
│       ├── gtk_utils.py        # Seat grabbing, click-outside & window centering
│       ├── network.py          # NetworkManager GLib backend wrapper
│       ├── network_dialog.py   # In-place Wi-Fi password modal
│       ├── theme_sync.py       # Atomic theme synchronizer across all apps & GSettings
│       ├── themes.py           # Global 10-theme palette & Dark/Light categorization
│       └── styles/             # Modular CSS stylesheets for floating menus
│           ├── audio.py        # Audio selector styles
│           ├── bluetooth.py    # Bluetooth menu styles
│           ├── network.py      # Network manager styles
│           ├── screen_project.py # Screen project styles
│           └── win11_start.py  # Start menu styles
├── fonts/                      # Custom font files (lucide.ttf)
├── sddm/                       # SDDM login manager configuration
│   ├── sddm.conf               # Environment & theme selection config
│   └── catppuccin-mocha.conf   # SilentSDDM Catppuccin Mocha preset
├── Pictures/Wallpapers/        # Curated Catppuccin Mocha wallpapers
├── home/                       # Home directory dotfiles (.gtkrc-2.0, .xinitrc, .xprofile, .Xresources, .zshrc)
├── install.sh                  # Automated Arch Linux installer script
├── .gitignore
└── README.md
```
