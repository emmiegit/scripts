#!/bin/bash
set -euo pipefail

verbose=false

# For pacman-based distros
kernel_name=linux
kernel_suffix=ARCH
running_kernel="$(uname -r)"
installed_kernel="$(pacman -Qi "$kernel_name" | grep '^Version' | awk '{print $3}')"
mod_installed_kernel="$(sed -e 's/\.arch/-arch/' <<< "$installed_kernel")"
full_installed_kernel="$mod_installed_kernel-$kernel_suffix"

for arg in "$@"; do
	case "$arg" in
		-v|--verbose)
			verbose=true
			;;
		-q|--quiet)
			printf() { :; }
			;;
	esac
done

if "$verbose"; then
	printf '$kernel_name:           "%s"\n' "$kernel_name"
	printf '$kernel_suffix:         "%s"\n' "$kernel_suffix"
	printf '$running_kernel:        "%s"\n' "$running_kernel"
	printf '$installed_kernel:      "%s"\n' "$installed_kernel"
	printf '$mod_installed_kernel:  "%s"\n' "$mod_installed_kernel"
	printf '$full_installed_kernel: "%s"\n' "$full_installed_kernel"
	echo
fi

if [[ "$running_kernel" == "$full_installed_kernel" ]]; then
	printf 'Your kernel (%s) is up-to-date.\n' "$running_kernel"
else
	printf 'Your running kernel (%s) is out-of-date!\n' "$running_kernel"
	printf 'The new kernel is %s.\n' "$full_installed_kernel"
	exit 1
fi
