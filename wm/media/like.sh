#!/bin/sh

case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mocp) ;;
	pianobar) printf '+' > ~/.config/pianobar/ctl ;;
	vlc) ;;
	*) false ;;
esac

