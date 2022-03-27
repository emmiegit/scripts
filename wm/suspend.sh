#!/bin/bash
set -eu

/usr/local/scripts/wm/i3-lock.py
xset dpms force suspend
systemctl suspend
