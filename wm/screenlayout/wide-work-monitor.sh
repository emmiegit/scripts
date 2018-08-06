#!/bin/sh
exec xrandr \
	--output HDMI1 \
		--off \
	--output VIRTUAL1 \
		--off \
	--output DP1 \
		--off \
	--output eDP1 \
		--mode 1920x1080 \
		--pos 0x704 \
		--rotate normal \
	--output DP2 \
		--primary \
		--mode 2560x1080 \
		--pos 1920x0 \
		--rotate normal
