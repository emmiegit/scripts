#!/bin/sh
# SSD health checker for the Samsung 850 EVO. Be sure to research your particular
# model to look for the correct attribute name, and obviously the right device too.
DEVICE='/dev/sdc'

get_health() {
    sudo smartctl -a "$DEVICE" | grep 'Wear_Leveling_Count' | awk '{print $4}'
}

echo "Life remaining for $DEVICE: $(get_health | perl -pe 'chomp')%"

