#!/bin/bash

strip_exif() {
    local prev=$(pwd)

    cd "$1"
    for fn in *; do
        if [[ -d $fn ]]; then
            strip_exif "$fn"
        elif [[ $fn == *.jpg ]] || [[ $fn == *.jpeg ]]; then
            out="tmp-$RANDOM.jpg"
            osize=$(stat -c%s "$fn")
            jpegtran -copy none "$fn" > "$out"
            nsize=$(stat -c%s "$out")
            mv "$out" "$fn"
            
            [[ $osize -ne $nsize ]] && echo "Removed EXIF data from $fn."
        fi
    done
    cd "$prev"
}

if [[ -d $1 ]]; then
    strip_exif "$1"
fi

