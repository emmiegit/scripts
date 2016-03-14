#!/usr/bin/env bash

if [[ $EUID == 0 ]]; then
    sudo -u ammon "$0"
    exit
fi

if [[ -z $DISPLAY ]]; then
    export DISPLAY=:0
fi

xsetwacom --set 'Wacom Intuos S 2 Pen stylus' Area 2000 2000 5000 5680

