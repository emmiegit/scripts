#!/usr/bin/env bash
# Licensed under the MIT License

PASSWORD_LIST="$(dirname "$0")/dat/passwords.txt"

check_pwd() {
	read -rsp 'Enter your password: ' userpwd
	echo

	[[ -z $userpwd ]] && exit

	while read -r cmnpwd; do
		if [[ "$userpwd" == "$cmnpwd" ]]; then
			printf 'Your password was found on the list, change it immediately.\n'
			return 1
		fi
	done < "$PASSWORD_LIST"

	printf 'Your password was not found on the list.\n'

	unset userpwd
}

echo 'This utility checks your password against the list of the 10,000 most common passwords. If it is found on that list, it is extremely encouraged to change it to something secure.'
echo 'If you'\''re concerned about this program stealing your password, please inspect the source code and make changes if you feel it necessary.'
echo

while true; do
	check_pwd
done

