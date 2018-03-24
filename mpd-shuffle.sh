#!/bin/bash
set -eu

source "${0%/*}/wm/media/mpc.sh"

if [[ $# -gt 0 ]] && [[ $1 -gt 0 ]]; then
	readonly songs="$1"
else
	readonly songs=1
fi

dir="$HOME/Music"
prefix_len="${#dir}"

i=0
while IFS= read -r -d '' file; do
	if [[ $i -ge $songs ]]; then
		break;
	fi

	if ! mpc add "${file:$((prefix_len + 1))}"; then
		continue
	fi
	printf 'Added "%s".\n' "$(basename "$file")"

	i=$((i + 1))
done < <(find -L "$dir" -type f -name '*.*' -and -not -iname 'albumart.*' -print0 | shuf -z)

[[ $i -eq $songs ]]

