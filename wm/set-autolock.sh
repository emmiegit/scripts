#!/usr/bin/env bash

case "$1" in
    on)
        xautolock -enable
        notify-send 'Computer autolock enabled.'
        ;;
    off)
        xautolock -disable
        notify-send 'Computer autolock disabled.'
        ;;
    *)
        echo "\"$1\" is not either \"on\" or \"off\"." >&2
        ;;
esac

