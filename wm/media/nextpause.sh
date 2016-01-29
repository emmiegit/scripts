#!/usr/bin/env bash

case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp)
        mocp --next
        sleep .05
        mocp --pause
        ;;
    pianobar)
        printf 'n' > ~/.config/pianobar/ctl
        sleep .05
        printf 'S' > ~/.config/pianobar/ctl
        ;;
    *)
        false
        ;;
esac

