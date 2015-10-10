#!/usr/bin/env bash
sudo -k
echo "This program will empty all your RAM disk cache."
echo "Clearing disk cache will NOT speed up performance and is just a placebo."
sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches' || echo "Caught user interrupt."
sudo -k
printf "Finished. "
read

