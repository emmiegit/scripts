#!/bin/bash
source buttonids.sh

# Helper functions
press() {
	# Usage: press key-id action
	local key=$1
	xdotool keydown $key
	shift
	$@
	xdotool keyup $key
}

# Basic button presses
a() {
	# Usage: a [duration]
	if [ ! -z "$1" ]; then
	    local duration="$1"
	else
	    local duration='.1'
	fi

	xdotool keydown $A
	sleep $duration
	xdotool keyup $A
}

b() {
	# Usage: a [duration]
	if [ ! -z "$1" ]; then
	    local duration="$1"
	else
	    local duration='.1'
	fi

	xdotool keydown $B
	sleep $duration
	xdotool keyup $B
}

short_hop() {
	xdotool key $X
}

jump() {
	press $X "sleep .1"
}

grab() {
	xdotool key $Z
}

up() {
	xdotool key $UP
}

up_tap() {
	press $UP
}

down() {
	xdotool key $DOWN
}

down_tap() {
	press $DOWN
}

left() {
	xdotool key $LEFT
}

left_tap() {
	press $LEFT
}

right() {
	xdotool key $RIGHT
}

right_tap() {
	press $RIGHT
}

cstick_up() {
	xdotool key $CSTICK_UP
}

cstick_down() {
	press $CSTICK_DOWN "sleep .1"
}

cstick_left() {
	press $CSTICK_LEFT "sleep .1"
}

cstick_right() {
	press $CSTICK_RIGHT "sleep .1"
}

shield() {
	# Usage: shield [duration]
	if [ ! -z "$1" ]; then
	    local duration="$1"
	else
	    local duration='.1'
	fi

	press $L "sleep $duration"
}

taunt() {
	xdotool key $DPAD_UP
}

