#!/usr/bin/env bash

# There's no way to go back in Pandora, so the
# pianobar option does nothing.
case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp)
        mocp --prev
        sleep .05
        mocp --pause
        ;;
    pianobar) ;;
    *) false ;;
esac

