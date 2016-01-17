#!/bin/sh
set -e

encfs /media/archive/Backup/Nexus\ One.crypt          /media/archive/Backup/Nexus\ One
encfs /media/archive/Backup/Nexus\ Five.crypt         /media/archive/Backup/Nexus\ Five
encfs /media/archive/Backup/Novus\ USB.crypt          /media/archive/Backup/Novus\ USB
encfs /media/archive/Backup/Tomboy\ Notes.crypt       /media/archive/Backup/Tomboy\ Notes

rclone sync /media/archive/Backup/Titus               Amazon\ Backup:/Live/Titus
rclone sync /media/archive/Backup/Archive\ Disk       Amazon\ Backup:/Live/Archive
rclone sync /media/archive/Backup/Nexus One.crypt     Amazon\ Backup:/Live/NexusOne
rclone sync /media/archive/Backup/Nexus Five.crypt    Amazon\ Backup:/Live/NexusFive
rclone sync /media/archive/Backup/Novus USB.crypt     Amazon\ Backup:/Live/NovusUSB
rclone sync /media/archive/Backup/Tomboy\ Notes.crypt Amazon\ Backup:/Live/TomboyNotes

