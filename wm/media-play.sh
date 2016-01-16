#!/usr/bin/env bash

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --toggle-pause ;;
    pianobar) printf 'p' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac

