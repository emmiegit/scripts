#!/bin/bash
set -eu

XMODMAP_FILE='/usr/local/scripts/dat/xmodmap-vi-keyswap'
FORCE=false
RESET=false

help_and_exit() {
	printf 'Usage: %s [-f] [-mXMODMAP_FILE]\n' "$(basename "$0")"
	printf 'Usage: %s --help\n\n'              "$(basename "$0")"
	printf '  -f, --force\n'
	printf '  	Run xmodmap, even if it appears that the keyswap is already set.\n'
	printf '  -r, --reset\n'
	printf '  	Reset to original keyboard layout.\n'
	printf '  -m[FILE], --modmapfile=[FILE]\n'
	printf '  	Specify the file to use to pass to "xmodmap". The default is to use "%s".\n' "$XMODMAP_FILE"
	exit 0
}

set_xmodmap_file() {
	case "$1" in
		-m*)
			local file="${1:2}"
			;;
		--modmapfile=*)
			local file="${1:13}"
			;;
		*)
			printf >&2 'Option in incorrect format: %s\n' "$1"
			return 1
			;;
	esac

	if [[ ! -e $file ]]; then
		printf >&2 'Cannot find xmodmap file "%s".\n' "$file"
		return 1
	else
		XMODMAP_FILE="$file"
	fi
}

keyswap() {
	if [[ -z $DISPLAY ]]; then
		printf >&2 '$DISPLAY is not set, is X running?\n'
		return 1
	else
		if "$FORCE" || xmodmap | grep -q 'Caps_Lock (0x42)'; then
			xmodmap "$XMODMAP_FILE"
		fi
	fi
}

for arg in "$@"; do
	case "$arg" in
		-f)             FORCE=true ;;
		--force)        FORCE=true ;;
		-r)             RESET=true ;;
		--reset)        RESET=true ;;
		-h)             help_and_exit ;;
		--help)         help_and_exit ;;
		-m*)            set_xmodmap_file "$arg" ;;
		--modmapfile=*) set_xmodmap_file "$arg" ;;
		*)
			printf >&2 'Unrecognized option: %s\nUse "--help" for a list of options.\n' "$arg"
			exit 1
			;;
	esac
done

if "$RESET"; then
	setxkbmap -layout us
else
	keyswap
fi
