#!/bin/bash
set -eux

# Updates all nvidia driver packages
#
# Since they don't appear together in sorted output
# but need to be built together

if [[ ! -d $AURDEST/*/ ]]; then
	echo "Directories exist in $AURDEST"
	exit 1
fi

# List of packages
readonly packages=(
	nvidia-580xx-dkms
	nvidia-580xx-settings
	nvidia-580xx-utils
	lib32-nvidia-580xx-utils
	lib32-opencl-nvidia-580xx
	opencl-nvidia-580xx
	libxnvctrl-580xx
)

# Download packages
(
	cd "$AURDEST"
	for pkg in "${packages[@]}"; do
		git clone "https://aur.archlinux.org/$pkg.git"
	done
)

# Build each package
(
	cd "$AURDEST"
	for pkg in "${packages[@]}"; do
		[[ ! -d $pkg/.git ]] && continue
		makepkg
	done
)

# Install all the packages
sudo pacman -U "$AURDEST/**/*.pkg.tar
