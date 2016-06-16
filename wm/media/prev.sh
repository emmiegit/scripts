#!/bin/sh

# There's not way to go back in Pandora, so the
# pianobar option does nothing.
case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mocp) mocp --prev ;;
	pianobar) ;;
	vlc) dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous ;;
	*) false ;;
esac

