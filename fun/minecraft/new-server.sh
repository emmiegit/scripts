#!/bin/bash

DEFAULT_JAR='1.8.8'
MAKE_BACKUPS='false'

usage_and_exit() {
	printf >&2 'Usage: %s directory-name [jar-version] [make-backups]\n' "$(basename $0)"
	return 1
}

make_server() {
	if [[ ! -f "bin/$2.jar" ]]; then
		printf >&2 'Cannot find Minecraft server jar for version %s.\n' "$2"
		return 1
	elif [ "$3" != 'true' -a "$3" != 'false' ]; then
		printf >&2 'Argument "make-backups" must be either "true" or "false", not %s.\n' "$3"
		return 1
	fi

	cd "$(dirname $0)"
	mkdir "$1"
	cd "$1"
	ln -s ../bin/$2.jar minecraft_server.jar
	ln -s ../bin/start.sh .
	ln -s ../bin/clean.sh .
	echo "$3" > make_backups
	cat > eula.txt <<- EOF
	# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://acount.mojang.com/documents/minecraft_eula).
	eula=true
	EOF
	cd ..
}

case $# in
	0) usage_and_exit ;;
	1) make_server "$1" "$DEFAULT_JAR" "$MAKE_BACKUPS" ;;
	2) make_server "$1" "$2" "$MAKE_BACKUPS" ;;
	3) make_server "$1" "$2" "$3" ;;
	*) usage_and_exit ;;
esac

