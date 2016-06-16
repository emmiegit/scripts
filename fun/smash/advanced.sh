#!/usr/bin/env bash
source basic.sh

left_aerial() {
	short_hop
	sleep .4
	cstick_left
}

right_aerial() {
	short_hop
	sleep .4
	cstick_right
}

#FIXME
up_aerial() {
	short_hop
	sleep .8
	cstick_up
}

#FIXME
down_aerial() {
	short_hop
	sleep .85
	cstick_down
}

#FIXME
left_wave_dash() {
	short_hop &
	sleep .9
	shield
	#down
	#left
}

right_wave_dash() {
	short_hop
	shield
	down
	right
}

dash_dance() {
	# Usage: dash_dance [duration]
	local starttime=`date +%s`
	while [ $((`date +%s` - $starttime)) -le "$1" ]; do
		run_left
		run_right
	done
}

