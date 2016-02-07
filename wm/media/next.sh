#!/bin/sh

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --next ;;
    pianobar) printf 'n' > ~/.config/pianobar/ctl ;;
    vlc) dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next ;;
    *) false ;;
esac

