#!/bin/bash

backup="/media/archive/backup/titus/borg"

export BORG_PASSPHRASE="$(pass show computer/titus/borg-raw)"
