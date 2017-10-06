#!/bin/sh
sudo rsync -vrtpAXlHogS --progress --safe-links --delete-after /media/archive /media/ExternalDisk
