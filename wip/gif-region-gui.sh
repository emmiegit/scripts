#!/bin/bash

# Delay before starting
DELAY=2

# Sound notification to let one know when recording is about to start (and ends)
beep() {
	paplay /usr/share/sounds/KDE-Im-Irc-Event.ogg &
}

# Default recording duration
DEFDUR=5

# Duration and output file
if [ $# -gt 0 ]; then
	D="--duration=$@"
else
	# Custom recording duration as set by user
	USERDUR=$(gdialog --title "Duration?" --inputbox "Please enter the screencast duration in seconds" 200 100 2>&1)

	# Duration and output file
	if [ $USERDUR -gt 0 ]; then
		D=$USERDUR
	else
		D=$DEFDUR
	fi

fi

# xrectsel from https://github.com/lolilolicon/xrectsel
ARGUMENTS=$(xrectsel "--x=%x --y=%y --width=%w --height=%h") || exit -1

echo Delaying $DELAY seconds. After that, byzanz will start
for (( i=$DELAY; i>0; --i )) ; do
	echo $i
	sleep 1
done
beep
byzanz-record --verbose --delay=0 ${ARGUMENTS} $D
beep

# Notify the user of end of recording.
notify-send "GIFRecorder" "Screencast saved to $FOLDER/GIFrecord_$TIME.gif"

