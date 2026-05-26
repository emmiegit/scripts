#!/bin/bash

# Updates all nvidia driver packages
#
# Since they don't appear together in sorted output
# but need to be built together

exec yay -Syu \
	nvidia-580xx-dkms
	nvidia-580xx-settings
	nvidia-580xx-utils
	lib32-nvidia-580xx-utils
	lib32-opencl-nvidia-580xx
	opencl-nvidia-580xx
	libxnvctrl-580xx
