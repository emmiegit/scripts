#!/usr/bin/env bash

### FUNCTIONS ###
usage_and_exit() {
	printf >&2 'Usage: %s directory...\n' "$(basename $0)"
	exit 1
}

write_makefile() {
		cat << EOF > Makefile
# Note for OBJECTS: list all *.o files necessary for compilation in the
# given variable. They must be listed like this:
# OBJECTS=abc.cpp.o \\
#		def.cpp.o	\\
#		main.cpp.o
# You *must* use tabs in front of each object name, you must escape each line
# with a backslash, like shown.

.PHONY: all debug force direct distclean clean

CC=g++
FLAGS=-Wall -Werror
OBJECTS=main.cpp.o
EXE=main

all: \$(EXE)

%.cpp.o: %.cpp
	\$(CC) \$(FLAGS) \$(EXTRA_FLAGS) -c -o \$@ \$<

\$(EXE): \$(OBJECTS)
	\$(CC) \$(FLAGS) \$(EXTRA_FLAGS) -o \$(EXE) \$(OBJECTS)

debug: clean
	make \$(EXE) EXTRA_FLAGS=-g

force: clean \$(EXE)

direct: clean
	\$(CC) \$(FLAGS) *.cpp *.h -o \$(EXE)

distclean:
	rm -f *.o *~ \$(EXE) core core.*

clean:
	rm -f *.o core core.* vgcore.* \$(EXE)

EOF
}

new_project() {
	set -e
	echo "[NEW] $1"
	mkdir -p -- "$1"
	cd -- "$1"
	write_makefile
	cd ..
}

update_project() {
	if [[ ! -d $1 ]]; then
		new_project
		return $?
	fi

	set -e
	echo "[UPDATE] $dir"
	cd -- "$1"
	write_makefile
	cd ..
}

main() {
	for dir in $@; do
		if [[ -e $dir ]]; then
			if [[ -d $dir ]]; then
				update_project "$dir"
			else
				printf >&2 'Location exists and is not a directory: "%s".\n' "$dir"
			fi
		else
			new_project "$dir"
		fi
	done
}

### MAIN ###
[ $# -eq 0 ] && usage_and_exit
cd "$(dirname $0)"
[[ $1 == --help ]] && usage_and_exit
main $@

