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

get-song() {
	local index="$((RANDOM % ${#SONGS[@]}))"
	echo "${SONGS[index]}"
}

main() {
    while true; do
		local song="$(get-song)"
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
	done
}

# Parse arguments and run
SONGS=("$@")
MASK=3
main

