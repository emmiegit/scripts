#!/bin/bash

exit_with_usage() {
	echo "Usage: $(basename $0) [options] post-number"
	exit 1
}

exit_with_help() {
	echo "Usage: $(basename $0) [options] post-number"
	echo "Available options:"
	echo " -h --help   Print this help message and exit."
	echo " -q --quiet  Only return an exit code, don't output anything."
	exit 0
}

[ $# -eq 0 ] && exit_with_usage
[ "$1" == "-h" ] || [ "$1" == "--help" ] && exit_with_help

outputs=true

while [ $# -gt 1 ]; do
	case $1 in
		-h) exit_with_help ;;
	--help) exit_with_help ;;
		-q) outputs=false ;;
   --quiet) outputs=false ;;
	esac
	shift
done

echo $1 | egrep -q '^[0-9]+$' || exit_with_usage

check_pattern() {
	[[ $1 -lt $3 ]] && return 1
	return $((($1 % $2) % $3 != 0))
}

is_dubs()	{ return $(check_pattern $1 100		 11); }
is_trips()	{ return $(check_pattern $1 1000	 111); }
is_quads()	{ return $(check_pattern $1 10000	 1111); }
is_quints() { return $(check_pattern $1 100000	 11111); }
is_hexas()	{ return $(check_pattern $1 1000000  111111); }
is_septs()	{ return $(check_pattern $1 10000000 1111111); }

if $outputs; then
	if is_septs $1; then
		echo "SEPTS TONGUE MY ANUS!!!"
	elif is_hexas $1; then
		echo "HEXXXXXA!!"
	elif is_quints $1; then
		echo "HOLY SHIT QUINTS GET!"
	elif is_quads $1; then
		echo "QUADS GET!"
	elif is_trips $1; then
		echo "Nice trips."
	elif is_dubs $1; then
		echo "Checked."
	elif is_dubs $(($1+1)) || is_dubs $(($1-1)); then
		echo "Off by one. ;-;"
	else
		echo "Nice try fag."
	fi
fi

exit $(is_dubs $1)

