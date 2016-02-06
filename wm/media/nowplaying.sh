#!/bin/sh

main() {
    case "$(~/Scripts/wm/detect-audio-player.sh)" in
        mocp)
            mocp -Q '%song by %artist'
            ;;
        pianobar)
            local fn="${HOME}/.config/pianobar/nowplaying"
            if [ ! -f "$fn" ]; then
                echo '(error)'
            else
                local artist=$(grep -Po "(?<=^artist=).*" "$fn")
                local title=$(grep -Po "(?<=^title=).*" "$fn")
                echo "$title by $artist"
            fi
            ;;
        *)
            echo '(none)'
            ;;
    esac
}

main

