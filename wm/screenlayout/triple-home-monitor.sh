#!/bin/bash
set -eu

(
	sleep 10;
	/usr/local/scripts/wm/new-wallpaper.sh
) &

exec xrandr \
	--output DVI-D-0 \
		--mode 1280x1024 \
		--pos 3840x0 \
		--rotate normal \
	--output DP-0 \
		--off \
	--output DP-1 \
		--off \
	--output DP-2 \
		--off \
	--output DP-3 \
		--mode 1920x1200 \
		--pos 0x0 \
		--rotate normal \
	--output DP-4 \
		--off \
	--output DP-5 \
		--primary \
		--mode 1920x1200 \
		--pos 1920x0 \
		--rotate normal \
	--output HDMI-0 \
		--same-as DP-5
