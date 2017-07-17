#!/bin/bash
set -euo pipefail

source "$(dirname "$0")/dat/repos"

background=true
fsck=false
gc=false

while getopts 'fcg' opt; do
	case "$opt" in
		f)
			background=false
			;;
		c)
			fsck=true
			;;
		g)
			gc=true
			;;
		\?)
			echo >&2 "Usage: $0 [-f] [-c] [-g] extra-repos..."
			exit 1
			;;
	esac
done
shift $((OPTIND - 1))

fsck() {
	if ! "$fsck"; then
		return 0
	fi

	git fsck --full || true
}

gc() {
	if ! "$gc"; then
		return 0
	fi

	git gc || true
}

main() {
	for repo in "${repos[@]}" "$@"; do
		echo "$repo"
		(
		cd "$repo"
		git pull || true
		git submodule update || true
		fsck
		gc
		)
	done
}

if "$background"; then
	echo 'Running in background.'
	main </dev/null >/dev/null 2>&1 &
	disown
else
	main
fi

