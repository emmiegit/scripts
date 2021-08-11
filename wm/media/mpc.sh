mpc() {
	local mpd_password="$(cat "$HOME/.mpd/password")"
	env mpc -h "$mpd_password@localhost" "$@"
}
