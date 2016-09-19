#!/bin/bash
set -eu

# For pacman-based distros
KERNEL_NAME=linux
KERNEL_SUFFIX=ARCH
RUNNING_KERNEL="$(uname -r)"
INSTALLED_KERNEL="$(pacman -Qi "$KERNEL_NAME" | grep '^Version' | awk '{print $3}')"

for arg in "$@"; do
	case "$arg" in
		-q)
			printf() { :; }
			;;
		--quiet)
			printf() { :; }
			;;
	esac
done

if [[ "$RUNNING_KERNEL" == "$INSTALLED_KERNEL-$KERNEL_SUFFIX" ]]; then
	printf 'Your kernel (%s) is up-to-date.\n' "$RUNNING_KERNEL"
else
	printf 'Your running kernel (%s) is out-of-date!\n' "$RUNNING_KERNEL"
	printf 'The new kernel is %s.\n' "$INSTALLED_KERNEL"
	exit 1
fi

