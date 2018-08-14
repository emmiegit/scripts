#!/bin/sh
exec xrandr \
	--output VGA-0 \
		--mode 1280x1024 \
		--pos 3840x0 \
		--rotate normal \
	--output DVI-D-0 \
		--primary \
		--mode 1920x1200 \
		--pos 1920x0 \
		--rotate normal \
	--output DVI-D-1 \
		--mode 1920x1200 \
		--pos 0x0 \
		--rotate normal \
	--output HDMI-0 \
		--off
