# ☕ Catppuccin Mocha i3wm Dotfiles

A modern, cohesive, and aesthetic **i3wm** rice built on **Arch Linux** themed in **Catppuccin Mocha (Mauve accent)**. Designed with fluid animations, interactive system menus, and Hyprland-inspired dynamic tiling.

---

## ✨ Features & Highlights

- **Window Manager**: `i3wm` with static minimal gaps (`6px inner`, `2px outer`), rounded corners (`12px`), and smart auto-tiling (`i3-autotile` Fibonacci/spiral split like Hyprland).
- **Inverted Screen Corners**: Custom Cairo/XFixes utility (`xcorners`) providing concave rounded screen corners underneath the docked top bar.
- **Top Status Bar**: `Polybar` configured with interactive modules:
  - **Date / Time**: Click to open a floating Catppuccin interactive calendar widget.
  - **Network (Ethernet)**: Click to open `nmtui` (left), connection editor (right), or connection status IP (middle).
  - **Audio & Memory & CPU**: Scroll to change volume, click to open `htop` in a floating terminal.
  - **Control Center & System Tray**: Native tray support for background apps (e.g. 9router, Discord, Steam).
- **Control Center (Quick Settings)**: Floating GTK3 card (`Super + c`) inspired by Android / Windows 11:
  - Interactive volume & brightness sliders with live feedback.
  - Quick toggle tiles: Network, Do Not Disturb (DND), Wallpaper, and Screenshot.
  - Mini media player with album/title controls (`playerctl`).
- **Wallpaper & Lockscreen Sync**: Dynamic wallpaper selector (`Super + Shift + w`) via Rofi with live thumbnails that syncs both the active desktop and the lockscreen automatically.
- **Lockscreen & Auto-Lock**: `i3lock-color` featuring 50% Gaussian blurred wallpaper, high-contrast clock, responsive emerald/peach/blue feedback indicator ring, and automatic locking after **5 minutes** of inactivity (AFK) via `xss-lock`.
- **Shell & Modern Terminal Stack (HyDE Inspired)**:
  - `ZSH` with `zsh-autosuggestions`, `zsh-syntax-highlighting`, and `fzf` history search.
  - `Starship` prompt customized with Catppuccin pastel colors and Arch glyphs (`󰣇`).
  - `Fastfetch` system information banner on terminal startup.
  - Modern CLI tools: `eza` (modern ls with icons), `bat` (syntax highlighting cat).
