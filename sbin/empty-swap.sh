#!/bin/bash
set -e

printf 'Turning off...'
sudo swapoff -a
echo done

printf 'Turning on...'
sudo swapon -a
echo done
