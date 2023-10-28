#!/bin/bash

detect_mpd() {
	source "${0%/*}/mpc.sh"
	case "$(mpc current 2>&1)" in
		'') return 1 ;;
		*) return 0 ;;
	esac
}

detect_mocp() {
	case "$(mocp --info 2>&1 | grep State)" in
		'State: PLAY') return 0 ;;
		'State: PAUSE') return 0 ;;
		'State: STOP') return 1 ;;
		*) return 1 ;;
	esac
}

detect_vlc() {
	case "$(qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get \
		org.mpris.MediaPlayer2.Player PlaybackStatus 2>&1)" in
		'Playing') return 0 ;;
		'Paused') return 0 ;;
		'Stopped') return 1 ;;
		*) return 1 ;;
	esac
}

detect_pianobar() {
	pgrep -U "$UID" pianobar > /dev/null
}

if detect_pianobar; then
	printf pianobar
elif detect_vlc; then
	printf vlc
elif detect_mocp; then
	printf mocp
elif detect_mpd; then
	printf mpd
else
	printf '(unknown)'
fi
