#!/bin/bash
set -eu -o pipefail

scrot -s --format png - | xclip -selection clipboard -t image/png -i
notify-send 'Screenshot copied to clipboard'
