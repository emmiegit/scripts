#!/usr/bin/env python3
import codecs
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
    Edit all: E S
    Help:     ?
    Quit:     q
"""

NEXT = (ord('n'), ord('l'), ord('j'), ord(' '), curses.KEY_ENTER, curses.KEY_DOWN, curses.KEY_RIGHT)
PREV = (ord('p'), ord('h'), ord('k'), curses.KEY_UP, curses.KEY_LEFT)
FIRST = (ord('g'), ord('0'), ord('^'), curses.KEY_HOME)
LAST = (ord('G'), ord('$'), curses.KEY_END)
RANDOM = (ord('r'),)
EDIT = (ord('e'), ord('s'))
EDIT_ALL = (ord('E'), ord('S'))
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

def get_blocks(fh, filename, fileno):
    blocks = []
    lines = []

    def append_block():
        content = '\n'.join(lines)
        blocks.append(Block(content, filename, fileno))

    for line in fh.readlines():
        line = line.rstrip()
        if line == '%':
            append_block()
            lines = []
        else:
            lines.append(line)
    append_block()

    return filter(None, blocks)

def get_all_blocks(files):
    blocks = []
    for i, filename in enumerate(files):
        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as fh:
            blocks += get_blocks(fh, filename, i + 1)

    if not blocks:
        if len(files) == 1:
            print("File is empty.")
        else:
            print("Files are empty.")
        exit(0)

    return blocks

class Block:
    __slots__ = (
        'content',
        'filename',
        'fileno',
    )

    def __init__(self, content, filename, fileno):
        self.content = content
        self.filename = filename
        self.fileno = fileno

    def __bool__(self):
        return bool(self.content)

class BlockDisplay:
    __slots__ = (
        'files',
        'blocks',
        'blockno',
    )

    def __init__(self, blocks, files):
        self.files = files
        self.blockno = 0
        self.blocks = blocks

    def run(self, win):
        curses.cbreak()
        curses.nonl()
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

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
            elif ch in EDIT_ALL:
                self.edit_all(win)
            elif ch in HELP:
                self.print_help(win)
            elif ch in QUIT:
                return 0

    def edit(self, win):
        curses.def_prog_mode()
        curses.endwin()
        block = self.blocks[self.blockno]
        run_editor([block.filename])
        self.blocks = get_all_blocks(self.files)
        if self.blockno >= len(self.blocks):
            self.blockno = 0
        curses.reset_prog_mode()
        self.redraw(win)

    def edit_all(self, win):
        curses.def_prog_mode()
        curses.endwin()
        run_editor(self.files)
        self.blockno = 0
        self.blocks = get_all_blocks(self.files)
        curses.reset_prog_mode()
        self.redraw(win)

    def redraw(self, win):
        win.erase()

        if self.blockno >= len(self.blocks):
            self.blockno = 0

        block = self.blocks[self.blockno]
        info1 = "File {} of {}".format(block.fileno, len(self.files))
        info2 = "Block {} of {}".format(self.blockno + 1, len(self.blocks))

        win.attron(curses.A_BOLD)
        win.addstr(0, 0, block.filename)
        win.attroff(curses.A_BOLD)
        win.addstr(1, 0, info1)
        win.addstr(2, 0, info2)
        win.addstr("\n\n")

        try:
            win.addstr(block.content)
            win.addstr("\n")
        except curses.error:
            y, x = win.getyx()
            win.move(y, 0)
            win.clrtoeol()
            win.addstr(' TEXT TOO LONG', curses.A_BOLD | curses.color_pair(1))

        win.refresh()

    def print_help(self, win):
        win.erase()
        win.addstr(0, 0, HEADER)
        win.addstr(HELP_STRING)
        win.refresh()
        _ = win.getch()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s filename..." % sys.argv[0], file=sys.stderr)
        exit(1)

    files = sys.argv[1:]
    blocks = get_all_blocks(files)
    display = BlockDisplay(blocks, files)
    curses.wrapper(display.run)

