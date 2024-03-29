#!/bin/bash
set -u

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
	local git_local
	local git_remote
	local git_base

	if [[ -z $(git remote 2>/dev/null) ]]; then
		echo -e "[${green}UP-TO-DATE${reset}]${changes} $repo\n"
		return
	fi

	"$fetch_repos" && git fetch

	git_local="$(git rev-parse 'HEAD' 2>/dev/null)"
	git_remote="$(git rev-parse '@{u}' 2>/dev/null)"
	git_base="$(git merge-base HEAD '@{u}' 2>/dev/null)"

	if [[ "$git_local" == "$git_remote" ]]; then
		echo -e "[${green}UP-TO-DATE${reset}]${changes} ${repo}"
	elif [[ "$git_local" == "$git_base" ]]; then
		echo -e "[${yellow}NEEDS PULL${reset}]${changes} ${repo}"
	elif [[ "$git_remote" == "$git_base" ]]; then
		echo -e "[${yellow}NEEDS PUSH${reset}]${changes} ${repo}"
		return 1
	else
		echo -e "[${bold_red}DIVERGED${reset}]${changes}   ${repo}"
		return 1
	fi
}

main() {
	local untracked=false
	local staged=false
	local return=0
	local lines=()
	local to_pull=()
	local git_status

	for dir in *; do
		[[ ! -d $dir ]] && continue
		cd "$dir"
		repo="${PWD##*/}"
		if [[ ! -d .git ]]; then
			lines+=("[NOT A REPO]  $repo")
			cd ..
			continue
		fi

		git_status="$(git status --porcelain)"
		if grep -q '^[^ ?]' <<< "$git_status"; then
			changes="${blue}!${reset}"
			staged=true
		elif grep -q '^ .' <<< "$git_status"; then
			changes="${red}!${reset}"
			untracked=true
		else
			changes=' '
		fi

		if lines+=("$(check_repo)"); then
			to_pull+=("$repo")
		else
			((return++))
		fi

		cd ..
	done

	"$untracked" && echo -e "'${red}!${reset}' means that untracked or unstaged files are present."
	"$staged" && echo -e "'${blue}!${reset}' means that changes have been staged but not commited."
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
for arg in "$@"; do
	if [[ $argno -eq $# && -d $arg ]]; then
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
