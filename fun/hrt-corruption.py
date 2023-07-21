#!/usr/bin/env python3

# See https://changaco.oy.lc/unicode-progress-bars/

from datetime import datetime

BAR_LEVELS =  "░▒▓█"
BAR_SIZE = 12

START_DAY = datetime(2023, 6, 9)
FULL_CORRUPTION = 2 * 365

def make_bar(percent):
    result = [None] * BAR_SIZE
    piece_cost = BAR_SIZE / FULL_CORRUPTION
    piece_choices = len(BAR_LEVELS) - 1

    for i in range(BAR_SIZE):
        piece = min(percent, piece_cost)
        piece_weight = piece / piece_cost
        bar_index = int(piece_weight * piece_choices)
        result[i] = BAR_LEVELS[bar_index]
        percent -= piece

    return "".join(result)

if __name__ == "__main__":
    days_since = (datetime.now() - START_DAY).days
    percent = days_since / FULL_CORRUPTION  # between 0 and 1
    bar = make_bar(percent)
    print(f"{bar} {percent * 100:.1f}% corrupted")

