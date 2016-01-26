#!/usr/bin/env bash

# Liking a song already in your music library isn't meaningful, so it does nothing.
case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) ;;
    pianobar) printf '+' > ~/.config/pianobar/ctl ;;
    *) false ;;
esac

