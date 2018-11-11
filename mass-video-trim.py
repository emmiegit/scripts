#!/usr/bin/python3

import re
import os
import sys
import subprocess

DURATION_REGEX = re.compile(r'Duration: ([0-9]+):([0-9]+):([0-9\.]+),')

SECONDS_TO_TRIM = 10 # time to remove from end
THIS_PROGRAM = os.path.basename(sys.argv[0])
OUTPUT_DIR = 'out'

def recursive_trim(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            trim(os.path.join(dirpath, filename))

def trim(filename):
    if os.path.basename(filename) in (THIS_PROGRAM, OUTPUT_DIR):
        return

    print(filename, end=' ')

    output_file = os.path.join(OUTPUT_DIR, filename)
    if os.path.isfile(output_file):
        print('skipping')
        return

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    try:
        output = subprocess.check_output(['ffprobe', filename], stderr=subprocess.STDOUT, encoding='UTF-8')
    except subprocess.CalledProcessError:
        print('error')
        return

    matches = DURATION_REGEX.findall(output)
    if not matches:
        raise ValueError(f"No duration outputted for '{file}'")

    match = matches[0]
    hours = int(match[0])
    minutes = int(match[1]) + 60 * hours
    seconds = float(match[2]) + 60 * minutes
    seconds_end = seconds - SECONDS_TO_TRIM
    print(f'to {seconds_end}')

    subprocess.check_call([
        'ffmpeg',
        '-i', filename,
        '-c', 'copy',
        '-to', str(seconds_end),
        output_file,
    ])

if __name__ == '__main__':
    if len(sys.argv) > 2:
        directory = sys.argv[1]
    else:
        directory = '.'

    recursive_trim(directory)
