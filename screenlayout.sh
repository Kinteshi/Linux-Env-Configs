#!/bin/sh
if xrandr | grep -q "HDMI-1 connected"; then
    # If it is, set the resolution to 1920x1080 and set the primary monitor to HDMI-1 at 75Hz
    xrandr --output eDP-1 --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-1 --primary --mode 2560x1080 --pos 1920x0 --rotate normal --output DP-1 --off --output HDMI-2 --off
else
    # If it isn't, set the set the primary monitor to eDP-1
    xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-1 --off --output DP-1 --off --output HDMI-2 --off
fi
