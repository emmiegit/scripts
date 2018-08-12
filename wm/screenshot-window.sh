#!/bin/sh
exec maim -u -i "$(xdotool getactivewindow)" "$HOME/incoming/$(date +%s).png"
#exec scrot -u "$HOME/incoming/$(date +%s).png"
