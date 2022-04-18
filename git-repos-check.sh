#!/bin/bash
set -eu

readonly green='\e[32m'
readonly yellow='\e[33;1m'
readonly bold_red='\e[31;1m'
readonly red='\e[31m'
readonly blue='\e[34m'
readonly reset='\e[0m'

fetch_repos=false
pull_repos=false

# Declare functions
help_and_exit() {
	echo "Usage: ${0##*/} [-f | --fetch] [-p | --pull] [directory-to-check]"
	echo ' -p, --pull: Attempt to pull all up-to-date and behind repositories.'
	echo ' -h, --help: Print this help message and quit.'
	exit 0
}

check_repo() {
	if [[ -z $(git remote 2>/dev/null) ]]; then
		echo "[${green}UP-TO-DATE${reset}]${changes} %s\n" "$repo"
		return
	fi

	"$fetch_repos" && git fetch

	local local="$(git rev-parse HEAD 2>/dev/null)"
	local remote="$(git rev-parse @{u} 2>/dev/null)"
	local base="$(git merge-base HEAD @{u} 2>/dev/null)"

	if [[ $local == $remote ]]; then
		echo "[${green}UP-TO-DATE${reset}]${changes} ${repo}"
	elif [[ $local == $base ]]; then
		echo "[${yellow}NEEDS PULL${reset}]${changes} ${repo}"
	elif [[ $remote == $base ]]; then
		echo "[${yellow}NEEDS PUSH${reset}]${changes} ${repo}"
		return 1
	else
		echo "[${bold_red}DIVERGED${reset}]${changes}   ${repo}"
		return 1
	fi
}

main() {
	local untracked=false
	local to_commit=false
	local return=0
	local lines=()
	local to_pull=()

	for dir in *; do
		[[ ! -d $dir ]] && continue
		cd "$dir"
		repo="$(basename "$(pwd)")"
		if [[ ! -d .git ]]; then
			lines+=("[NOT A REPO]  $repo")
			cd ..
			continue
		fi

		local status="$(git status --porcelain)"
		if echo "$status" | grep -q '^[^ ?]'; then
			changes="${blue}!${reset}"
			to_commit=true
		elif echo "$status" | grep -q '^ .'; then
			changes="${red}!${reset}"
			untracked=true
		else
			changes=' '
		fi

		lines+=("$(check_repo)")
		if [[ $? -gt 0 ]]; then
			((return++))
		else
			to_pull+=("$repo")
		fi

		cd ..
	done

	"$untracked" && echo "'${red}!${reset}' means that untracked or unstaged files are present."
	"$to_commit" && echo "'${blue}!${reset}' means that changes have been staged but not commited."
	printf "%s\n" "${lines[@]}"

	if "$pull_repos" && [[ ${#to_pull[@]} -gt 0 ]]; then
		for repo in "${to_pull[@]}"; do
			cd "$repo"
			echo "Pulling $repo..."
			git pull
			git submodule update --recursive
			cd ..
		done
	fi

	return "$return"
}

# Process arguments
argno=1
for arg in $@; do
	if [[ $argno -eq $# -a -d $arg ]]; then
		cd "$arg"
		break
	fi

	case "$arg" in
		-F|--fetch) fetch_repos=true ;;
		-p|--pull) pull_repos=true ;;
		-h|--help) help_and_exit ;;
		*)
			echo "Unknown argument: $arg" >&2
			echo "See --help for help" >&2
			exit 1
			;;
	esac
	((argno++))
done

# Run program
main
