#!/bin/sh

packages="$(checkupdates | wc -l)"

case "$packages" in
	0) echo "Up-to-date" ;;
	1) echo "1 package" ;;
	*) echo "$packages packages" ;;
esac

