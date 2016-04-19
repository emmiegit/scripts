#!/bin/sh

/usr/local/scripts/wm/vim-keyswap.sh
mkdir -p "/tmp/$USER/pacaur"
ln -s "/tmp/pacaurtmp-$USER" "/tmp/$USER/pacaur"
#uim-toolbar-gtk-systray &

#disown

