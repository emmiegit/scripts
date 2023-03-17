#!/bin/bash
set -eu

# Pre-suspend preparation
/usr/local/scripts/wm/i3-lock.py
xset dpms force suspend

# Suspension
systemctl suspend

# Post-suspend recovery
systemctl restart ibus.service
