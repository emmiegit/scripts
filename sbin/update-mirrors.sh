#!/bin/bash
set -eu

echodo() {
	echo "$@"
	sudo "$@"
}

rank_and_update() {
	echo 'Ranking mirrors...'
	rankmirrors mirrorlist.bak > mirrorlist

	echo 'Updating git repo...'
	etckeeper commit 'Update mirrorlist.'
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
sudoedit mirrorlist.bak
sudo rank_and_update
