#!/usr/bin/env python
from __future__ import print_function, with_statement
import curses
import os
import random
import subprocess
import sys

# TODO:
# - Wrap words
# - Allow scrolling for large blocks
# - Add search
# - Command-line options
# - Support ctrl+z backgrounding

HEADER = """\
psplit v0.1
Copyright (C) 2016 Ammon Smith
Licensed under the GPL, version 2 or later.
"""

HELP_STRING = """
Keybinds:
    Next:     n j l <down> <space> <enter> <right>
    Previous: p k h <up> <left>
    First:    g 0 ^ <home>
    Last:     G $ <end>
    Random:   r
    Edit:     e s
    Help:     ?
    Quit:     q
"""

NEXT = (ord('n'), ord('l'), ord('j'), ord(' '), curses.KEY_ENTER, curses.KEY_DOWN, curses.KEY_RIGHT)
PREV = (ord('p'), ord('h'), ord('k'), curses.KEY_UP, curses.KEY_LEFT)
FIRST = (ord('g'), ord('0'), ord('^'), curses.KEY_HOME)
LAST = (ord('G'), ord('$'), curses.KEY_END)
RANDOM = (ord('r'),)
EDIT = (ord('e'), ord('s'))
HELP = (ord('?'), ord('H'))
QUIT = (ord('q'),)

def plural(number):
    if number == 1:
        return ''
    else:
        return 's'

def run_editor(arguments):
    try:
        editor = os.environ['VISUAL']
    except KeyError:
        try:
            editor = os.environ['EDITOR']
        except KeyError:
            editor = 'vi'

    subprocess.call([editor] + arguments)

def get_blocks(fh):
    blocks = []
    lines = []
    for line in fh.readlines():
        line = line.rstrip()
        if line == '%':
            blocks.append('\n'.join(lines))
            lines = []
        else:
            lines.append(line)
    blocks.append('\n'.join(lines))

    if len(blocks) == 1 and not blocks[0]:
        return []
    else:
        return blocks

def get_all_blocks(files):
    blocks = []
    for filename in files:
        with open(filename, 'r') as fh:
            blocks += get_blocks(fh)

    if not blocks:
        if len(files) == 1:
            print("File is empty.")
        else:
            print("Files are empty.")
        exit(0)

    return blocks

class BlockDisplay(object):
    def __init__(self, blocks, files):
        self.files = files
        self.blockno = 0
        self.blocks = blocks

    def run(self, win):
        curses.cbreak()
        curses.nonl()
        curses.noecho()

        while True:
            self.redraw(win)

            ch = win.getch()
            if ch in NEXT:
                self.blockno = min(self.blockno + 1, len(self.blocks) - 1)
            elif ch in PREV:
                self.blockno = max(self.blockno - 1, 0)
            elif ch in FIRST:
                self.blockno = 0
            elif ch in LAST:
                self.blockno = len(self.blocks) - 1
            elif ch in RANDOM:
                self.blockno = random.randint(0, len(self.blocks) - 1)
            elif ch in EDIT:
                self.edit(win)
            elif ch in HELP:
                self.print_help(win)
            elif ch in QUIT:
                return 0

    def edit(self, win):
        curses.def_prog_mode()
        curses.endwin()
        run_editor(self.files)
        self.blocks = get_all_blocks(self.files)
        curses.reset_prog_mode()
        self.redraw(win)

    def redraw(self, win):
        win.erase()

        if self.blockno >= len(self.blocks):
            self.blockno = 0

        info = "Block %d of %d (%d file%s)" % \
            (self.blockno + 1, len(self.blocks), len(self.files), plural(len(self.files)))
        block = self.blocks[self.blockno]

        win.addstr(0, 0, info)
        win.addstr("\n\n")
        win.addstr(block)
        win.addstr("\n")

        win.refresh()

    def print_help(self, win):
        win.erase()
        win.addstr(0, 0, HEADER)
        win.addstr(HELP_STRING)
        win.refresh()

        ch = win.getch()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s filename..." % sys.argv[0], file=sys.stderr)
        exit(1)

    files = sys.argv[1:]
    blocks = get_all_blocks(files)
    display = BlockDisplay(blocks, files)
    curses.wrapper(display.run)

