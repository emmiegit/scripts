#!/bin/bash

case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mpd) echo 'Not implemented yet'; false ;;
	mocp) echo 'Not implemented yet'; false ;;
	pianobar) printf '-' > ~/.config/pianobar/ctl ;;
	vlc) dbus-send --session --dest=org.mpris.vlc /Player org.freedesktop.MediaPlayer.Stop ;;
	*) false ;;
esac
