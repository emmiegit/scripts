#!/usr/bin/env bash
set -eu

DEST="$HOME/Documents/Relic/Private"
LOCK="$DEST/.$1"
EXT=7z
HASH_SCRIPT="$HOME/Programming/mhash/media-hash.py"
FILE_TREE_SCRIPT='/usr/local/scripts/arch/ft_diff.py'
CLEAR_RECENT=false
TEST_ARCHIVE=false
_remove_lock=true

on_sigterm() {
	printf 'Caught user interrupt, closing down.\n'
	if [[ -f $LOCK ]] && "$_remove_lock"; then
		rm -f "$LOCK"
	else
		printf 'Warning: can'\''t remove lock file.'
	fi
	exit 1
}

on_exit() {
	printf 'Finished.\n'
	if [[ -f $LOCK ]] && "$_remove_lock"; then
		rm -f "$LOCK"
	else
		printf 'Warning: can'\''t remove lock file.\n'
	fi
	exit 0
}

trap on_sigterm SIGTERM SIGINT
trap on_exit EXIT

# Lock check
if [[ -f $LOCK ]]; then
	printf >&2 'This script is already running.\n'
	_remove_lock=false
	read -r
	exit 1
fi

# Sanity tests
if [[ ! -d $DEST ]]; then
	printf >&2 'Destination directory does not exist.\n'
	exit 1
fi

varch() {
	ARCHIVE="$1.$EXT"
	cd "$DEST"
	touch "$LOCK"

	if [[ -d $1 ]]; then
		printf '[Compressing]\n'
		read -rsp 'Password: ' password
		printf 'Hashing images...\n'
		"$HASH_SCRIPT" "$DEST/$1"
		printf 'Checking file diff...\n'
		"$FILE_TREE_SCRIPT" "$DEST/$1"
		printf 'Backing up old archive...\n'
		[[ -f $ARCHIVE ]] && mv -u "$ARCHIVE" "$ARCHIVE~"
		printf 'Adding files to archive...\n'
		7z a -p"$password" -t7z -ms=on -mhe=on -m0=lzma -mx=3 "$ARCHIVE" "$1"
		"$TEST_ARCHIVE" && 7z t -p"$password" "$ARCHIVE"
		printf 'Removing old files...\n'
		rm -r "${1:?}/"
		if "$CLEAR_RECENT"; then
			printf 'Clearing recent documents...\n'
			: > ~/.local/share/recently-used.xbel
			printf 'Clearing thumbnails...\n'

			if [[ -d ~/.thumbnails ]]; then
				rm -f ~/.thumbnails/normal/*
				rm -f ~/.thumbnails/large/*
			else
				rm -f ~/.cache/thumbnails/normal/*
				rm -f ~/.cache/thumbnails/large/*
			fi
		fi
	elif [[ ! -f $ARCHIVE ]]; then
		printf '[Error]\n'
		printf 'Cannot find archive at %s!\n' "$ARCHIVE"
	else
		printf '[Extracting]\n'
		read -rsp 'Password: ' password
		7z x -p"$password" "$ARCHIVE"
	fi
}

if [[ $# -eq 0 ]]; then
	read -rp 'Which archive would you like to access? ' name
	varch "$name"
elif [[ $# -gt 0 ]]; then
	varch "$1"
fi

