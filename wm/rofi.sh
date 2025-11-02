#!/bin/sh
set -eu

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 [mode]" >&2
	exit 1
fi

case "$1" in
	emoji|unicode)
		exec rofimoji \
			--files \
				emoji \
				math \
				chess_symbols \
				currency_symbols \
				miscellaneous_symbols \
				latin-1_supplement \
				cjk_radicals_supplement \
				cjk_japanese_kun \
				cjk_japanese_on
		;;
	run|window)
		exec rofi -show combi -modi combi -combi-modes 'drun,window,run'
		;;
	*)
		echo "Unknown mode: $1" >&2
		;;
esac
