#!/usr/bin/env python

import math
from typing import Sequence

ADDRESSES = [
    0x000000000062c010,
    0x0000000004060000,
    0x0000000008761610,
    0x00000000106bdcd8,
    0x000000001febdcd8,
    0x000000002de88a40,
    0x0000000040160000,
    0x000000006ecbd4e0,
    0x000000007a4bdcd8,
    0x000000007b7e9788,
    0x00000000906bd4e0,
    0x00000000fa4bd4e0,
    0x00000000fb7e8f90,
    0x0000000106600000,
    0x0000000200020000,
    0x0000000241083100,
    0x00000006d98c0020,
    0x0000000801620000,
    0x0000000d08100000,
    0x0000000f80110000,
    (0x000000002b964dd8, 0x000000002b968da8),
]

KB = 1024
MB = 1024 * KB
GB = 1024 * MB


def region_size(size: int) -> str:
    if size >= GB:
        div = GB
        unit = "G"
    elif size >= MB:
        div = MB
        unit = "M"
    else:
        div = KB
        unit = "K"

    mult = math.ceil(size / div)

    if unit == "K" and mult < 4:
        mult = 4

    return f"{mult}{unit}"


def build_memmap(addresses: Sequence[int | tuple[int, int]] = ADDRESSES) -> str:
    regions = []
    for address in addresses:
        match address:
            case (start, end):
                regions.append((start, region_size(end - start)))
            case address:
                regions.append((address, "4K"))

    sep = r"\\\$"
    parts = ",".join(f"{size}{sep}0x{address:016x}" for address, size in regions)
    return f"memmap={parts}"

if __name__ == "__main__":
    print(build_memmap())
