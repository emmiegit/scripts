#!/bin/bash
set -eu

did_something=false

if [[ $# -eq 0 ]]; then
	readonly start_dir=.
else
	readonly start_dir="$1"
fi

relapath() {
	realpath --relative-to="$start_dir" -- "$1"
}

recursively_convert() {
	for file in "$1/"*; do
		if [[ -d $file ]]; then
			printf '[DIR] %s\n' "$(relapath "$file")"
			recursively_convert "$file"
		elif [[ $file == *.md ]]; then
			local target="${file%.*}.gen.pdf"

			if [[ ! -f $target ]] || [[ $file -nt $target ]]; then
				did_something=true
				printf '[PDF] %s\n' "$(relapath "$target")"
				pandoc -f markdown_github --latex-engine=xelatex -o "$target" -- "$file" || {
					printf 2>&1 'PDF conversion failed, falling back to HTML generation\n'
					target="${file%.*}.gen.html"
					printf '[HTML] %s\n' "$(relapath "$target")"
					markdown "$file" > "$target"
				}
			fi
		fi
	done
}

recursively_convert "$start_dir"
"$did_something" || printf 'Nothing to do.\n'

