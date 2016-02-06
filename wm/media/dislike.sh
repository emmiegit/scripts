#!/bin/sh

# TODO: figure out how to remove an item from MOC's playlist
case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) ;;
    pianobar) printf '-' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac

