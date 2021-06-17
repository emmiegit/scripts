#!/usr/bin/env python3

import sys
from io import StringIO

MAX_MESSAGE_LEN = 2000

class StringBuilder:
    __slots__ = (
        "buffer",
        "length",
    )

    def __init__(self):
        self.buffer = StringIO()
        self.length = 0

    def append(self, s):
        self.length += self.buffer.write(s)

    def __len__(self):
        return self.length

    def __str__(self):
        return self.buffer.getvalue()

def split_message(text):
    parts = []
    part = StringBuilder()

    # Split by line, preserving newlines
    for line in text.splitlines(True):
        if len(part) + len(line) > MAX_MESSAGE_LEN:
            # This part is max size, move to the next one
            parts.append(str(part))
            part = StringBuilder()

        # Add new line to buffer
        part.append(line)

    # Finish up the final part
    parts.append(str(part))

    # Return parts
    return parts

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    parts = split_message(text)
    for i, part in enumerate(parts):
        print(part)

        if i < len(parts) - 1:
            print("[ --------- ]\n")
