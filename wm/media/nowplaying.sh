#!/bin/sh

case "$(/usr/local/scripts/wm/media/detect-audio-player.sh)" in
	mpd)
		mpc -f '%title% by %artist%'
		;;
	mocp)
		mocp -Q '%song by %artist'
		;;
	pianobar)
		local fn="${HOME}/.config/pianobar/nowplaying"
		if [ ! -f "$fn" ]; then
			echo '(error)'
		else
			local artist=$(grep -Po "(?<=^artist=).*" "$fn")
			local title=$(grep -Po "(?<=^title=).*" "$fn")
			echo "$title by $artist"
		fi
		;;
	vlc)
		local title="$(qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get org.mpris.MediaPlayer2.Player Metadata | grep '^xesam:title: ')"
		echo "${title:13}"
		;;
	*)
		echo '(none)'
		;;
esac
