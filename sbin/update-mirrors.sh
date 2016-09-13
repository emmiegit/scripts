#!/bin/sh
set -eu

echodo() {
	echo "$@"
	"$@"
}

main() {
	if [ ! -f mirrorlist.pacnew ]; then
		echo 'No mirrorlist.pacnew!'
		exit 1
	fi

	echo 'Backing up old mirror list...'
	echodo mv -f mirrorlist mirrorlist.old
	echodo cp -f mirrorlist.pacnew mirrorlist.bak

	echo 'Please uncomment any mirrors you would like to use:'
	vim mirrorlist.bak

	echo 'Ranking mirrors...'
	rankmirrors mirrorlist.bak > mirrorlist
}

if [ $EUID != 0 ]; then
	sudo "$0"
	exit 0
fi

cd /etc/pacman.d

main

