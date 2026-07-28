#!/bin/bash

# Updates all nvidia driver packages
#
# Since they don't appear together in sorted output
# but need to be built together

# TODO figure out how to best implement this
#      since saying "just install these packages"
#      in a row doesn't actually work...
#
#      perhaps cloning and doing makepkg on the relevant
#      base packages then installing the *.pkg.tar files?

echo yay -Sy \
	nvidia-580xx-dkms
	nvidia-580xx-settings
	nvidia-580xx-utils
	lib32-nvidia-580xx-utils
	lib32-opencl-nvidia-580xx
	opencl-nvidia-580xx
	libxnvctrl-580xx
