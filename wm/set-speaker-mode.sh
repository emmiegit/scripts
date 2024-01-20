#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
	printf >&2 'Usage: %s (headphones | tv)\n' "${0##*/}"
	exit 1
fi

mode="$1"
quiet=false
analog_sink='alsa_output.pci-0000_12_00.3.analog-stereo' # unused, former headphone_sink
headphones_sink='alsa_output.usb-Focusrite_Scarlett_Solo_USB_Y799H6922E91A3-00.HiFi__hw_USB__sink'
television_sink='alsa_output.pci-0000_0b_00.1.hdmi-stereo'

shift
for arg in "$@"; do
	case "$arg" in
		-q)
			quiet=true
			;;
		--quiet)
			quiet=true
			;;
		*)
			printf >&2 'Unknown argument: %s.\n' "$arg"
			exit 1
	esac
done

function notify() {
	if [[ $# -gt 0 ]] && ! "$quiet"; then
		notify-send "$@"
	fi
}

function set_sink() {
	pactl set-default-sink "$1"
}

case "$mode" in
	headphones|hp)
		notify 'Setting computer to headphone mode.'
		set_sink "$headphones_sink"
		;;
	television|tv)
		notify 'Setting computer to television mode.'
		set_sink "$television_sink"
		;;
	*)
		printf >&2 'Unknown speaker setting: %s.\n' "$mode"
		exit 1
esac
