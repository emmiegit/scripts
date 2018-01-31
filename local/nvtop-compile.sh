#!/bin/bash
set -eu

# For compiling nvtop without CMake
# (CentOS 7)

cd /tmp
git clone https://github.com/Syllo/nvtop
cd nvtop

sudo yum install -y \
	ncurses-devel \
	cuda-nvml-dev-9-1

flags=(
	'-pipe'
	'-O2'
	'-march=native'
	'-mtune=generic'
	'-fstack-protector-strong'
)

for src in src/*.c; do
	obj="${src%?}o"
		gcc \
			"${flags[@]}" \
			-std=gnu11 \
			-Iinclude \
			-isystem /usr/local/cuda-9.1/targets/x86_64-linux/include \
			-c -o "$obj" \
			"$src"
done

# Linking
gcc \
	"${flags[@]}" \
	-Wl,-O1,--sort-common,--as-needed,-z,relo,-z,now \
	-rdynamic \
	-L/usr/lib64/nvidia \
	-o nvtop \
	src/*.o

echo 'Final binary is "nvtop"'
