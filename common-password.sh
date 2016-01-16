#!/bin/bash
# Licensed under the MIT License

PASSWORD_LIST="$(dirname $0)/dat/passwords.txt"

check_pwd() {
    read -sp "Enter your password: " userpwd
    echo

    [ -z $userpwd ] && exit

    found=false
    for cmnpwd in `cat $PASSWORD_LIST`; do
        if [ "$userpwd" == "$cmnpwd" ]; then
            printf "Your password was found on the list, change it immediately.\n"
            found=true
            break
        fi
    done

    if ! $found; then
        printf "Your password was not found on the list.\n"
    fi

    unset userpwd
}

echo "This utility checks your password against the list of the 10,000 most common passwords. If it is found on that list, it is extremely encouraged to change it to something secure."
echo "If you're concerned about this program stealing your password, please inspect the source code and make changes if you feel it necessary."
echo

while true; do
    check_pwd
done

