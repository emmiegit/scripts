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
}

trap on_exit EXIT SIGTERM SIGINT SIGHUP SIGSEGV

touch $lockfile
notify-send 'Locking screen...'

# Detect number of monitors
case $(xrandr --query | grep ' connected' | wc -l) in
    1)
        screen=$(mktemp /tmp/lockscreen-XXXXXX.png)
        result=$(mktemp /tmp/lockscreen-XXXXXX.png)
        maim --opengl $screen
        convert $screen -scale 10% -scale 1000% $screen
        composite -gravity Center $lock $screen $result
        rm -f $screen $result
        ;;
    2)
        left=$(mktemp /tmp/lockscreen-XXXXXX.png)
        right=$(mktemp /tmp/lockscreen-XXXXXX.png)
        left_2=$(mktemp /tmp/lockscreen-XXXXXX.png)
        right_2=$(mktemp /tmp/lockscreen-XXXXXX.png)
        result=$(mktemp /tmp/lockscreen-XXXXXX.png)
        maim --opengl --geometry=${x_res}x${y_res}+0+0 $left
        maim --opengl --geometry=${x_res}x${y_res}+${x_res}+0 $right
        convert $left -scale 10% -scale 1000% $left
        convert $right -scale 10% -scale 1000% $right
        composite -gravity Center $lock $left $left_2
        composite -gravity Center $lock $right $right_2
        convert +append $left_2 $right_2 $result
        i3lock -i $result
        rm -f $left $left_2 $right $right_2 $result
        ;;
    *)
        screen=$(mktemp /tmp/lockscreen-XXXXXX.png)
        i3lock -i $screen
        rm -f $screen
        ;;
esac


