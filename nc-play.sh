#!/bin/bash
set -eu

# Signal handling
trap exit EXIT SIGTERM SIGHUP SIGINT

# Function definitions
play() {
    mpv --no-video "$@"
}

play-nc() {
    mpv --no-video --speed=1.5 --audio-pitch-correction=no "$@"
}

play-ac() {
    mpv --no-video --speed=0.67 --audio-pitch-correction=no "$@"
}

play-random() {
	if [[ $((RANDOM % 2)) -eq 0 ]]; then
		FLAGS='--audio-pitch-correction=no'
	else
		FLAGS=
	fi

	mpv --no-video --speed="$(perl -e 'printf("%1.2f", rand() * 1.5)')" $FLAGS "$@"
}

get-song() {
	local index="$((RANDOM % ${#SONGS[@]}))"
	echo "${SONGS[index]}"
}

main() {
	while true; do
		local song="$(get-song)"

		if [[ $MASK -eq 0 ]]; then
			play-random "$song"
		else
			local sel="$((RANDOM % MASK))"

			case "$sel" in
				0)
					play "$song"
					;;
				1)
					play-nc "$song"
					;;
				2)
					play-ac "$song"
					;;
			esac
		fi
	done
}

SONGS=()
MASK=3

# Parse arguments
for arg in "$@"; do
	case "$arg" in
		-n)
			MASK=2
			;;
		--nightcore-only)
			MASK=2
			;;
		-s)
			MASK=0
			;;
		--random-speeds)
			MASK=0
			;;
		*)
			SONGS+=("$arg")
			;;
	esac
done

main

