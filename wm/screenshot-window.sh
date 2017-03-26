#!/bin/sh
exec maim -u -i "$(xdotool getactivewindow)" "$HOME/Incoming/$(date +%s).png"

