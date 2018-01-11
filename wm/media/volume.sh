#!/bin/bash
set -eu

pamixer "$@"
notify-send "Volume: $(pamixer --get-volume)"
