#!/bin/bash
set -eu

xset dpms force suspend
/usr/local/scripts/wm/i3-lock.py
systemctl suspend
