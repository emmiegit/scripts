#!/bin/bash

STATUS_FILE='/usr/local/scripts/dat/autolock_state'

restart_autolock() {
	pkill -U "${USER}" xautolock
	/usr/local/scripts/wm/start-autolock.sh

	if [[ $? -gt 0 ]]; then
	    notify-send 'Unable to restart autolock process.'
	    return 1
	else
	    case "$1" in
	        on)
	            xautolock -enable
	            notify-send 'Started autolock process.'
	            ;;
	        off)
	            pkill -U "${USER}" xautolock
	            notify-send 'Killed autolock process.'
	            ;;
	    esac
	fi
}

main() {
	case "$1" in
	    on)
	        xset +dpms
	        xautolock -enable \
	            && notify-send 'Computer autolock enabled.' \
	            || restart_autolock "$1"
	        ;;
	    off)
	        xset s -dpms
	        xautolock -disable \
	            && notify-send 'Computer autolock disabled.' \
	            || restart_autolock "$1"
	        ;;
	    *)
	        echo >&2 "\"$1\" is not either \"on\" or \"off\"."
	        return 1
	        ;;
	esac
	echo "$1" > "${STATUS_FILE}"
}

main "$1"

