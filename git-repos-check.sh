#!/bin/bash

GREEN='\e[32m'
YELLOW='\e[33;1m'
BOLD_RED='\e[31;1m'
RED='\e[31m'
BLUE='\e[34m'
RESET='\e[0m'

PULL_REPOS=false

# Declare functions
help_and_exit() {
	echo 'Usage: %s [-p | --pull] [directory-to-check]\n' "$(basename "$0")"
	echo ' -p, --pull: Attempt to pull all up-to-date and behind repositories.\n'
	echo ' -h, --help: Print this help message and quit.\n'
	exit 0
}

check_repo() {
	if [[ -z $(git remote 2>/dev/null) ]]; then
		printf "[${GREEN}UP-TO-DATE${RESET}]${CHANGES} %s\n" "$REPO"
		return
	fi

	local LOCAL="$(git rev-parse @ 2>/dev/null)"
	local REMOTE="$(git rev-parse @{u} 2>/dev/null)"
	local BASE="$(git merge-base @ @{u} 2>/dev/null)"

	if [[ $LOCAL == $REMOTE ]]; then
		printf "[${GREEN}UP-TO-DATE${RESET}]${CHANGES} %s\n" "$REPO"
	elif [[ $LOCAL == $BASE ]]; then
		printf "[${YELLOW}NEEDS PULL${RESET}]${CHANGES} %s\n" "$REPO"
	elif [[ $REMOTE == $BASE ]]; then
		printf "[${YELLOW}NEEDS PUSH${RESET}]${CHANGES} %s\n" "$REPO"
		return 1
	else
		printf "[${BOLD_RED}DIVERGED${RESET}]${CHANGES}   %s\n" "$REPO"
		return 1
	fi
}

main() {
	local UNTRACKED=false
	local TO_COMMIT=false
	local RET=0
	local lines=()
	local to_pull=()

	for dir in *; do
		[[ ! -d $dir ]] && continue
		cd "$dir"
		REPO="$(basename "$(pwd)")"
		if [[ ! -d .git ]]; then
			lines+=("[NOT A REPO]  $REPO")
			cd ..
			continue
		fi

		local status="$(git status --porcelain)"
		if echo "$status" | grep -q '^[^ ?]'; then
			CHANGES="${BLUE}!${RESET}"
			TO_COMMIT=true
		elif echo "$status" | grep -q '^ .'; then
			CHANGES="${RED}!${RESET}"
			UNTRACKED=true
		else
			CHANGES=' '
		fi

		lines+=("$(check_repo)")
		if [ $? -gt 0 ]; then
			((RET++))
		else
			to_pull+=("$REPO")
		fi

		cd ..
	done

	$UNTRACKED && printf "'${RED}!${RESET}' means that untracked or unstaged files are present.\n"
	$TO_COMMIT && printf "'${BLUE}!${RESET}' means that changes have been staged but not commited.\n"
	printf "%s\n" "${lines[@]}"

	if $PULL_REPOS && [ ${#to_pull[@]} -gt 0 ]; then
		for repo in "${to_pull[@]}"; do
			cd "$repo"
			printf 'Pulling %s...\n' "$repo"
			git pull
			git submodule update --recursive
			cd ..
		done
	fi

	return $RET
}

# Process arguments
argno=1
for arg in $@; do
	if [ $argno -eq $# -a -d "$arg" ]; then
		cd "$arg"
		break
	fi

	case "$arg" in
		-p) PULL_REPOS=true ;;
		--pull) PULL_REPOS=true ;;
		-h) help_and_exit ;;
		--help) help_and_exit ;;
		*)
			printf 'Unknown argument: %s. See --help for help.\n' "$arg"
			exit 1
			;;
	esac
	((argno++))
done

# Run program
main

