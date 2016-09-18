#!/bin/sh

OSU_DIRECTORY='/opt/osu/game'
OSU_FILES=('collection.db' "osu\!.${USER}.cfg" 'osu!.cfg' 'osu!.db' 'presence.db' 'scores.db')
BACKUP_DIRECTORY='/media/archive/Games/osu!/bak'

cd "$OSU_DIRECTORY"
for fn in "${OSU_FILES[@]}"; do
	cp -fv "$fn" -t "$BACKUP_DIRECTORY"
done

