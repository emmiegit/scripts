#!/bin/bash
set -eu

packages="$(pacman -Qu | wc -l)"
arch_linux_icon='' # siji font

case "$packages" in
	0) echo ;;
	*) echo "$arch_linux_icon $packages" ;;
esac
