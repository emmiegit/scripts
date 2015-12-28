#!/bin/sh
# Detects if the logitech-g710-linux-driver has detected
# the keyboard and has exposed it's lower-level functions
# via and interface in /sys/bus/hid/devices.

# Main function definition
find_g710() {
    local found=false

    for dir in /sys/bus/hid/devices/0003:046D:C24D.*; do
        if [ -L $dir ]; then
            cd "$dir"
            
            if [ -d logitech-g710 ]; then
                if $PATH_ONLY; then
                    printf "%s" "$dir"
                else
                    printf "Found logitech-g710 interface directory in %s.\n" "$dir"
                fi

                found=true
            elif $VERBOSE; then
                printf "Checked %s, interface not found.\n" "$dir"
            fi
        fi
    done

    if ! $found; then
        $PATH_ONLY || printf "Logitech G710 driver interface not found.\n"
        return 1
    fi
}

# Give basic usage information
help_and_exit() {
    printf "Usage: %s [options]\n" "$(basename 0)"
    printf "-p, --pathonly    Only print the interface directory if found. Implies --quiet.\n"
    printf "-q, --quiet       Don't be verbose. (default)\n"
    printf "-v, --verbose     Be verbose when searching for the interface.\n"
    printf "-h, --help        Where you are now.\n"
    exit 0
}

# Default settings
PATH_ONLY=false
VERBOSE=false

# Parse arguments
while [ "$#" -gt "0" ]; do
    case "$1" in
        -p)         PATH_ONLY=true; VERBOSE=false ;;
        --pathonly) PATH_ONLY=true; VERBOSE=false ;;
        -v)         VERBOSE=true ;;
        --verbose)  VERBOSE=true ;;
        -q)         VERBOSE=false ;;
        --quiet)    VERBOSE=false ;;
        -h)         help_and_exit ;;
        --help)     help_and_exit ;;
        *)
            printf "Unknown argument: \"%s\".\n" "$1"
            printf "Try using \"--help\".\n"
            exit 1
            ;;
    esac
    shift
done

# Main function invocation
find_g710

