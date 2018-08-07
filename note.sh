#!/usr/bin/bash
set -euo pipefail

if [[ ${NOTES_DIR:-x} == x ]]; then
	NOTES_DIR="$HOME/documents/notes"
fi

if [[ ${VISUAL:-x} == x ]]; then
	VISUAL="${EDITOR:-vi}"
fi

readonly argcount="$#"

check_args() {
	if [[ $argcount -ne $1 ]]; then
		usage_and_exit
	fi
}

usage() {
	echo "Usage:"
	echo "    ${0##*/} list"
	echo "    ${0##*/} edit <note>"
	echo "    ${0##*/} new <note>"
	echo "    ${0##*/} show|view <note>"
	echo "    ${0##*/} del|delete|rm|remove <note>..."
	echo "    ${0##*/} commit"
	echo "    ${0##*/} git <command>"
}

usage_and_exit() {
	usage
	exit 1
}

list_files() {
	local files=()

	for filename in *.txt; do
		files+=("${filename%.*}")
	done

	tr ' ' '\n' <<< "${files[@]}" | column -x
}

cd "$NOTES_DIR"
[[ $# -eq 0 ]] && usage_and_exit

case "$1" in
	help)
		usage
		;;
	list)
		check_args 1
		list_files
		;;
	edit)
		check_args 2
		"$VISUAL" "$2.txt"
		;;
	new)
		check_args 2
		if [[ -f "$2.txt" ]]; then
			echo "Note '$2' already exists!"
			exit 1
		else
			"$VISUAL" "$2"
		fi
		;;
	show|view)
		check_args 2
		cat "$2.txt"
		;;
	del|delete|rm|remove)
		shift
		rm "$@"
		;;
	commit)
		git add .
		git commit
		;;
	git)
		shift
		git "$@"
		;;
	*)
		usage_and_exit
		;;
esac
