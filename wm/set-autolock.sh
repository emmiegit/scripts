#!/usr/bin/env bash

restart_autolock() {
    pkill xautolock
    ~/Scripts/wm/start-autolock.sh

    if [[ $? -gt 0 ]]; then
        notify-send 'Unable to restart autolock process.'
        return 1
    else
        case "$1" in
            on)
                xautolock -enable
                notify-send 'Restarted autolock process. Autolock enabled.'
                ;;
            off)
                xautolock -disable
                notify-send 'Restarted autolock process. Autolock disabled.'
                ;;
        esac
    fi
}

main() {
    case "$1" in
        on)
            xautolock -enable \
                && notify-send 'Computer autolock enabled.' \
                || restart_autolock "$1"
            ;;
        off)
            xautolock -disable \
                && notify-send 'Computer autolock disabled.' \
                || restart_autolock "$1"
            ;;
        *)
            echo "\"$1\" is not either \"on\" or \"off\"." >&2
            ;;
    esac
}

main "$1"

