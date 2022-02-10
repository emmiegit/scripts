#!/bin/sh
SUSPEND=true

if $SUSPEND; then
	notify-send 'Suspending computer...'
else
	notify-send 'Not suspending, only locking...'
fi

/usr/local/scripts/wm/i3-lock.sh
xset dpms force suspend
$SUSPEND && systemctl suspend
