#!/bin/bash
set -euo pipefail

cd "$HOME/documents/games/minecraft-servers/$1"
echo "Backing up Minecraft server '$1'..."

readonly backup_dir="_backups/$(date +'%Y-%m-%d')"
mkdir -p "$backup_dir"
cp -an world world_nether world_the_end "$backup_dir"
