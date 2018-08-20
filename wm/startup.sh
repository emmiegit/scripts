#!/bin/sh
set -eu

dir_make() {
	for dir in "$@"; do
		mkdir -m700 -p "/tmp/$USER/$dir"
	done
}

mkdir -m777 -p "/tmp/shared"
dir_make aur
dir_make cache
dir_make vim_undo
dir_make private
ln -sf "/tmp/$USER/aur" "$HOME/.cache/yay"

/usr/local/scripts/wm/screenlayout/run.sh
