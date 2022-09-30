#!/bin/bash
set -eux

# Device-specific settings
xinput --set-prop '2.5G Mouse' 'libinput Accel Speed' 0.25
xinput --set-prop 'USB Optical Mouse' 'libinput Accel Speed' -0.25

# Disable acceleration
xset m 0 0