- **Terminal Emulator**: `Kitty` running Zsh with `JetBrainsMono Nerd Font`, 0.92 opacity, and full Catppuccin Mocha palette.
- **Compositor**: `Picom` with dual-kawase blur, rounded corners (`12px`), drop shadows, and smooth **Zoom / Scale Pop** workspace transitions.
- **App Launcher & Power Menu**: `Rofi` customized with frosted floating cards.
- **Display Manager**: `SDDM` running the [SilentSDDM](https://github.com/uiriansan/SilentSDDM) theme (Catppuccin Mocha preset, matching blurred wallpaper, and persistent auto-sync with the wallpaper selector).

---

## ⌨️ Keybindings Cheat Sheet

| Keybinding | Action |
| :--- | :--- |
| **`Super + t`** / **`Super + Enter`** | Launch Kitty Terminal |
| **`Super + b`** | Launch Brave Browser |
| **`Super + e`** | Launch Nemo File Manager |
| **`Super + a`** / **`Super + d`** | Open Rofi Application Launcher |
| **`Super + v`** | Open Clipboard History (Greenclip + Rofi) |
| **`Super + Shift + v`** | Clear Clipboard History |
| **`Super + c`** | Toggle Control Center (Quick Settings) |
| **`Super + Shift + w`** | Open Wallpaper Selector |
| **`Super + Escape`** | Lock Screen |
| **`Super + q`** | Close focused window |
| **`Super + f`** | Toggle Fullscreen |
| **`Super + Shift + Space`** | Toggle Floating window mode |
| **`Super + Tab`** | Switch between open windows (Rofi) |
| **`Super + Shift + e`** | Open Power Menu (Lock, Logout, Reboot, Shutdown) |
| **`Print`** | Screenshot selected area (saves to `~/Pictures/Screenshots` & clipboard) |
| **`Shift + Print`** | Screenshot entire screen |
| **`Ctrl + Print`** | Screenshot focused window |
| **`Alt + Print`** | Screenshot with 3-second delay |
| **`Super + Shift + r`** | In-place Restart i3wm |

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

- **Core**: `i3-wm`, `polybar`, `picom`, `kitty`, `rofi`, `feh`, `dunst`, `libnotify`
- **Shell & CLI**: `zsh`, `starship`, `fastfetch`, `eza`, `bat`, `fzf`, `zsh-autosuggestions`, `zsh-syntax-highlighting`
- **Audio & Media**: `pamixer`, `playerctl`, `brightnessctl`
- **Network**: `networkmanager-dmenu`, `network-manager-applet`
- **File Manager & Media Engine**: `nemo`, `file-roller`, `nemo-fileroller`, `p7zip`, `unrar`, `nemo-terminal`, `ffmpegthumbnailer`, `tumbler`, `webp-pixbuf-loader`, `poppler-glib`
- **Utilities**: `maim`, `slop`, `xclip`, `htop`, `imagemagick`, `bc`, `xorg-xrandr`, `xorg-xset`, `xorg-xrdb`
- **Fonts & Emojis**: `noto-fonts-emoji` (full-color emoji), `inter-font` (UI font), `noto-fonts`, `noto-fonts-cjk` (East Asian glyphs), `JetBrainsMono Nerd Font`, `lucide`
- **GTK & Python**: `python`, `python-gobject`, `gtk3`, `cairo`, `papirus-icon-theme`
- **Display Manager**: `sddm`, `qt6-svg`, `qt6-virtualkeyboard`, `qt6-multimedia-ffmpeg`, `qt6-imageformats`
- **AUR Packages**: `sddm-silent-theme`, `i3lock-color`, `betterlockscreen`, `nemo-preview`, `rofi-greenclip` *(optional)*

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
2. Bootstrap `yay` automatically (if no AUR helper exists) and install AUR packages (`sddm-silent-theme`, `i3lock-color`, `nemo-preview`, `betterlockscreen`).
3. Download and register `JetBrainsMono Nerd Font` and `Lucide` icons into the font cache.
4. Download and setup the official `Catppuccin Mocha` GTK and Cursor themes.
5. Compile C helper utilities (`xcorners` and `set-root-cursor`).
6. Deploy all `.config/`, `.local/bin/`, wallpapers, and home files (`.xinitrc`, `.xprofile`, `.zshrc`, etc.).
7. Setup and enable `SilentSDDM` with matching blurred wallpaper and auto-sync.
8. Restart `i3wm` with the new configuration.

---

## 📂 Repository Structure

```
dotfiles/
├── .config/
│   ├── betterlockscreen/   # Betterlockscreen configuration
│   ├── dunst/              # Notification daemon styling
│   ├── fastfetch/          # Fastfetch system info banner
│   ├── fontconfig/         # Font fallback & Noto Color Emoji configuration
│   ├── gtk-3.0/            # GTK 3.0 theme & font settings
│   ├── gtk-4.0/            # GTK 4.0 theme & font settings
│   ├── i3/                 # i3wm config & rules
│   ├── kitty/              # Kitty terminal configuration
│   ├── picom/              # Picom compositor (blur, animations, shadows)
│   ├── polybar/            # Polybar config & launch script
│   ├── rofi/               # Rofi app launcher, powermenu & wallpaper rasi
│   └── starship.toml       # Starship prompt configuration
├── .local/bin/             # Custom utility scripts
│   ├── calendar-popup      # Interactive floating calendar widget
│   ├── control-center      # GTK Quick Settings control center
│   ├── generate-lock-bg    # Lockscreen canvas renderer
│   ├── i3-autotile         # Hyprland-style automatic spiral tiling daemon
│   ├── lockscreen          # Lockscreen launcher
│   ├── network-info        # Network details notifier
│   ├── powermenu           # Horizontal rofi power menu
│   ├── screenshot          # maim + slop screenshot helper
│   ├── toggle-htop         # Smart toggle for task manager
│   ├── wallpaper-selector  # Dynamic wallpaper selector with thumbnails
│   └── src/                # C source code for compiled helpers
│       ├── set-root-cursor.c
│       └── xcorners.c
├── fonts/                  # Custom font files (lucide.ttf)
├── sddm/                   # SDDM login manager configuration
│   ├── sddm.conf           # Environment & theme selection config
│   └── catppuccin-mocha.conf # SilentSDDM Catppuccin Mocha preset
├── Pictures/Wallpapers/    # Curated Catppuccin Mocha wallpapers
├── home/                   # Home directory dotfiles (.xinitrc, .zshrc, .xprofile, .Xresources, .gtkrc-2.0)
├── install.sh              # Automated Arch Linux installer script
├── .gitignore
└── README.md
```

---

## 🎨 Theme Details
- **Palette**: [Catppuccin Mocha](https://github.com/catppuccin/catppuccin)
- **Accent Color**: Mauve (`#cba6f7`)
- **Font**: JetBrainsMono Nerd Font
- **Icons**: Papirus-Dark
- **Cursors**: Catppuccin Mocha Mauve Cursors
