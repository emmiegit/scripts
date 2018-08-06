mpc() {
	local mpd_password="$(cat ~/documents/secure/files/mpd-passwd.txt)"
	env mpc -h "$mpd_password@localhost" "$@"
}
