#!/bin/sh
exec maim -u -i "$(xdotool getactivewindow)" "$HOME/incoming/$(date +%s).png"
