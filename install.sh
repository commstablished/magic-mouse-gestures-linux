#!/bin/bash
#
# Magic Mouse Gestures for Linux - Installation Script
# https://github.com/commstablished/magic-mouse-gestures-linux
#

set -e  # Exit on error

echo "======================================"
echo "Magic Mouse Gestures for Linux"
echo "Installation Script"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "⚠️  Please do not run this script as root (without sudo)"
   echo "   Run it as your normal user. It will ask for sudo when needed."
   exit 1
fi

# Check for required commands
echo "→ Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed!"
    echo "  Install it with: sudo apt-get install python3"
    exit 1
fi

if ! command -v xdotool &> /dev/null; then
    echo "✗ xdotool is not installed!"
    echo "  Install it with: sudo apt-get install xdotool"
    exit 1
fi

# Check for Magic Mouse
echo "→ Checking for Magic Mouse 2..."
if ! libinput list-devices 2>/dev/null | grep -q "Magic Mouse"; then
    echo "⚠️  Magic Mouse not detected!"
    echo "   Make sure:"
    echo "   1. Your Magic Mouse is paired and connected"
    echo "   2. The Magic Mouse 2 driver is installed"
    echo "      (https://github.com/rohitpid/Linux-Magic-Trackpad-2-Driver)"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install Python dependencies
echo "→ Installing Python dependencies..."
if ! python3 -c "import evdev" 2>/dev/null; then
    echo "  Installing python3-evdev..."
    sudo apt-get update -qq
    sudo apt-get install -y python3-evdev
fi

# Add user to input group
echo "→ Adding $USER to input group..."
sudo usermod -a -G input $USER

# Get current display
DISPLAY_NUM=$(echo $DISPLAY | grep -oP ':\K\d+' || echo "1")

# Copy script
echo "→ Installing magic_swipe.py..."
sudo cp magic_swipe.py /usr/local/bin/magic_swipe.py
sudo chmod 755 /usr/local/bin/magic_swipe.py

# Create and install systemd service
echo "→ Creating systemd service..."
cat > /tmp/magic-swipe.service << EOF
[Unit]
Description=Magic Mouse Workspace Switcher
After=graphical.target
Requires=graphical.target

[Service]
Type=simple
User=$USER
Group=input
ExecStart=/usr/bin/python3 /usr/local/bin/magic_swipe.py
Restart=on-failure
RestartSec=5
Environment="DISPLAY=:$DISPLAY_NUM"
Environment="XAUTHORITY=$HOME/.Xauthority"

[Install]
WantedBy=graphical.target
EOF

sudo mv /tmp/magic-swipe.service /etc/systemd/system/magic-swipe.service

# Enable and start service
echo "→ Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable magic-swipe.service
sudo systemctl start magic-swipe.service

# Check status
echo ""
echo "→ Checking service status..."
sleep 1

if sudo systemctl is-active --quiet magic-swipe.service; then
    echo "✓ Service is running!"
else
    echo "⚠️  Service failed to start. Checking logs..."
    sudo journalctl -u magic-swipe.service -n 20 --no-pager
    exit 1
fi

echo ""
echo "======================================"
echo "✓ Installation Complete!"
echo "======================================"
echo ""
echo "🎉 Magic Mouse gestures are now active!"
echo ""
echo "Usage:"
echo "  • Swipe LEFT  → Previous workspace"
echo "  • Swipe RIGHT → Next workspace"
echo ""
echo "⚠️  IMPORTANT: You must LOG OUT and LOG BACK IN for"
echo "   input group permissions to take effect!"
echo ""
echo "Configuration:"
echo "  • Edit /usr/local/bin/magic_swipe.py to customize actions"
echo "  • View logs: sudo journalctl -u magic-swipe.service -f"
echo "  • Check status: sudo systemctl status magic-swipe.service"
echo ""
echo "Enjoy your macOS-like gestures on Linux! 🖱️✨"
echo ""
