#!/bin/bash
set -eu

# Pre-suspend preparation
/usr/local/scripts/wm/i3-lock.py
xset dpms force suspend

# Suspension
systemctl suspend

# Post-suspend recovery
/usr/local/scripts/wm/vi-keyswap.sh
/usr/local/scripts/wm/reset-repeat-rate.sh
systemctl --user restart ibus.service
