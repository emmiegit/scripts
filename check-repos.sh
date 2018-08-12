#!/bin/bash
set -euo pipefail

readonly red="\e[31m\e[1m"
readonly green="\e[32m"
readonly reset="\e[0m"
source "$(dirname "$0")/dat/repos"

invalid=0

valid_git() {
	(
	cd "$1"
	if git status --porcelain > /dev/null; then
		return 0
	else
		return 1
	fi
	)
}

main() {
	for repo in "${repos[@]}" "$@"; do
		printf "%s: " "$repo"
		if [[ ! -d $repo ]]; then
			printf "${red}not found${reset}\n"
			((invalid++))
		elif [[ ! -d $repo/.git ]]; then
			printf "${red}not repo${reset}\n"
			((invalid++))
		elif ! valid_git "$repo"; then
			printf "${red}invalid${reset}\n"
			((invalid++))
		else
			printf "${green}ok${reset}\n"
		fi
	done
}

main
exit $invalid
