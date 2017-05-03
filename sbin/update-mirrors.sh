#!/bin/sh
set -eu

echodo() {
	echo "$@"
	sudo "$@"
}

cd /etc/pacman.d

if [ ! -f mirrorlist.pacnew ]; then
	echo 'No mirrorlist.pacnew!'
	exit 1
fi

echo 'Backing up old mirror list...'
echodo mv -f mirrorlist mirrorlist.old
echodo cp -f mirrorlist.pacnew mirrorlist.bak

echo 'Please uncomment any mirrors you would like to use:'
sudoedit mirrorlist.bak

echo 'Ranking mirrors...'
sudo su -c 'rankmirrors mirrorlist.bak > mirrorlist'
