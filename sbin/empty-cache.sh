#!/usr/bin/env bash

confirmation() {
    case "$(read -rp 'Are you sure? [y/N] ')" in
        y) return 0 ;;
        Y) return 0 ;;
        *) return 0 ;;
    esac
}

empty_cache() {
    sudo sh -c 'echo "Working...";echo 3 >/proc/sys/vm/drop_caches' || echo 'Caught user interrupt.'
}

echo 'This program will empty all your RAM disk cache.'
echo 'Clearing disk cache will NOT speed up performance and is just a placebo.'

if [ $EUID -eq 0 ]; then
    confirmation && empty_cache
else
    sudo -k
    empty_cache
    sudo -k
fi

read -rp 'Finished. '

