#!/usr/bin/env bash

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --stop ;;
    pianobar) printf 'q' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac
