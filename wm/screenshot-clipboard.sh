#!/bin/sh
maim -u -s --format png /dev/stdout | xclip -selection clipboard -t image/png -i
notify-send 'Screenshot copied to clipboard'
