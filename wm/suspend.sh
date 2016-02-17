#!/bin/sh
notify-send 'Suspending computer...'
/usr/local/scripts/wm/lock.sh
systemctl suspend

