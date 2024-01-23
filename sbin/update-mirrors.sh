#!/bin/bash
set -eu

if [[ $EUID != 0 ]]; then
	exec sudo -E "$0" "$@"
fi

echodo() {
	echo "$@"
	"$@"
}

cd /etc/pacman.d

if [[ ! -f mirrorlist.pacnew ]]; then
	echo 'No mirrorlist.pacnew!'
	exit 1
fi

echo 'Backing up old mirror list...'
echodo mv -f mirrorlist mirrorlist.old
echodo cp -f mirrorlist.pacnew mirrorlist.bak

echo 'Please uncomment any mirrors you would like to use:'
"$EDITOR" mirrorlist.bak
echodo sed -i '/^#/d' mirrorlist.bak

echo 'Ranking mirrors...'
rankmirrors mirrorlist.bak > mirrorlist

echo 'Updating git repo...'
etckeeper commit 'Update mirrorlist.'
