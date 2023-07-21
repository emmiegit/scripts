#!/usr/bin/env python3

# See https://changaco.oy.lc/unicode-progress-bars/

from datetime import datetime

try:
    import pyperclip
    CLIPBOARD = True
except ImportError:
    CLIPBOARD = False

BAR_LEVELS = "░▒▓█"
BAR_SIZE = 12

START_DAY = datetime(2023, 6, 9)
FULL_CORRUPTION = 2 * 365


def make_bar(percent):
    result = [None] * BAR_SIZE
    piece_cost = 1 / BAR_SIZE
    piece_choices = len(BAR_LEVELS) - 1
    nudge = 0.0001  # Avoids rounding-down issues at 100%

    for i in range(BAR_SIZE):
        piece = min(percent, piece_cost)
        piece_weight = piece / piece_cost
        bar_index = int(piece_weight * piece_choices + nudge)
        result[i] = BAR_LEVELS[bar_index]
        percent -= piece

    return "".join(result)


def copy_to_clipboard(text):
    if CLIPBOARD:
        pyperclip.copy(text)
        print("Copied to clipboard!")


if __name__ == "__main__":
    days_since = (datetime.now() - START_DAY).days
    percent = days_since / FULL_CORRUPTION  # between 0 and 1
    bar = make_bar(percent)
    output = f"Corruption progress: {bar} {percent * 100:.1f}%"
    print(output)
    copy_to_clipboard(output)
