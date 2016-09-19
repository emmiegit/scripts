#!/bin/bash
set -e

CONFIRM=false
RECURSIVE=false

confirmation() {
	if $CONFIRM; then
		read -p "Are you sure you want to do this? [y/N] " response
		case $response in
			yes) return 0 ;;
			y) return 0 ;;
			Y) return 0 ;;
			*) return 1 ;;
		esac
	else
		return 0
	fi
}

movefile() {
	while true; do
		printf '%s [%s]: ' "$1" "$(identify -format '%[fx:w]x%[fx:h]' "$1" 2> /dev/null || printf 'error')"
		read dest
		if [[ -z $dest ]] || [ "$dest" == "." ]; then
			return
		elif [[ $dest == '!' ]]; then
			confirmation && trash "$1" && return
		elif [[ $dest == '!!' ]]; then
			confirmation && rm "$1" && return
		elif [[ $dest == '!!!' ]]; then
			confirmation && shred -u "$1" && return
		elif [[ $dest == '*' ]]; then
			tree -ld
		elif [[ $dest == '+' ]]; then
			read -p "What should the new directory be called? " dest
			mkdir "$dest"
		elif [[ $dest == +* ]]; then
			mkdir "${dest:1}"
		elif [[ $dest == '_' ]]; then
			xdg-open .
		elif [[ -d $dest ]]; then
			mv "$1" "$dest" && return
		else
			echo "That's not a valid directory."
		fi
	done
}

organize() {
	prev=$(pwd)
	cd "$1"
	for fn in *; do
		if [[ -d $fn ]] && $RECURSIVE; then
			echo "Recursively organizing $fn..."
			organize "$fn"
		elif file "$fn" | grep -q 'image'; then
			feh -g 960x600 "$fn" 2> /dev/null &
			movefile "$fn"
			kill $! ||:
		else
			echo "Skipping $fn..."
		fi
	done

	cd "$prev"
}

if [[ $# -eq 0 ]]; then
	echo "Usage: $(basename $0) directory-to-organize..."
	exit 1
fi

echo 'For each picture, enter the directory it should be moved to.'
echo 'Note that you can specify any directory, such as abc/def or /tmp/pictures.'
echo 'Specifying nothing, or . will keep the image where it is.'
echo 'In addition, there some other special commands you can specify:'
echo ' !   - Trash the current image. (This assumes you have a binary called "trash" on your $PATH)'
echo ' !!  - Delete the current image.'
echo ' !!! - Shreds and deletes the current image.'
echo ' *   - List all directories in the current working directory.'
echo ' +   - Create a directory. You can specify the name directly by using "+dir_name".'
echo ' _   - Open the current directory in your file explorer of choice.'
echo ''

while [[ $# -gt 0 ]]; do
	organize "$1"
	shift
done

