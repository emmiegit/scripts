#!/bin/bash
set -eu

usage_and_exit() {
	printf >&2 "Usage: %s [-c] [-I header-file] [-D define[=value]] c-type...\n" "$0"
	printf >&2 "    -c               Compile in the current directory.\n"
	printf >&2 "    -I <file>        Include this file in the C source.\n"
	printf >&2 "    -D <key>=<val>   Include this definition in the C source.\n"
	exit 1
}

[[ $# -eq 0 ]] && usage_and_exit

# Variables
c_compiler=cc
includes=()
defines=()
use_temp=true

# Parse arguments
while getopts ':cI:D:?' opt; do
	case "$opt" in
		c)
			use_temp=false
			;;
		I)
			includes+=("$OPTARG")
			;;
		D)
			defines+=("$OPTARG")
			;;
		:)
			printf >&2 "Option %s requires an argument\n". "$OPTARG"
			usage_and_exit
			;;
		\?)
			printf >&2 "Invalid argument: '-%s'\n" "$OPTARG"
			usage_and_exit
			;;
	esac
done
shift "$((OPTIND - 1))"

# Create temp files
if "$use_temp"; then
	c_file="$(mktemp ${TEMP_DIR:-/tmp}/XXXXXXX.c)"
	c_binary="$(mktemp ${TEMP_DIR:-/tmp}/XXXXXXX)"
else
	c_file="$(mktemp XXXXXXX.c)"
	c_binary="$(mktemp XXXXXXX)"
fi

# Remove temp files on exit
on_exit() {
	rm -f "$c_file" "$c_binary"
}
 
trap on_exit EXIT SIGABRT SIGINT SIGHUP SIGTERM

[[ $# -eq 0 ]] && usage_and_exit

for type in "$@"; do
	cat > "$c_file" <<- EOF
	#include <stdio.h>

	EOF

	for include in "${includes[@]}"; do
		cat >> "$c_file" <<- EOF
		#include "$include"
		EOF
	done
	echo >> "$c_file"

	for define in "${defines[@]}"; do
		key="$(cut -d= -f1 <<< "$define")"
		val="$(cut -d= -f2 <<< "$define")"

		cat >> "$c_file" <<- EOF
		#define $key $val
		EOF
	done
	echo >> "$c_file"

	cat >> "$c_file" <<- EOF
	int main(void)
	{
		printf("sizeof($type) -> %lu\n", (unsigned long)sizeof($type));
		return 0;
	}

	EOF

	"$c_compiler" -o "$c_binary" "$c_file" 2>/dev/null \
		&& "$c_binary" \
		|| printf >&2 "sizeof(%s) -> unknown\n" "$type"
done

