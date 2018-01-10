#!/bin/bash
set -eu

pamixer "$@"
notify-send "Muted: $(pamixer --get-mute)"
