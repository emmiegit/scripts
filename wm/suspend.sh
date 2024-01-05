#!/bin/bash
set -eu

# Pre-suspend preparation
/usr/local/scripts/wm/i3-lock.py
xset dpms force suspend

# TODO suspend currently broken due to kernel update
## Suspension
#systemctl suspend
#
## Post-suspend recovery
#systemctl restart ibus.service
