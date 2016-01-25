#!/usr/bin/env bash

lockfile="/tmp/$USER-lockscreen.lock"   # The lock file to prevent multiple lock screens from triggering
lock='/usr/local/scripts/dat/lock.png'  # The image of a lock to superimpose on the screenshots
x_res=1920                              # The resolution of your monitor(s). This assumes both monitors
y_res=1200                              # are the same size.

if [ -f $lockfile ]; then
    exit 1
fi

on_exit() {
    rm -f $lockfile
    killall -SIGUSR2 dunst
}

trap on_exit EXIT SIGTERM SIGINT SIGHUP SIGSEGV

touch $lockfile
killall -SIGUSR1 dunst

# Detect number of monitors
case $(xrandr --query | grep -c ' connected') in
    1)
        maim --opengl --format png /dev/stdout \
            | convert /dev/stdin -scale 10% -scale 1000% /dev/stdout \
            | composite -gravity Center $lock /dev/stdin /dev/stdout \
            | i3lock -i /dev/stdin
        ;;
    2)
        left=$(mktemp /tmp/lockscreen-XXXXXX.png)
        right=$(mktemp /tmp/lockscreen-XXXXXX.png)
        maim --opengl --format png --geometry=${x_res}x${y_res}+0+0 /dev/stdout \
            | convert /dev/stdin -scale 10% -scale 1000% /dev/stdout \
            | composite -gravity Center $lock /dev/stdin $left &
        maim --opengl --format png --geometry=${x_res}x${y_res}+${x_res}+0 /dev/stdout \
            | convert /dev/stdin -scale 10% -scale 1000% /dev/stdout \
            | composite -gravity Center $lock /dev/stdin $right &
        wait
        convert +append $left $right /dev/stdout \
            | i3lock -i /dev/stdin
        rm -f $left $right
        ;;
    *)
        maim --opengl /dev/stdout \
            | i3lock -i /dev/stdin
        ;;
esac

