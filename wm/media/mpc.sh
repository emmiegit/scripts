mpc() {
	local mpd_password="$(cat ~/Documents/Secure/files/mpd-passwd.txt)"
	env mpc -h "$mpd_password@localhost" "$@"
}
