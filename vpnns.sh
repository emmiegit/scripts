#!/usr/bin/env zsh
set -eux

readonly ns_name='vpngate'
readonly addr0='10.200.200.0'
readonly addr1='10.200.200.1'
readonly addr2='10.200.200.2'
readonly subnet=24

if [[ $EUID != 0 ]]; then
	echo >&2 "This script needs root privileges."
	exec sudo "$0" "$@"
	exit 1
fi

function iface_up() {
    ip netns add "$ns_name"

    ip netns exec "$ns_name" ip addr add 127.0.0.1/8 dev lo
    ip netns exec "$ns_name" ip link set lo up

    ip link add vpn0 type veth peer name vpn1
    ip link set vpn0 up
    ip link set vpn1 netns "$ns_name" up

    ip addr add "$addr1/$subnet" dev vpn0
    ip netns exec "$ns_name" ip addr add "$addr2/$subnet" dev vpn1
    ip netns exec "$ns_name" ip route add default via "$addr1" dev vpn1

    iptables -A INPUT \! -i vpn0 -s "$addr0/$subnet" -j DROP
    iptables -t nat -A POSTROUTING -s "$addr0/$subnet" -o wl+ -j MASQUERADE

    sysctl -q net.ipv4.ip_forward=1

    mkdir -p "/etc/netns/$ns_name"
	cp /etc/resolv.conf "/etc/netns/$ns_name/resolv.conf"

    ip netns exec "$ns_name" fping -q www.google.com
}

function iface_down() {
    rm -rf "/etc/netns/$ns_name"

    sysctl -q net.ipv4.ip_forward=0

    iptables -D INPUT \! -i vpn0 -s "$addr0/$subnet" -j DROP
    iptables -t nat -D POSTROUTING -s "$addr0/$subnet" -o wl+ -j MASQUERADE

    ip netns delete "$ns_name"
}

function run() {
    exec sudo ip netns exec "$ns_name" "$@"
}

function start_vpn() {
	if [[ $# -eq 0 ]]; then
		echo >&2 "Usage: $0 openvpn-file"
	fi

    sudo ip netns exec "$ns_name" openvpn --config "$1" &

    while ! sudo ip netns exec "$ns_name" ip a show dev tun0 up; do
        sleep .3
    done
	disown
}

case "$1" in
    up)
        iface_up
		;;
    down)
        iface_down
		;;
    run)
		shift
        run "$@"
		;;
    start_vpn)
        start_vpn "$1"
		;;
    *)
        echo "Syntax: $0 up|down|status|run|start_vpn|stop_vpn"
        exit 1
        ;;
esac

