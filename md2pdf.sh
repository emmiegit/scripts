#!/bin/bash
set -euo pipefail

did_something=false

recursively_convert() {
	local changed=false

	for file in *; do
		"$changed" && printf '[DIR] %s\n' "$(basename "$(pwd)")"

		if [[ -d $file ]]; then
			cd "$file"
			recursively_convert
			cd ..
		elif [[ $file == *.md ]]; then
			local target="${file%.*}.pdf"

			if [[ ! -f $target ]] || [[ $file -nt $target ]]; then
				changed=true
				did_something=true
				printf '[MD] %s\n' "$file"
				pandoc -f markdown_github "$file" -o "$target"
				markdown "$file" > "$target"
			fi
		fi
	done
}

[[ $# -gt 0 ]] && cd "$1"
recursively_convert
"$did_something" || printf 'Nothing to do.\n'

