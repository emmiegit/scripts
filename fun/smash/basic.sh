#!/usr/bin/env bash
source buttons.sh

left_special() {
    left &
    b
}

right_special() {
    right &
    b
}

#FIXME
up_smash() {
    if [ -z "$1" ]; then
        cstick_up
    else
        up $1 &
        sleep .1
        a $1
    fi
}

#FIXME
down_smash() {
    down_tap &
    a $1
}

left_smash() {
    left &
    a $1
}

right_smash() {
    right &
    a $1
}

up_tilt() {
    up_tap &
    a
}

down_tilt() {

    down .3 &
    a
}

left_tilt() {
    left_tap &
    a
}

right_tilt() {
    right_tap &
    a
}

run_left() {
    # Usage: run_left [duration]
    if [ ! -z "$1" ]; then
        local duration="$1"
    else
        local duration='.1'
    fi

    press $LEFT "sleep $duration"
}

walk_left() {
    # Usage: walk_left [duration]
    if [ ! -z "$1" ]; then
        local duration="$1"
    else
        local duration='.1'
    fi

    press $LEFT_TAP "sleep $duration"
}

run_right() {
    # Usage: run_right [duration]
    if [ ! -z "$1" ]; then
        local duration="$1"
    else
        local duration='.1'
    fi

    press $RIGHT "sleep $duration"
}

walk_right() {
    # Usage: walk_right [duration]
    if [ ! -z "$1" ]; then
        local duration="$1"
    else
        local duration='.1'
    fi

    press $RIGHT_TAP "sleep $duration"
}

dash_attack_left() {
    # Usage: dash_attack_left [duration]
    run_left "$1"
    a
}

dash_attack_right() {
    # Usage: dash_attack_right [duration]
    run_right "$1"
    a
}

tumble_left() {
    press $L "left"
}

tumble_right() {
    press $L "right"
}

spot_dodge() {
    press $L "down .3"
}

