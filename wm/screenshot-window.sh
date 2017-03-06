#!/bin/sh
exec maim -i "$(xdotool getactivewindow)" "$HOME/Incoming/$(date +%s).png"

