#!/bin/bash
set -eux
set -o pipefail

readonly backup_dir="$(mktemp -d)/$(date +'%Y-%m-%d')"

mkdir "$backup_dir"
cd "$HOME/documents/games/minecraft-servers/$1"
echo "Backing up Minecraft server '$1'..."

rsync \
	-vrtpAXl \
	-zz \
	--safe-links \
	"$@" \
	"Adam:/usr/games/minecraft/$1/"{world,world_nether,world_the_end} \
	"$backup_dir"

7z a archive.7z "$backup_dir"
rm -rf "$backup_dir"
