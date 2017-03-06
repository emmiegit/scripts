#!/bin/bash
set -eu

# VPN constants
readonly ns_name='vpngate'
readonly addr0='10.200.200.0'
readonly addr1='10.200.200.1'
readonly addr2='10.200.200.2'
readonly subnet=24
readonly dev0='vpn0'
readonly dev1='vpn1'
readonly tun='vpntun0'
readonly iface_match='en+'
readonly vpn_pidfile="/run/vpnns-$ns_name.pid"

# Print constants
readonly underline="\e[4m"
readonly reset="\e[0m"

# Runtime
readonly args=("$@")

function msg() {
	if tty -s; then
		printf "${underline}%s${reset}\n" "$1"
	else
		echo "$1"
	fi
}

function getroot() {
	if [[ $UID != 0 ]]; then
		msg "This operation needs root privileges."
		_USER="$USER" exec sudo "$0" "${args[@]}"
	fi
}

function cmd_do() {
	echo "$@"
	"$@"
}

function cmd_bg() {
	echo "$@"
	"$@" &
}

function cmd_ns() {
	echo "ip netns exec $ns_name $@"
	ip netns exec "$ns_name" "$@"
}

function dowrite() {
	echo "echo $1 > $2"
	echo "$1" > "$2"
}

function iface_up() {
	if iface_status > /dev/null; then
		msg "Interface $ns_name is already up"
		return 1
	fi

	getroot
	cmd_do ip netns add "$ns_name"

    cmd_ns ip addr add '127.0.0.1/8' dev lo
    cmd_ns ip addr add '::1/128' dev lo
    cmd_ns ip link set lo up

	cmd_do ip link add "$dev1" type veth peer name "$dev0"
	cmd_do ip link set "$dev1" netns "$ns_name"

	cmd_do ip link set "$dev0" up
	cmd_ns ip link set "$dev1" up

	cmd_do ip addr add "$addr1/$subnet" dev "$dev0"
	cmd_ns ip addr add "$addr2/$subnet" dev "$dev1"
	cmd_ns ip route add default via "$addr1" dev "$dev1"

    cmd_do sysctl -q net.ipv4.ip_forward=1

	##
    cmd_do ip link add "$dev0" type veth peer name "$dev1"
    cmd_do ip link set "$dev0" up
    cmd_do ip link set "$dev1" netns "$ns_name" up

    cmd_do ip addr add "$addr1/$subnet" dev "$dev0"
    cmd_ns ip addr add "$addr2/$subnet" dev "$dev1"
    cmd_ns ip route add default via "$addr1" dev "$dev1"

    cmd_do iptables -A INPUT \! -i "$dev0" -s "$addr0/$subnet" -j DROP
    cmd_do iptables -t nat -A POSTROUTING -s "$addr0/$subnet" -o "$iface_match" -j MASQUERADE

    cmd_do mkdir -p "/etc/netns/$ns_name"
	dowrite "nameserver 8.8.8.8" "/etc/netns/$ns_name/resolv.conf"

	msg "Testing namespace..."
	cmd_ns ping -c 2 8.8.8.8
    cmd_ns ping -c 2 www.google.com
}

function iface_down() {
	if ! iface_status > /dev/null; then
		msg "Interface $ns_name is already down"
		return 1
	fi

	getroot
	cmd_do rm -rf "/etc/netns/$ns_name"

    cmd_do sysctl -q net.ipv4.ip_forward=0

    cmd_do iptables -D INPUT \! -i "$dev0" -s "$addr0/$subnet" -j DROP
    cmd_do iptables -t nat -D POSTROUTING -s "$addr0/$subnet" -o "$iface_match" -j MASQUERADE

    cmd_do ip netns delete "$ns_name"
}

function iface_status() {
	if ip netns | grep -q "$ns_name"; then
		msg "Interface $ns_name is UP"
	else
		msg "Interface $ns_name is DOWN"
		return 1
	fi
}

function ns_run() {
	getroot
	if [[ "${_USER:-root}" != "root" ]]; then
		cmd_ns sudo -u "$_USER" "$@"
	else
		cmd_ns "$@"
	fi
}

function vpn_up() {
	if [[ $# -eq 0 ]]; then
		msg "Usage: $0 vpn up openvpn-file"
		return 1
	fi

	if vpn_status > /dev/null; then
		msg "The VPN is already up"
		return 1
	fi

	local readonly config="$1"

	getroot
	cmd_bg ip netns exec "$ns_name" \
		openvpn \
			--cd "$(dirname "$config")" \
			--config "$config" \
			--dev "$tun" \
			--errors-to-stderr

    until ip netns exec "$ns_name" ip addr show dev "$tun" up; do
        sleep .3
    done

	dowrite "$!" "$vpn_pidfile"
	disown
}

function vpn_down() {
	if [[ ! -f "$vpn_pidfile" ]]; then
		msg "The instance isn't up"
		return 1
	fi

	if ! vpn_status > /dev/null; then
		msg "The VPN is already down"
		return 1
	fi

	readonly local pid="$(cat "$vpn_pidfile")"

	cmd_do kill "$pid"
	cmd_do rm -f "$vpn_pidfile"
}

function vpn_status() {
	if [[ ! -f "$vpn_pidfile" ]]; then
		msg "The OpenVPN tunnel is DOWN"
		return 1
	fi

	readonly local pid="$(cat "$vpn_pidfile")"

	if kill -0 "$pid"; then
		msg "The OpenVPN tunnel is UP"
	else
		msg "The OpenVPN tunnel is DEAD"
		rm -f "$vpn_pidfile"
		return 1
	fi
}

function usage_and_exit() {
	if "$1"; then
		msg "Invalid parameters."
	fi
	echo "Usage: $0 ns (up|down|status|exec) [arguments]"
	echo "Usage: $0 vpn (up|down|status) [arguments]"
	echo "Usage: $0 run [arguments]"
	echo "Usage: $0 help"
	exit 1
}

if [[ $# -eq 0 ]]; then
	usage_and_exit true
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
				usage_and_exit true
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
				usage_and_exit true
				;;
		esac
		;;
	run)
		shift
		ns_run "$@"
		;;
	help)
		usage_and_exit false
		;;
	*)
		usage_and_exit true
		;;
esac

