#!/usr/bin/env bash

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --next && mocp --pause ;;
    pianobar) printf 'nS' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac

