#!/usr/bin/env python3

import pyperclip

ZERO_WIDTH_SPACE = "​"

if __name__ == "__main__":
    pyperclip.copy(ZERO_WIDTH_SPACE)
    print("Copied to clipboard!")
