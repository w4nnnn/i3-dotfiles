#!/usr/bin/env bash
# ==============================================================================
# Catppuccin Mocha i3wm Rice - Automated Installer for Arch Linux
# ==============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prevent running as root/sudo (common mistake that installs files into /root)
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}${BOLD}[!] ERROR: Jangan jalankan script ini dengan 'sudo ./install.sh'!${NC}"
    echo -e "${YELLOW}Jalankan sebagai user biasa:${NC} ${BOLD}./install.sh${NC}"
    echo -e "Script akan otomatis meminta password sudo saat dibutuhkan untuk instalasi paket sistem."
    exit 1
fi

# Setup logging (terminal output + log file)
LOG_FILE="$HOME/install_dotfiles.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "=== Dotfiles Installation Started: $(date) ==="

echo -e "${PURPLE}${BOLD}"
cat << "EOF"
   ____      _                                _        _ _____ 
  / ___|__ _| |_ _ __  _ __  _   _  ___ ___(_)_ __   (_)___ / 
 | |   / _` | __| '_ \| '_ \| | | |/ __/ __| | '_ \  | | |_ \ 
 | |__| (_| | |_| |_) | |_) | |_| | (_| (__| | | | | | |___) |
  \____\__,_|\__| .__/| .__/ \__,_|\___\___|_|_| |_| |_|____/ 
                |_|   |_|                                     
            Catppuccin Mocha Rice Automated Installer
EOF
echo -e "${NC}"

# Check Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo -e "${YELLOW}[!] Warning: This script is crafted for Arch Linux.${NC}"
fi

# Detect AUR Helper
AUR_HELPER=""
if command -v yay >/dev/null 2>&1; then
    AUR_HELPER="yay"
elif command -v paru >/dev/null 2>&1; then
    AUR_HELPER="paru"
fi

# ------------------------------------------------------------------------------
# 1. Install Pacman Packages
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[1/7] Syncing databases & installing required packages...${NC}"

# Ensure database is updated to prevent 404 package errors
sudo pacman -Sy

OFFICIAL_PKGS=(
    i3-wm
    polybar
    picom
    kitty
    rofi
    feh
    dunst
    libnotify
    xorg-xrandr
    xorg-xset
    xorg-xrdb
    xss-lock
    polkit-gnome
    brightnessctl
    playerctl
    pamixer
    maim
    slop
    xclip
    htop
    imagemagick
    bc
    python
    python-gobject
    gtk3
    cairo
    gcc
    make
    pkgconf
    libx11
    libxfixes
    libxcursor
    network-manager-applet
    networkmanager-dmenu
    papirus-icon-theme
    nemo
    file-roller
    nemo-fileroller
    7zip
    unrar
    nemo-terminal
    ffmpegthumbnailer
    tumbler
    webp-pixbuf-loader
    poppler-glib
    zsh
    zsh-autosuggestions
    zsh-syntax-highlighting
    starship
    fastfetch
    eza
    bat
    fzf
    noto-fonts-emoji
    noto-fonts
    noto-fonts-cjk
    inter-font
    sddm
    qt6-svg
    qt6-virtualkeyboard
    qt6-multimedia-ffmpeg
    qt6-imageformats
)

TO_INSTALL=()
for pkg in "${OFFICIAL_PKGS[@]}"; do
    if ! pacman -Q "$pkg" >/dev/null 2>&1; then
        TO_INSTALL+=("$pkg")
    fi
done

if [ ${#TO_INSTALL[@]} -gt 0 ]; then
    echo -e "${BLUE}Packages to install: ${TO_INSTALL[*]}${NC}"
    sudo pacman -S --needed --noconfirm "${TO_INSTALL[@]}"
else
    echo -e "${GREEN}All required official packages are already installed.${NC}"
fi

# ------------------------------------------------------------------------------
# 2. Install AUR Packages (betterlockscreen, i3lock-color, nemo-preview, sddm-silent-theme)
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[2/7] Checking AUR packages (betterlockscreen, i3lock-color, nemo-preview, sddm-silent-theme)...${NC}"

# If no AUR helper found, automatically bootstrap yay-bin
if [ -z "$AUR_HELPER" ]; then
    echo -e "${BLUE}No AUR helper found. Bootstrapping 'yay' automatically...${NC}"
    sudo pacman -S --needed --noconfirm git base-devel
    BUILD_DIR="/tmp/yay-bin"
    rm -rf "$BUILD_DIR"
    if git clone https://aur.archlinux.org/yay-bin.git "$BUILD_DIR"; then
        (cd "$BUILD_DIR" && makepkg -si --noconfirm) || true
        rm -rf "$BUILD_DIR"
    fi
    if command -v yay >/dev/null 2>&1; then
        AUR_HELPER="yay"
        echo -e "${GREEN}'yay' installed successfully!${NC}"
    fi
fi

if [ -n "$AUR_HELPER" ]; then
    AUR_PKGS=(betterlockscreen i3lock-color nemo-preview sddm-silent-theme)
    AUR_TO_INSTALL=()
    for pkg in "${AUR_PKGS[@]}"; do
        if ! pacman -Q "$pkg" >/dev/null 2>&1; then
            AUR_TO_INSTALL+=("$pkg")
        fi
    done
    if [ ${#AUR_TO_INSTALL[@]} -gt 0 ]; then
        echo -e "${BLUE}Installing via $AUR_HELPER: ${AUR_TO_INSTALL[*]}${NC}"
        $AUR_HELPER -S --needed --noconfirm "${AUR_TO_INSTALL[@]}" || echo -e "${YELLOW}[!] Some AUR packages could not be installed automatically. Continuing...${NC}"
    else
        echo -e "${GREEN}AUR packages are already installed.${NC}"
    fi
else
    echo -e "${YELLOW}[!] Could not setup AUR helper. Please install AUR packages manually if desired.${NC}"
fi

# ------------------------------------------------------------------------------
# 3. Fonts & Themes Setup
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[3/7] Setting up JetBrainsMono Nerd Font & Catppuccin Theme...${NC}"

# Font
mkdir -p "$HOME/.local/share/fonts"
if [ -f "$DIR/fonts/lucide.ttf" ]; then
    cp "$DIR/fonts/lucide.ttf" "$HOME/.local/share/fonts/"
fi

if ! fc-list : family | grep -iq "JetBrainsMono Nerd Font"; then
    echo -e "${BLUE}Downloading JetBrainsMono Nerd Font...${NC}"
    curl -sL "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/JetBrainsMono.tar.xz" -o /tmp/JetBrainsMono.tar.xz
    tar -xf /tmp/JetBrainsMono.tar.xz -C "$HOME/.local/share/fonts/"
    rm -f /tmp/JetBrainsMono.tar.xz
    fc-cache -f "$HOME/.local/share/fonts"
    echo -e "${GREEN}Fonts installed!${NC}"
else
    fc-cache -f "$HOME/.local/share/fonts" >/dev/null 2>&1 || true
    echo -e "${GREEN}Fonts are up to date.${NC}"
fi

# GTK Theme (Catppuccin Mocha Mauve)
mkdir -p "$HOME/.local/share/themes" "$HOME/.local/share/icons" "$HOME/.icons"
if [ ! -d "$HOME/.local/share/themes/catppuccin-mocha-mauve-standard+default" ]; then
    echo -e "${BLUE}Downloading Catppuccin Mocha GTK Theme...${NC}"
    python3 - << 'PYEOF'
import urllib.request, zipfile, io, os
themes_dir = os.path.expanduser("~/.local/share/themes")
url = "https://github.com/catppuccin/gtk/releases/download/v1.0.3/catppuccin-mocha-mauve-standard%2Bdefault.zip"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
        z.extractall(themes_dir)
PYEOF
fi

# Cursors (Catppuccin Mocha Mauve Cursors)
if [ ! -d "$HOME/.local/share/icons/catppuccin-mocha-mauve-cursors" ]; then
    echo -e "${BLUE}Downloading Catppuccin Mocha Cursors...${NC}"
    python3 - << 'PYEOF'
import urllib.request, zipfile, io, os
icons_dir = os.path.expanduser("~/.local/share/icons")
url = "https://github.com/catppuccin/cursors/releases/download/v2.0.0/catppuccin-mocha-mauve-cursors.zip"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
        z.extractall(icons_dir)

# Convert fake text files into real POSIX symlinks
cur_dir = os.path.join(icons_dir, "catppuccin-mocha-mauve-cursors", "cursors")
if os.path.exists(cur_dir):
    for f in os.listdir(cur_dir):
        p = os.path.join(cur_dir, f)
        if os.path.isfile(p) and not os.path.islink(p):
            try:
                with open(p, "rb") as fp:
                    c = fp.read()
                if len(c) < 80 and c.isascii() and b"\x00" not in c:
                    target = c.decode("utf-8").strip()
                    os.remove(p)
                    os.symlink(target, p)
            except Exception:
                pass
PYEOF
fi

# Symlinks for backwards compatibility
ln -sf "$HOME/.local/share/icons/catppuccin-mocha-mauve-cursors" "$HOME/.icons/catppuccin-mocha-mauve-cursors"
mkdir -p "$HOME/.icons/default" "$HOME/.local/share/icons/default"
cat << 'EOF' > "$HOME/.icons/default/index.theme"
[Icon Theme]
Name=Default
Comment=Default Cursor Theme
Inherits=catppuccin-mocha-mauve-cursors,Adwaita
EOF
cp "$HOME/.icons/default/index.theme" "$HOME/.local/share/icons/default/index.theme"
ln -sf "$HOME/.local/share/icons/catppuccin-mocha-mauve-cursors/cursors" "$HOME/.icons/default/cursors" 2>/dev/null || true
ln -sf "$HOME/.local/share/icons/catppuccin-mocha-mauve-cursors/cursors" "$HOME/.local/share/icons/default/cursors" 2>/dev/null || true

# ------------------------------------------------------------------------------
# 4. Compile C Helper Binaries
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[4/7] Compiling helper utilities (xcorners & set-root-cursor)...${NC}"
mkdir -p "$HOME/.local/bin"

if [ -f "$DIR/.local/bin/src/set-root-cursor.c" ]; then
    gcc -O2 "$DIR/.local/bin/src/set-root-cursor.c" -lX11 -lXcursor -o "$HOME/.local/bin/set-root-cursor"
    echo -e "${GREEN}Compiled set-root-cursor!${NC}"
fi

if [ -f "$DIR/.local/bin/src/xcorners.c" ]; then
    gcc -O2 "$DIR/.local/bin/src/xcorners.c" $(pkg-config --cflags --libs cairo x11 xfixes) -lm -o "$HOME/.local/bin/xcorners"
    echo -e "${GREEN}Compiled xcorners!${NC}"
fi

# ------------------------------------------------------------------------------
# 5. Deploy Dotfiles & Wallpapers
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[5/7] Deploying configuration files...${NC}"

# Clean up deprecated ~/.i3 directory to prevent i3 from loading the default config
if [ -d "$HOME/.i3" ]; then
    echo -e "${YELLOW}Backing up deprecated ~/.i3 to ~/.i3.bak...${NC}"
    mv "$HOME/.i3" "$HOME/.i3.bak" 2>/dev/null || true
fi
if [ -f "$HOME/.i3/config" ]; then
    mv "$HOME/.i3/config" "$HOME/.i3/config.bak" 2>/dev/null || true
fi

# .config files & directories
mkdir -p "$HOME/.config"
for cfg in "$DIR/.config/"*; do
    target_name=$(basename "$cfg")
    if [ -d "$cfg" ]; then
        mkdir -p "$HOME/.config/$target_name"
        cp -rf "$cfg/"* "$HOME/.config/$target_name/"
    else
        cp -f "$cfg" "$HOME/.config/$target_name"
    fi
    echo -e "${GREEN}  ✓ ~/.config/$target_name${NC}"
done

# Ensure polybar launch script is executable
chmod +x "$HOME/.config/polybar/launch.sh" 2>/dev/null || true

# .local/bin scripts
mkdir -p "$HOME/.local/bin"
for bin in "$DIR/.local/bin/"*; do
    if [ -f "$bin" ]; then
        target_name=$(basename "$bin")
        cp -f "$bin" "$HOME/.local/bin/$target_name"
        chmod +x "$HOME/.local/bin/$target_name"
        echo -e "${GREEN}  ✓ ~/.local/bin/$target_name${NC}"
    fi
done
chmod +x "$HOME/.local/bin/"* 2>/dev/null || true

# Wallpapers
mkdir -p "$HOME/Pictures/Wallpapers"
if [ -d "$DIR/Pictures/Wallpapers" ]; then
    cp -rf "$DIR/Pictures/Wallpapers/"* "$HOME/Pictures/Wallpapers/"
    echo -e "${GREEN}  ✓ ~/Pictures/Wallpapers (Wallpapers collection)${NC}"
fi

# Home configuration files (.xinitrc, .xprofile, .Xresources, .gtkrc-2.0, .zshrc)
if [ -d "$DIR/home" ]; then
    cp -rf "$DIR/home/".* "$HOME/" 2>/dev/null || true
    chmod +x "$HOME/.xinitrc" "$HOME/.xprofile" 2>/dev/null || true
    echo -e "${GREEN}  ✓ Home config files (.xinitrc, .xprofile, .Xresources, .gtkrc-2.0, .zshrc)${NC}"
fi

# Ensure ~/.local/bin is in PATH in ~/.bashrc
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Set Zsh as default user shell if installed
if command -v zsh >/dev/null 2>&1 && [ "$SHELL" != "$(which zsh)" ]; then
    echo -e "${BLUE}Setting Zsh as default user shell...${NC}"
    sudo usermod -s "$(which zsh)" "$USER" 2>/dev/null || chsh -s "$(which zsh)" 2>/dev/null || true
fi

# ------------------------------------------------------------------------------
# 6. Apply System Themes & GSettings
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[6/7] Applying GTK themes, SDDM & preferences...${NC}"

xrdb -merge "$HOME/.Xresources" 2>/dev/null || true
"$HOME/.local/bin/set-root-cursor" 2>/dev/null || true

if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark' 2>/dev/null || true
    gsettings set org.gnome.desktop.interface gtk-theme 'catppuccin-mocha-mauve-standard+default' 2>/dev/null || true
    gsettings set org.gnome.desktop.interface cursor-theme 'catppuccin-mocha-mauve-cursors' 2>/dev/null || true
    gsettings set org.gnome.desktop.interface font-name 'JetBrainsMono Nerd Font 10' 2>/dev/null || true
    gsettings set org.gnome.desktop.wm.preferences theme 'catppuccin-mocha-mauve-standard+default' 2>/dev/null || true

    # Cinnamon / Nemo settings
    gsettings set org.cinnamon.desktop.interface cursor-theme 'catppuccin-mocha-mauve-cursors' 2>/dev/null || true
    gsettings set org.cinnamon.desktop.interface gtk-theme 'catppuccin-mocha-mauve-standard+default' 2>/dev/null || true
    gsettings set org.cinnamon.desktop.interface icon-theme 'Papirus-Dark' 2>/dev/null || true
    gsettings set org.cinnamon.desktop.interface font-name 'JetBrainsMono Nerd Font 10' 2>/dev/null || true
    gsettings set org.cinnamon.desktop.default-applications.terminal exec 'kitty' 2>/dev/null || true
    gsettings set org.cinnamon.desktop.default-applications.terminal exec-arg '-e' 2>/dev/null || true
    gsettings set org.nemo.extensions.nemo-terminal terminal-shell '/usr/bin/zsh' 2>/dev/null || true
fi

# Add user to libvirt and kvm groups if installed
if getent group libvirt >/dev/null 2>&1; then
    sudo usermod -aG libvirt,kvm "$USER" 2>/dev/null || true
fi

# Set initial wallpaper
INITIAL_WALL="$HOME/Pictures/Wallpapers/catppuccin-aesthetic.jpg"
if [ -f "$INITIAL_WALL" ]; then
    mkdir -p "$HOME/.cache"
    ln -sf "$INITIAL_WALL" "$HOME/.cache/current_wallpaper"
    feh --bg-fill "$INITIAL_WALL" 2>/dev/null || true
    magick "$INITIAL_WALL" -resize 1920x1080^ -gravity center -extent 1920x1080 -blur 0x12 "$HOME/.cache/lockscreen_blur.png" 2>/dev/null || true
fi

# Ensure SilentSDDM theme is installed
if [ ! -d /usr/share/sddm/themes/silent ]; then
    echo -e "${BLUE}Downloading SilentSDDM theme to /usr/share/sddm/themes/silent...${NC}"
    sudo git clone -b main --depth=1 https://github.com/uiriansan/SilentSDDM /usr/share/sddm/themes/silent 2>/dev/null || true
fi

# Configure SilentSDDM Theme (Catppuccin Mocha)
if [ -d /usr/share/sddm/themes/silent ]; then
    echo -e "${GREEN}Configuring SilentSDDM (Catppuccin Mocha)...${NC}"
    if [ -f "$DIR/sddm/sddm.conf" ]; then
        sudo cp "$DIR/sddm/sddm.conf" /etc/sddm.conf 2>/dev/null || true
    fi
    if [ -f "$DIR/sddm/catppuccin-mocha.conf" ]; then
        sudo cp "$DIR/sddm/catppuccin-mocha.conf" /usr/share/sddm/themes/silent/configs/catppuccin-mocha.conf 2>/dev/null || true
    fi
    sudo sed -i 's|^ConfigFile=.*|ConfigFile=configs/catppuccin-mocha.conf|' /usr/share/sddm/themes/silent/metadata.desktop 2>/dev/null || true

    # Prepare wallpaper and permissions for auto-sync
    if [ -f "$INITIAL_WALL" ]; then
        sudo cp "$INITIAL_WALL" /usr/share/sddm/themes/silent/backgrounds/wallpaper.jpg 2>/dev/null || true
        sudo chown "$USER:$USER" /usr/share/sddm/themes/silent/backgrounds/wallpaper.jpg 2>/dev/null || true
    fi
fi

# Enable Graphical boot target & SDDM display manager
echo -e "${BLUE}Setting up graphical display manager (SDDM)...${NC}"
sudo systemctl set-default graphical.target 2>/dev/null || true
sudo systemctl disable lightdm 2>/dev/null || true
sudo systemctl enable sddm 2>/dev/null || true

# ------------------------------------------------------------------------------
# 7. Finishing up
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}${BOLD}[7/7] Reloading window manager...${NC}"

if pgrep -x i3 >/dev/null 2>&1; then
    i3-msg restart >/dev/null 2>&1 || true
    echo -e "${GREEN}i3wm restarted successfully!${NC}"
fi

echo -e "\n${PURPLE}${BOLD}======================================================${NC}"
echo -e "${GREEN}${BOLD}       Installation Completed Successfully!           ${NC}"
echo -e "${PURPLE}${BOLD}======================================================${NC}"
echo -e "${CYAN}📁 Detailed log saved to:${NC} ${BOLD}$LOG_FILE${NC}\n"
echo -e "${CYAN}Key Shortcuts:${NC}"
echo -e "  • ${BOLD}Super + t${NC}       : Open Kitty Terminal"
echo -e "  • ${BOLD}Super + b${NC}       : Open Brave Browser"
echo -e "  • ${BOLD}Super + a / d${NC}   : Open Rofi App Launcher"
echo -e "  • ${BOLD}Super + c${NC}       : Open Control Center (Quick Settings)"
echo -e "  • ${BOLD}Super + Shift + w${NC} : Open Wallpaper Selector"
echo -e "  • ${BOLD}Super + Escape${NC}  : Lock Screen"
echo -e "  • ${BOLD}Super + q${NC}       : Close Window"
echo -e "  • ${BOLD}Print${NC}           : Screenshot Area"
echo -e "  • ${BOLD}Shift + Print${NC}   : Screenshot Fullscreen"
echo -e "  • ${BOLD}Super + Shift + r${NC} : Restart i3wm"
echo ""
