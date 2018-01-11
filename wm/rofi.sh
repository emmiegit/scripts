#!/bin/sh
exec rofi -show run -modi run \
	-font 'mono 12' -columns 3 \
	-disable-history \
	-color-window '#222222, #222222, #b1b4b3' \
	-color-normal '#222222, #b1b4b3, #222222, #005577, #b1b4b3' \
	-color-active '#222222, #b1b4b3, #222222, #007763, #b1b4b3' \
	-color-urgent '#222222, #b1b4b3, #222222, #77003d, #b1b4b3' \
	-kb-row-select 'Tab' -kb-row-tab ''
