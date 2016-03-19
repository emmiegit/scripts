#!/bin/sh
HIBERNATE=true

if $HIBERNATE && [ "$(cat /etc/hostname)" != 'Titus' ]; then
    notify-send 'Hibernating computer...'
else
    notify-send 'Not hibernating, only locking...'
fi

/usr/local/scripts/wm/lock.sh
xset dpms force suspend
$HIBERNATE && systemctl hibernate
