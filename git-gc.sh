#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
	readonly dirlist=(.)
else
	readonly dirlist=("$@")
fi

readonly origdir="$(pwd)"
for dir in "${dirlist[@]}"; do
	for repo in "$dir"/*/; do
		if [[ ! -d "$repo/.git" ]]; then
			continue
		fi

		cd "$repo"
		echo "Entering $repo..."
		git fsck --full
		git gc --aggressive
		git prune --verbose
		cd "$origdir"
	done
done
