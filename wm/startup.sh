#!/bin/sh
set -eu

dir_make() {
	mkdir -m700 -p "/tmp/$USER/$1"
}

dir_make cache
dir_make mutt/{headers,bodies}
dir_make pacaur
dir_make pulse
dir_make vim_undo
exec /usr/local/scripts/wm/vi-keyswap.sh

