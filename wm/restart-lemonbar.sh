#!/bin/sh

LEMONBAR_PIDFILE="/run/user/$UID/lemonbar.pid"

if [ -f "$LEMONBAR_PIDFILE" ]; then
    kill "$(cat "$LEMONBAR_PIDFILE")"
fi

"$HOME/.config/i3/lemonbar/main.py" </dev/null >/dev/null 2>&1 &
disown

