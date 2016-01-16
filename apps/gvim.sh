#!/usr/bin/env bash

gvim() {
    if [[ $# -eq 0 ]]; then
        /usr/bin/gvim
    else
        ( /usr/bin/gvim --remote-tab-silent "$1" ||
          /usr/bin/gvim "$1" ) 2> /dev/null 
        shift
        [[ $# -gt 0 ]] && gvim $@
    fi
}

if [[ $1 == "--run" ]]; then
    shift
    gvim "$@"
fi

