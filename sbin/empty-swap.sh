#!/bin/bash
set -e

printf 'Turning off...'
swapoff -a
echo done

printf 'Turning on...'
swapon -a
echo done
