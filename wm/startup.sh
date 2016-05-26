#!/bin/sh

/usr/local/scripts/wm/vim-keyswap.sh
mkdir -p "/tmp/$USER/"{vim_undo,pacaur}
uim-toolbar-gtk-systray &

disown

