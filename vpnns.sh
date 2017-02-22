#!/bin/bash
set -eu

readonly ns_name='vpngate'
readonly addr0='10.200.200.0'
readonly addr1='10.200.200.1'
readonly addr2='10.200.200.2'
readonly dev0='vpn0'
readonly dev1='vpn1'
readonly subnet=24
readonly vpn_pidfile="/run/vpnns-$ns_name.pid"

function getroot() {
	if [[ $EUID != 0 ]]; then
		echo >&2 "This script needs root privileges."
		exec sudo "$0" "$@"
		exit 1
	fi
}

function docmd() {
	echo "$@"
	"$@"
}

function bgcmd() {
	echo "$@"
	"$@" &
}

function iface_up() {
	getroot
	docmd ip netns add "$ns_name"

    docmd ip netns exec "$ns_name" ip addr add 127.0.0.1/8 dev lo
    docmd ip netns exec "$ns_name" ip link set lo up

    docmd ip link add "$dev0" type veth peer name "$dev1"
    docmd ip link set "$dev0" up
    docmd ip link set "$dev1" netns "$ns_name" up

    docmd ip addr add "$addr1/$subnet" dev "$dev0"
    docmd ip netns exec "$ns_name" ip addr add "$addr2/$subnet" dev "$dev1"
    docmd ip netns exec "$ns_name" ip route add default via "$addr1" dev "$dev1"

    docmd iptables -A INPUT \! -i "$dev0" -s "$addr0/$subnet" -j DROP
    docmd iptables -t nat -A POSTROUTING -s "$addr0/$subnet" -o wl+ -j MASQUERADE

    docmd sysctl -q net.ipv4.ip_forward=1

    docmd mkdir -p "/etc/netns/$ns_name"
	docmd cp /etc/resolv.conf "/etc/netns/$ns_name/resolv.conf"

    docmd ip netns exec "$ns_name" fping -q www.google.com
}

function iface_down() {
	getroot
	docmd rm -rf "/etc/netns/$ns_name"

    docmd sysctl -q net.ipv4.ip_forward=0

    docmd iptables -D INPUT \! -i "$dev0" -s "$addr0/$subnet" -j DROP
    docmd iptables -t nat -D POSTROUTING -s "$addr0/$subnet" -o wl+ -j MASQUERADE

    docmd ip netns delete "$ns_name"
}

function iface_status() {
	if ip netns | grep "$ns_name"; then
		echo "Interface $ns_name is UP"
	else
		echo "Interface $ns_name is DOWN"
		return 1
	fi
}

function ns_run() {
	docmd exec ip netns exec "$ns_name" "$@"
}

function vpn_up() {
	if [[ $# -eq 0 ]]; then
		echo "Usage: $0 vpn up openvpn-file"
		return 1
	fi

	getroot
	bgcmd ip netns exec "$ns_name" openvpn --config "$1"

    while ! ip netns exec "$ns_name" ip a show dev tun0 up; do
        sleep .3
    done

	echo "$!" > "$vpn_pidfile"
	disown
}

function vpn_down() {
	if [[ ! -f "$vpn_pidfile" ]]; then
		echo "The instance isn't up"
		return 1
	fi

	readonly local pid="$(cat "$vpn_pidfile")"

	docmd kill "$pid"
	docmd rm -f "$vpn_pidfile"
}

function vpn_status() {
	if [[ ! -f "$vpn_pidfile" ]]; then
		echo "The OpenVPN instance is DOWN"
		return 1
	fi

	readonly local pid="$(cat "$vpn_pidfile")"

	if kill -0 "$pid"; then
		echo "The OpenVPN instance is UP"
	else
		echo "The OpenVPN instance is DEAD"
		rm -f "$vpn_pidfile"
		return 1
	fi
}

function usage_and_exit() {
	echo "Usage: $0 ns (up|down|status|exec) [arguments]"
	echo "Usage: $0 vpn (up|down|status) [arguments]"
	echo "Usage: $0 run [arguments]"
	exit 1
}

if [[ $# -lt 2 ]]; then
	usage_and_exit
fi

case "$1" in
	ns)
		case "$2" in
			up)
				iface_up
				;;
			down)
				iface_down
				;;
			status)
				iface_status
				;;
			exec)
				shift
				ns_run "$@"
				;;
			*)
				usage_and_exit
				;;
		esac
		;;
	vpn)
		case "$2" in
			up)
				vpn_up
				;;
			down)
				vpn_down
				;;
			status)
				vpn_status
				;;
			*)
				usage_and_exit
				;;
		esac
		;;
	run)
		shift
		ns_run "$@"
		;;
	*)
		usage_and_exit
		;;
esac

