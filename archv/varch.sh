#!/bin/bash
set -euo pipefail

readonly dest="$HOME/Documents/Relic/Private"
readonly lock="$dest/.$1.lock"
readonly ext=7z
readonly hash_script='/usr/local/scripts/archv/media-hash.py'
readonly hash_only=false
readonly clear_recent=true
readonly test_archive=false
readonly remove_files=false
_remove_lock=true

on_sigterm() {
	printf 'Caught user interrupt, closing down.\n'
	if [[ -f $lock ]] && "$_remove_lock"; then
		rm -f "$lock"
	else
		printf 'Warning: can'\''t remove lock file.'
	fi
	exit 1
}

on_exit() {
	printf 'Finished.\n'
	if [[ -f $lock ]] && "$_remove_lock"; then
		rm -f "$lock"
	else
		printf 'Warning: can'\''t remove lock file.\n'
	fi
	exit 0
}

trap on_sigterm SIGTERM SIGINT
trap on_exit EXIT

# Lock check
if [[ -f $lock ]]; then
	printf >&2 'This script is already running.\n'
	_remove_lock=false
	read -r
	exit 1
fi

# Sanity tests
if [[ ! -d $dest ]]; then
	printf >&2 'Destination directory does not exist.\n'
	exit 1
fi

varch() {
	local archive="$1.$ext"
	cd "$dest"
	touch "$lock"

	if [[ -d $1 ]]; then
		printf '[Compressing]\n'
		if ! "$hash_only"; then
			read -rsp 'Password: ' password
		fi
		if [[ -f $archive ]]; then
			if ! 7z l -p"$password" "$archive" >/dev/null 2>&1; then
				printf >&2 'Invalid password or corrupt archive!\n'
				exit 1
			fi
		else
			printf 'Creating new archive\n'
		fi
		printf 'Hashing images...\n'
		"$hash_script" "$dest/$1"
		echo
		"$hash_only" && return
		printf 'Backing up old archive...\n'
		[[ -f $archive ]] && mv -u "$archive" "$archive~"
		printf 'Adding files to archive...\n'
		7z a -p"$password" -t7z -ms=on -mhe=on -m0=lzma -mx=3 "$archive" "$1"
		"$test_archive" && 7z t -p"$password" "$archive"
		if "$remove_files"; then
			printf 'Removing old files...\n'
			rm -rf "${1:?}"
		fi
		if "$clear_recent"; then
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
	elif [[ ! -f $archive ]]; then
		printf '[Error]\n'
		printf 'Cannot find archive at %s!\n' "$archive"
	else
		printf '[Extracting]\n'
		read -rsp 'Password: ' password
		7z x -p"$password" "$archive"
	fi
}

if [[ $# -eq 0 ]]; then
	read -rp 'Which archive would you like to access? ' name
	varch "$name"
elif [[ $# -gt 0 ]]; then
	varch "$1"
fi

