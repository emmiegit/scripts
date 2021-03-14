#!/usr/bin/env python3

"""
A command-line implementation of snowflake_time() from discord.py

This copies the code here to avoid importing a very large library for
a small utility function.
"""

import sys
from datetime import datetime


DISCORD_EPOCH = 1420070400000


def snowflake_time(id):
    return datetime.utcfromtimestamp(((id >> 22) + DISCORD_EPOCH) / 1000)


def timedelta_string(timedelta):
    parts = []

    offset_name = "ago" if timedelta.days >= 0 else "from now"
    timedelta = abs(timedelta)

    years, days = divmod(timedelta.days, 365)
    months, days = divmod(days, 30)
    weeks, days = divmod(days, 7)
    hours, seconds = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    seconds += timedelta.microseconds / 1e6
    seconds = round(seconds, 2)

    if years:
        parts.append((years, "year"))
    if months:
        parts.append((months, "month"))
    if weeks:
        parts.append((weeks, "week"))
    if days:
        parts.append((days, "day"))
    if hours:
        parts.append((hours, "hour"))
    if minutes:
        parts.append((minutes, "minute"))
    if seconds:
        parts.append((seconds, "second"))

    delta_string = ", ".join(
        f"{amount} {unit}" if amount == 1 else f"{amount} {unit}s"
        for (amount, unit) in parts
    )

    return delta_string, offset_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} ID...")
        sys.exit(1)

    for arg in sys.argv[1:]:
        try:
            id = int(arg)
        except ValueError:
            print(f"{arg} - Not an integer")
            continue

        timestamp = snowflake_time(id)
        elapsed = datetime.utcnow() - timestamp
        delta_string, offset_name = timedelta_string(elapsed)

        print(f"{id} - {timestamp} ({delta_string} {offset_name})")
