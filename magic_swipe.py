#!/usr/bin/env python3
"""
Magic Mouse Workspace Switcher for Linux
Detects two-finger horizontal swipes on Magic Mouse 2 and switches workspaces.

Author: commstablished
License: MIT
Repository: https://github.com/commstablished/magic-mouse-gestures-linux

Requires:
- Magic Mouse 2 Linux driver (https://github.com/rohitpid/Linux-Magic-Trackpad-2-Driver)
- python3-evdev
- xdotool
"""

import evdev
from evdev import InputDevice, ecodes
import subprocess
import sys
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Workspace switching commands
# Modify these to match your desktop environment's keyboard shortcuts

# Vertical workspaces (Pop!_OS, GNOME)
# Using Super+Up/Down (no Ctrl to avoid browser zoom interference)
WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "super+Up"]
WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "super+Down"]

# Alternative configurations (uncomment to use):

# Horizontal workspaces
# WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "ctrl+alt+Left"]
# WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "ctrl+alt+Right"]

# KDE Plasma
# WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "ctrl+F1"]
# WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "ctrl+F2"]

# XFCE
# WORKSPACE_SWITCH_LEFT = ["xdotool", "key", "ctrl+alt+Left"]
# WORKSPACE_SWITCH_RIGHT = ["xdotool", "key", "ctrl+alt+Right"]

# Custom actions (examples):
# Volume control
# WORKSPACE_SWITCH_LEFT = ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"]
# WORKSPACE_SWITCH_RIGHT = ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"]

# Debouncing: Minimum time (in seconds) between swipe actions
# Set to 0 to disable debouncing
# Increased to reduce sensitivity and prevent accidental triggers
DEBOUNCE_TIME = 0.5

# Verbose output (useful for debugging)
VERBOSE = True

# ============================================================================
# CODE
# ============================================================================

class MagicMouseGestureHandler:
    """Handles Magic Mouse gesture detection and action execution"""

    def __init__(self):
        self.last_action_time = 0
        self.device = None

    def find_magic_mouse(self):
        """Find and return the Magic Mouse input device"""
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        if VERBOSE:
            print("Available input devices:")
            for device in devices:
                print(f"  {device.path}: {device.name}")

        for device in devices:
            if "Magic Mouse" in device.name:
                return device

        return None

    def should_process_action(self):
        """
        Check if enough time has passed since last action (debouncing)
        Returns True if we should process the action, False otherwise
        """
        if DEBOUNCE_TIME <= 0:
            return True

        current_time = time.time()
        time_since_last = current_time - self.last_action_time

        if time_since_last >= DEBOUNCE_TIME:
            self.last_action_time = current_time
            return True

        return False

    def execute_action(self, command, direction):
        """
        Execute the workspace switch command

        Args:
            command: List of command arguments to execute
            direction: "left" or "right" for logging
        """
        if not self.should_process_action():
            return

        try:
            subprocess.run(command, check=False, capture_output=True)

            if VERBOSE:
                if direction == "left":
                    print(f"→ Switching workspace UP (swipe left detected)")
                elif direction == "right":
                    print(f"← Switching workspace DOWN (swipe right detected)")

        except Exception as e:
            print(f"Error executing action: {e}")

    def monitor_swipes(self):
        """
        Main loop: Monitor for horizontal swipe events and trigger actions
        """
        if VERBOSE:
            print("\n" + "="*60)
            print("Magic Mouse Workspace Switcher is running!")
            print("="*60)
            print("Swipe left/right with two fingers to change workspaces")
            print(f"Debounce time: {DEBOUNCE_TIME}s")
            print("Press Ctrl+C to stop\n")

        try:
            # Read events in a continuous loop
            for event in self.device.read_loop():
                # We only care about relative axis events (REL)
                if event.type == ecodes.EV_REL:
                    # Check if it's a horizontal wheel event (swipe)
                    if event.code == ecodes.REL_HWHEEL:
                        # Trigger on horizontal swipes
                        # Debouncing handles preventing rapid-fire triggers
                        if event.value < 0:  # Left swipe
                            self.execute_action(WORKSPACE_SWITCH_LEFT, "left")
                        elif event.value > 0:  # Right swipe
                            self.execute_action(WORKSPACE_SWITCH_RIGHT, "right")

        except KeyboardInterrupt:
            if VERBOSE:
                print("\n\nStopping Magic Mouse Workspace Switcher")

    def run(self):
        """Main entry point"""
        if VERBOSE:
            print("="*60)
            print("Magic Mouse 2 Workspace Switcher")
            print("="*60)

        # Find the Magic Mouse
        self.device = self.find_magic_mouse()

        if not self.device:
            print("\n✗ Magic Mouse not found!")
            print("\nTroubleshooting:")
            print("1. Make sure your Magic Mouse is paired and connected")
            print("2. Verify the Magic Mouse 2 driver is installed:")
            print("   libinput list-devices | grep 'Magic Mouse'")
            print("3. Check that the driver module is loaded:")
            print("   lsmod | grep hid_magicmouse")
            sys.exit(1)

        if VERBOSE:
            print(f"\n✓ Found: {self.device.name}")
            print(f"  Device: {self.device.path}\n")

        # Start monitoring
        try:
            self.monitor_swipes()
        except PermissionError:
            print("\n✗ Permission denied!")
            print("\nTo fix this:")
            print("1. Add yourself to the input group:")
            print(f"   sudo usermod -a -G input $USER")
            print("2. Log out and log back in")
            print("3. Or run this script with sudo (not recommended):")
            print(f"   sudo python3 {__file__}")
            sys.exit(1)

def main():
    """Application entry point"""
    handler = MagicMouseGestureHandler()
    handler.run()

if __name__ == "__main__":
    main()
