#!/bin/sh
set -eu

hibernate=true

if "$hibernate"; then
	notify-send 'Hibernating computer...'
else
	notify-send 'Not hibernating, only locking...'
fi

/usr/local/scripts/wm/lock
$hibernate && systemctl hibernate
