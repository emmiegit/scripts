#!/bin/sh
HIBERNATE=true

if $HIBERNATE; then
    notify-send 'Hibernating computer...'
else
    notify-send 'Not hibernating, only locking...'
fi

/usr/local/scripts/wm/lock.sh
$HIBERNATE && systemctl hibernate

