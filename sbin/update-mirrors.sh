#!/bin/sh
set -e

cd /etc/pacman.d

if [ $EUID != 0 ]; then
	echo 'Warning: not root.'
fi

if [ ! -f mirrorlist.pacnew ]; then
	echo 'No mirrorlist.pacnew!'
	exit 1
fi

echo 'Backing up old mirror list...'
mv -f mirrorlist mirrorlist.old
cp -f mirrorlist.pacnew mirrorlist.bak

echo 'Please uncomment any mirrors you would like to use:'
"$EDITOR" mirrorlist.bak

echo 'Ranking mirrors...'
rankmirrors mirrolist.bak > mirrorlist

