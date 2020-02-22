#!/bin/bash
set -eux
set -o pipefail

cd "$HOME/documents/games/minecraft-servers/$1/backups"
echo "Backing up Minecraft server '$1'..."

readonly backup_dir="$(date +'%Y-%m-%d')"
mkdir -p "$backup_dir"
cp -an world world_nether world_the_end "$backup_dir"
7z a archive.7z "$backup_dir"
rm -rf "$backup_dir"
