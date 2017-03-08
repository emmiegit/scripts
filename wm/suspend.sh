#!/bin/sh
SUSPEND=true

if $SUSPEND; then
	notify-send 'Suspending computer...'
else
	notify-send 'Not suspending, only locking...'
fi

/usr/local/scripts/wm/lock.sh
xset dpms force suspend
$SUSPEND && systemctl suspend

