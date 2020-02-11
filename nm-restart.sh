#!/bin/bash
set -eu

nmcli con down "$1"
nmcli con up "$1"
