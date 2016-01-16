#!/usr/bin/env bash

rclone sync /media/archive/Backup/Titus              Amazon\ Backup:/Live/Titus
rclone sync /media/archive/Backup/Archive\ Disk      Amazon\ Backup:/Live/Archive
rclone sync /media/archive/Backup/Nexus One.crypt    Amazon\ Backup:/Live/NexusOne
rclone sync /media/archive/Backup/Nexus Five.crypt   Amazon\ Backup:/Live/NexusFive
rclone sync /media/archive/Backup/Novus USB.crypt    Amazon\ Backup:/Live/NovusUSB
rclone sync /media/archive/Backup/Tombo\ Notes.crypt Amazon\ Backup:/Live/TomboyNotes

