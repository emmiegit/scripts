#!/bin/sh

# There's not way to go back in Pandora, so the
# pianobar option does nothing.
case "$(~/Scripts/wm/detect-audio-player.sh)" in
    mocp) mocp --prev ;;
    pianobar) ;;
    *) false ;;
esac

