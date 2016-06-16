#!/bin/sh

# TODO: figure out how to remove an item from MOC's playlist
case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mocp) ;;
	pianobar) printf '-' > ~/.config/pianobar/ctl ;;
	vlc) dbus-send --session --dest=org.mpris.vlc /Player org.freedesktop.MediaPlayer.Stop ;;
	*) false ;;
esac

