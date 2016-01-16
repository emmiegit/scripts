#!/usr/bin/env bash

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --next ;;
    pianobar) printf 'n' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac

