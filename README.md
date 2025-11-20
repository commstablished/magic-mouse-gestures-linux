# Magic Mouse Gestures for Linux

Add macOS-style two-finger swipe gestures to your Apple Magic Mouse 2 on Linux! Switch workspaces with intuitive left/right swipes.

![Magic Mouse 2](https://img.shields.io/badge/Device-Magic%20Mouse%202-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🖱️ **Two-finger swipe gestures** for workspace switching
- 🚀 **Automatic startup** via systemd service
- ⚡ **Lightweight** - minimal CPU usage
- 🎯 **Simple setup** - no kernel compilation needed (if you already have the driver)
- 🔧 **Customizable** - easily modify actions for swipes

## 📋 Prerequisites

### 1. Magic Mouse 2 Linux Driver

You **must** have the Magic Mouse 2 kernel driver installed first. This provides the multi-touch support.

**Install the driver:**
```bash
git clone https://github.com/rohitpid/Linux-Magic-Trackpad-2-Driver.git
cd Linux-Magic-Trackpad-2-Driver
```

Follow the installation instructions in that repository to compile and load the driver.

**Verify the driver is working:**
```bash
# Your Magic Mouse should be detected
libinput list-devices | grep -A 10 "Magic Mouse"
```

### 2. System Requirements

- **Linux Kernel**: 4.18+ (tested on 6.8.0+)
- **Python**: 3.6 or higher
- **Desktop Environment**: GNOME, KDE, XFCE, or any DE with workspace support
- **Display Server**: X11 (Wayland support may vary)

### 3. Software Dependencies

```bash
# Ubuntu/Debian/Pop!_OS
sudo apt-get install python3 python3-evdev xdotool

# Fedora
sudo dnf install python3 python3-evdev xdotool

# Arch Linux
sudo pacman -S python python-evdev xdotool
```

## 🚀 Quick Install

Run the automated installer:

```bash
curl -sSL https://raw.githubusercontent.com/commstablished/magic-mouse-gestures-linux/main/install.sh | bash
```

Or install manually (see below).

## 📦 Manual Installation

### 1. Clone this repository

```bash
git clone https://github.com/commstablished/magic-mouse-gestures-linux.git
cd magic-mouse-gestures-linux
```

### 2. Install dependencies

```bash
sudo apt-get install python3-evdev xdotool
```

### 3. Add your user to the input group

This allows reading mouse events without root:

```bash
sudo usermod -a -G input $USER
```

**Important**: Log out and log back in for group changes to take effect!

### 4. Install the script and service

```bash
# Copy the script to a system location
sudo cp magic_swipe.py /usr/local/bin/magic_swipe.py
sudo chmod 755 /usr/local/bin/magic_swipe.py

# Install the systemd service
sudo cp magic-swipe.service /etc/systemd/system/magic-swipe.service
```

### 5. Configure the service for your display

Edit the service file to match your display number:

```bash
# Find your display number
echo $DISPLAY

# Edit the service file (usually :0 or :1)
sudo nano /etc/systemd/system/magic-swipe.service
# Change Environment="DISPLAY=:1" to match your display
```

### 6. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable magic-swipe.service
sudo systemctl start magic-swipe.service
```

### 7. Verify it's running

```bash
sudo systemctl status magic-swipe.service
```

You should see "active (running)" in green.

## 🎮 Usage

Just swipe with two fingers on your Magic Mouse:
- **Swipe LEFT** → Previous workspace (up)
- **Swipe RIGHT** → Next workspace (down)

The gestures work automatically after installation!

## ⚙️ Configuration

### Change Keyboard Shortcuts

Edit `/usr/local/bin/magic_swipe.py` and modify these lines:

```python
# Default: Ctrl+Super+Up/Down for vertical workspaces (Pop!_OS/GNOME)
WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "ctrl+super+Up"]
WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "ctrl+super+Down"]

# Alternative: For horizontal workspaces
# WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "ctrl+alt+Left"]
# WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "ctrl+alt+Right"]
```

After changes, restart the service:
```bash
sudo systemctl restart magic-swipe.service
```

### Custom Actions

You can make swipes do anything! Examples:

```python
# Volume control
WORKSPACE_SWITCH_LEFT = ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"]
WORKSPACE_SWITCH_RIGHT = ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"]

# Browser navigation
WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "alt+Left"]  # Back
WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "alt+Right"]  # Forward

# Media controls
WORKSPACE_SWITCH_LEFT = ["playerctl", "previous"]
WORKSPACE_SWITCH_RIGHT = ["playerctl", "next"]
```

## 🐛 Troubleshooting

### Service won't start

Check the logs:
```bash
sudo journalctl -u magic-swipe.service -n 50
```

### "Permission denied" errors

Make sure you:
1. Added yourself to the `input` group
2. Logged out and back in
3. The script has proper permissions (755)

### "Can't open display" errors

Your `DISPLAY` environment variable in the service file doesn't match. Check:
```bash
echo $DISPLAY
```

Then update `/etc/systemd/system/magic-swipe.service` accordingly.

### Gestures not detected

Verify your Magic Mouse driver is working:
```bash
# Run the event monitor
sudo python3 /usr/local/bin/magic_swipe.py

# Try swiping - you should see output
```

If nothing appears, the Magic Mouse 2 driver may not be properly installed.

## 🔄 Uninstall

```bash
sudo systemctl stop magic-swipe.service
sudo systemctl disable magic-swipe.service
sudo rm /etc/systemd/system/magic-swipe.service
sudo rm /usr/local/bin/magic_swipe.py
sudo systemctl daemon-reload
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

### Ideas for improvements:
- [ ] Debouncing to reduce sensitivity
- [ ] Configuration file instead of editing Python
- [ ] Support for more gestures (3-finger, pinch, etc.)
- [ ] Wayland support
- [ ] GUI configuration tool

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- **[rohitpid](https://github.com/rohitpid/Linux-Magic-Trackpad-2-Driver)** for the Magic Mouse 2 kernel driver
- The Linux input subsystem developers
- Everyone who contributed ideas and testing

## 📚 How It Works

This tool works by:
1. The Magic Mouse 2 driver sends `REL_HWHEEL` (horizontal wheel) events when you swipe
2. Our Python script listens for these events using the `evdev` library
3. When a swipe is detected, it triggers keyboard shortcuts via `xdotool`
4. The systemd service keeps it running in the background

It's simple, but effective!

## 💬 Support

Having issues? Please [open an issue](https://github.com/commstablished/magic-mouse-gestures-linux/issues) with:
- Your Linux distribution and version
- Kernel version (`uname -r`)
- Output of `sudo journalctl -u magic-swipe.service -n 50`
- Desktop environment (GNOME, KDE, etc.)

---

**Made with ❤️ by the Linux community**

*If this helped you, give it a ⭐ on GitHub!*
