#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/games/wine/plants-vs-zombies'
export WINEHOME="$WINEPREFIX"

cd "$WINEPREFIX/drive_c/games/Pogo Games/Plants Vs Zombies Game of the Year Edition"

if [[ -n $KILL ]]; then
	wineserver -k
elif [[ -n $VERBOSE ]]; then
	wine 'PlantsVsZombies.ifn' &
else
	wine 'PlantsVsZombies.ifn' \
		< /dev/null \
		> /dev/null \
		2> /dev/null \
		&
	disown
fi
