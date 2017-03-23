#!/bin/bash
set -euo pipefail

did_something=false

recursively_convert() {
	for file in *; do
		if [[ -d $file ]]; then
			cd "$file"
			recursively_convert
			cd ..
		elif [[ $file == *.md ]]; then
			local target="${file%.*}.pdf"

			if [[ ! -f $target ]] || [[ $file -nt $target ]]; then
				did_something=true
				printf '[MD] %s\n' "$target"
				pandoc -f markdown_github --latex-engine=xelatex -o "$target" -- "$file"
				markdown "$file" > "$target"
			fi
		fi
	done
}

[[ $# -gt 0 ]] && cd "$1"
recursively_convert
"$did_something" || printf 'Nothing to do.\n'

