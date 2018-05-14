#!/bin/sh
exec scrot "$HOME/Incoming/$(date +%s).png"
exec maim -u "$HOME/Incoming/$(date +%s).png"
