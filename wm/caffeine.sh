#!/bin/bash

# Prevent xscreensaver from running.

PIDFILE=/tmp/$USER-caffeine.pid
NOTIFY=false

is_running() {
	[[ -f $PIDFILE ]] && kill -0 `cat $PIDFILE` 2> /dev/null
	return $?
}

caffeinate() {
	while true; do
		sleep 55
		xscreensaver-command -deactivate > /dev/null 2>&1
		xdotool key shift
	done
}

notify() {
	if $NOTIFY; then
		notify-send "Caffeine" "$1"
	else
		echo "$1"
	fi
}

print_usage() {
	echo "Usage: $(basename "$0") [flags] (start|stop|restart|toggle|status|help)"
}

usage_and_exit() {
	print_usage
	exit 1
}

help_and_exit() {
	print_usage
	echo "Flags:"
	echo " --notify  Use notify-send to push notifications to the screen."
	exit 0
}

do_start() {
	if is_running; then
		notify "Caffeine is already running."
		exit 1
	else
		echo "Starting Caffeine..."
		caffeinate & disown
		notify "Caffeine started: pid $!"
		echo $! > $PIDFILE
		exit $?
	fi
}

do_stop() {
	if ! is_running; then
		notify "Caffeine is not running."
		exit 1
	else
		echo "Stopping Caffeine..."
		kill `cat $PIDFILE`
		rm $PIDFILE
		notify "Caffeine stopped."
		exit $?
	fi
}

[[ $# -eq 0 ]] && usage_and_exit

while [[ $# -gt 1 ]]; do
	case "$1" in
		--notify) NOTIFY=true ;;
		*)
			echo "Unknown flag: $1."
			exit 1
			;;
	esac
	shift
done

case "$1" in
	start) do_start ;;
	stop) do_stop ;;
	restart)
		do_stop
		sleep 1
		if is_running; then
			notify "Unable to stop Caffeine."
			exit 1
		fi

		do_start
		sleep 1
		if ! is_running; then
			notify "Unable to start Caffeine."
			exit 1
		fi
		;;
	toggle)
		if is_running; then
			echo "Toggle: stopping Caffeine."
			stop
		else
			echo "Toggle: starting Caffeine."
			start
		fi
		;;
	status)
		if is_running; then
			notify "Caffeine is running, process id `cat $PIDFILE`."
		else
			notify "Caffeine is not running."
		fi
		;;
	help)
		help_and_exit
		;;
	*)
		echo "Unknown option: $1."
		usage_and_exit
		;;
esac

