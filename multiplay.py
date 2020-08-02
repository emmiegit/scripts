#!/usr/bin/env python3

# This is for playing multiple audio streams at the same time.
# Video is not presently implemented.
#
# See https://superuser.com/a/1325668 for more information.

import subprocess
import sys

def execute(file_args, mpv_args):
    args = ['mpv']
    args.extend(mpv_args)
    args.extend(file_args)
    ret = subprocess.call(args)
    sys.exit(ret)

def single_play(mpv_args, file):
    args = [file]
    execute(args, mpv_args)

def double_play(mpv_args, file0, file1):
    args = [
        '--lavfi-complex=[aid1][aid2]amix[ao]',
        file0,
        f'--external-file={file1}',
    ]
    execute(args, mpv_args)

def multi_play(mpv_args, files):
    # build the lavfi-complex argument
    lavfi = ['--lavfi-complex=']
    for i in range(len(files)):
        lavfi.append(f'[aid{i+1}]')
    lavfi.append(f'amix=inputs={len(files)}[ao]')

    args = [''.join(lavfi)]
    del lavfi

    # add the audio files
    args.append(files[0])
    for file in files[1:]:
        args.append(f'--external-file={file}')

    # run
    execute(args, mpv_args)

if __name__ == '__main__':
    mpv_args = []
    files = []

    # Gather arguments
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            mpv_args.append(arg)
        else:
            files.append(arg)

    # Use the correct mpv invocation
    if len(files) == 1:
        single_play(mpv_args, files[0])
    elif len(files) == 2:
        double_play(mpv_args, files[0], files[1])
    else:
        multi_play(mpv_args, files)
