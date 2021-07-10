#!/bin/bash
set -eu

case "$#" in
	0)
		echo >&2 "Usage: $0 [output-directory] input-file..."
		exit 1
		;;
	1)
		inputs=("$1")
		output=''
		;;
	*)
		output="$1"
		shift

		inputs=("$@")
		;;
esac


# See https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not

if [[ -n $output ]]; then
	libreoffice --headless --convert-to pdf "${inputs[@]}" --outdir "$output"
else
	libreoffice --headless --convert-to pdf "${inputs[@]}"
fi
