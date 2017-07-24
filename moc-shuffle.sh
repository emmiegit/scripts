#!/bin/bash
set -eu

if [[ $# -gt 0 ]] && [[ $1 -gt 0 ]]; then
	readonly songs="$1"
else
	readonly songs=1
fi

i=0
while IFS= read -r -d '' file; do
	if [[ $i -ge $songs ]]; then
		break;
	fi

	if ! mocp -a "$file"; then
		continue
	fi
	printf 'Added "%s".\n' "$(basename "$file")"

	i=$[i + 1]
done < <(find -L "$HOME/Music" -type f -name '*.*' -and -not -iname 'albumart.*' -print0 | shuf -z)

[[ $i -eq $songs ]]

