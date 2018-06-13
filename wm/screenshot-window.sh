#!/bin/sh
exec maim -u -i "$(xdotool getactivewindow)" "$HOME/Incoming/$(date +%s).png"
#exec scrot -u "$HOME/Incoming/$(date +%s).png"
