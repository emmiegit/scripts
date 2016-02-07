#!/bin/sh

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) ;;
    pianobar) printf '+' > ~/.config/pianobar/ctl ;;
    vlc) ;;
    *) false ;;
esac

