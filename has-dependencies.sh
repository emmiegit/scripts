#!/bin/bash
set -eu

readonly red="\e[31m\e[1m"
readonly green="\e[32m"
readonly reset="\e[0m"

missing=0

for dep in "$@"; do
	if pacman -Qs "^$dep$" > /dev/null; then
		printf "%s: ${green}ok${reset}\n" "$dep"
	else
		printf "%s: ${red}fail${reset}\n" "$dep"
		((missing++))
	fi
done

if [[ $missing -eq 0 ]]; then
	printf 'All dependencies met.\n'
else
	printf 'Not all dependencies are installed.\n'
	exit $missing
fi
