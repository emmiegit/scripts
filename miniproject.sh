#!/usr/bin/env bash

### FUNCTIONS ###
usage_and_exit() {
    printf >&2 'Usage: %s action [directory]\n' "$(basename $0)"
    printf >&2 'Actions: cc, clean, new, run\n'
    exit 1
}

compile() {
    local ret=0
    for dir in $@; do
        if [[ ! -d $dir ]]; then
            printf >&2 'Directory %s does not exist, cannot compile.\n' "$dir"
            continue
        fi

        cd "$dir"
        for fn in *.cpp; do
            [[ ! -f $fn ]] && [[ $fn != *.cpp ]] && continue
            echo "[CC] $fn"
            g++ -Wall -Werror -o "${fn:0:-4}" "$fn"
            ((ret += $?))
        done
        cd ..
    done
    return $ret
}

clean() {
    local ret=0
    for dir in $@; do
        if [[ ! -d $dir ]]; then
            printf >&2 'Directory %s does not exist, cannot clean.\n' "$dir"
            continue
        fi

        cd "$dir"
        for fn in *; do
            if [[ -f $fn.cpp ]] && [[ -x $fn ]]; then
                echo "[RM] $fn"
                rm -- "$fn"
                ((ret += $?))
            fi
        done
        cd ..
    done
    return $ret
}

new() {
    local ret=0
    for dir in $@; do
        if [[ -e $dir ]]; then
            printf >&2 'Path at %s already exists, cannot create directory.\n' "$dir"
            continue
        fi

        echo "[NEW] $dir"
        mkdir -p -- "$dir"
        cd "$dir"
        cat << EOF > compile.sh
#!/bin/sh
../$(basename $0) cc '$dir'
EOF
        ((ret += $?))
        cat << EOF > clean.sh
#!/bin/sh
../$(basename $0) clean '$dir'
EOF
        ((ret += $?))
        chmod +x *.sh
        ((ret += $?))
        cd ..
    done
    return $ret
}

run() {
    local ret=0
    for dir in $@; do
        local exe=main
        if [[ ! -d $dir ]]; then
            printf >&2 'Directory %s does not exist, cannot run.\n' "$dir"
            continue
        elif [[ ! -f "$dir/$exe" ]]; then
            printf >&2 'Executable %s not found in %s, cannot run.\n' "$exe" "$dir"
            continue
        elif [[ ! -x "$dir/$exe" ]]; then
            printf >&2 'File %s in %s does not have executable bit set.\n' "$exe" "$dir"
            continue
        fi

        echo "[RUN] $dir"
        "$dir/$exe"
        ((ret += $?))
    done
    return $ret
}

### MAIN ###
[ $# -eq 0 ] && usage_and_exit
cd "$(dirname $0)"
case "$1" in
    cc)
        shift
        if [[ -z $@ ]]; then
            compile *
        else
            compile $@
        fi
        ;;
    clean)
        shift
        if [[ -z $@ ]]; then
            clean *
        else
            clean $@
        fi
        ;;
    new)
        shift
        if [[ -z $@ ]]; then
            new *
        else
            new $@
        fi
        ;;
    *)
        printf >&2 'Unknown action: %s.\n' "$1"
        usage_and_exit
        ;;
esac

