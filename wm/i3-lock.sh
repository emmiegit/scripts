#!/bin/bash
set -eu

# The lock file to prevent multiple lock screens from triggering
lockfile="/tmp/${USER}-lockscreen.lock"

# The image of a lock to superimpose on the screenshots
lockimage='/usr/local/scripts/dat/lock.png'

# The resolution of your monitor(s). This assumes both monitors
# are the same size.
x_res=1920
y_res=1200

# The pixelation effect. These two numbers need to multiply
# to 10,000.
small_scale=5
large_scale=2000

if [[ -f "$lockfile" ]]; then
	exit 1
else
	touch "$lockfile"
fi

monitors="$(xrandr --query | grep -c ' connected')"

if [[ "$monitors" == 2 ]]; then
	left="$(mktemp /tmp/lockscreen-XXXXXXXX.png)"
	right="$(mktemp /tmp/lockscreen-XXXXXXXX.png)"
else
	left=
	right=
fi

on_exit() {
	[[ "$monitors" == 2 ]] && rm -f "$left" "$right"

	rm -f "$lockfile"
	killall -SIGUSR2 dunst || true
}

trap on_exit EXIT SIGTERM SIGINT SIGHUP SIGSEGV

killall -SIGUSR1 dunst || true

# Display lock screen depending on number of monitors
case "$monitors" in
	1)
		maim --opengl --format png /dev/stdout \
			| convert /dev/stdin -scale "$small_scale%" -scale "$large_scale%" /dev/stdout \
			| composite -gravity Center "$lockimage" /dev/stdin /dev/stdout \
			| i3lock -i /dev/stdin
		;;
	2)
		maim --opengl --format png --geometry="${x_res}x${y_res}+0+0" /dev/stdout \
			| convert /dev/stdin -scale "$small_scale%" -scale "$large_scale%" /dev/stdout \
			| composite -gravity Center "$lockimage" /dev/stdin "$left" &
		maim --opengl --format png --geometry="${x_res}x${y_res}+${x_res}+0" /dev/stdout \
			| convert /dev/stdin -scale "$small_scale%" -scale "$large_scale%" /dev/stdout \
			| composite -gravity Center "$lockimage" /dev/stdin "$right" &
		wait
		convert +append "$left" "$right" /dev/stdout \
			| i3lock -i /dev/stdin
		;;
	*)
		maim --opengl /dev/stdout \
			| i3lock -i /dev/stdin
		;;
esac

