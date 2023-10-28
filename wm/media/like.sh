#!/bin/bash

case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mpd) ;;
	mocp) ;;
	pianobar) printf '+' > ~/.config/pianobar/ctl ;;
	vlc) ;;
	*) false ;;
esac
