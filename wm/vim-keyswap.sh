#!/bin/bash

if [[ ! -z $DISPLAY ]]; then
    if echo `xmodmap` | grep -q "Caps_Lock (0x42)"; then
        xmodmap /usr/local/scripts/dat/xmodmap-vim-keyswap
    fi
fi
