#!/bin/bash
set -e

echo "Warning: buggy interaction with sloppy mouse focus."

move_mouse_to_frame() {
	eval $(xwininfo -id $(xdotool getactivewindow) |
		sed -n -e "s/^ \+Absolute upper-left X: \+\([0-9]\+\).*/X=\1/p" \
			   -e "s/^ \+Absolute upper-left Y: \+\([0-9]\+\).*/Y=\1/p" ) &&
	xdotool mousemove $X $Y
}

if [[ -z `wmctrl -xl | grep "nautilus\.Nautilus"` ]]; then
	nautilus "$1" &
else
	oldclip="$(xclip -o -sel clip)"
	eval $(xdotool getmouselocation --shell)
	echo -n "$1" | xclip -i -sel clip
	wmctrl -xF -R nautilus.Nautilus
	sleep .01
	#move_mouse_to_frame
	xdotool key ctrl+t ctrl+l ctrl+v Return
	echo -n "$oldclip" | xclip -i -sel clip
	sleep .5
	#xdotool mousemove $X $Y
fi

