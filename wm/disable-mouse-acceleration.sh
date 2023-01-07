#!/bin/bash
set -ux

# Per-device
xinput --set-prop '2.4G Mouse' 'libinput Accel Speed' 0
xinput --set-prop 'USB Optical Mouse' 'libinput Accel Speed' -0.25
