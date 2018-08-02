#!/bin/sh
exec xrandr \
	--output HDMI1 \
		--off \
	--output VIRTUAL1 \
		--off \
	--output DP1 \
		--off \
	--output eDP1 \
		--primary \
		--mode 1920x1080 \
		--pos 0x1080 \
		--rotate normal \
	--output DP2 \
		--mode 2560x1080 \
		--pos 1336x0 \
		--rotate normal
