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
    pgrep -U "$UID" pianobar > /dev/null
}

if detect-pianobar; then
    printf "pianobar"
elif detect-mocp; then
    printf "mocp"
else
    printf "unknown"
fi

