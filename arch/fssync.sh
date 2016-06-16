#!/bin/bash

# fssync - Two-way rsync
fssync() {
	case $# in
	3)
		rsync $1 "$2" "$3" &&
		rsync $1 "$3" "$2" ;;
	2)
		rsync -avhl "$1" "$2" &&
		rsync -avhl "$2" "$1" ;;
	*)
		echo "Usage: fssync [options] first-directory second-directory"
		return 1
	esac
	
	printf "Finished synchronizing $1 and $2.\n\n"
}

fssync_nolink() {
	case $# in
	3)
		rsync $1 "$2" "$3" &&
		rsync $1 "$3" "$2" ;;
	2)
		rsync -avh --no-links "$1" "$2" &&
		rsync -avh --no-links "$2" "$1" ;;
	*)
		echo "Usage: fssync [options] first-directory second-directory"
		return 1
	esac
	
	printf "Finished synchronizing $1 and $2.\n\n"
}

