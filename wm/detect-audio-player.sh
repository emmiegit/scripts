#!/usr/bin/env bash

detect-mocp() {
    case "$(mocp --info 2>&1 | grep State)" in
        'State: PLAY') return 0 ;;
        'State: PAUSE') return 0 ;;
        'State: STOP') return 1 ;;
        *) return 1 ;;
    esac
}

detect-pianobar() {
    pgrep -U $UID pianobar > /dev/null
}

if detect-mocp; then
    printf "mocp"
elif detect-pianobar; then
    printf "pianobar"
else
    printf "unknown"
fi

