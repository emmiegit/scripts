#!/usr/bin/env python

import math
from typing import Sequence

BADRAM = [
    (0x0000000000600000, 0xfffffff890e40800),
    (0x0000000000868000, 0xffffffff30878000),
    (0x0000000040000000, 0xfffffff8d1198090),
    (0x0000000050040000, 0xfffffff874658000),
    (0x0000000106600010, 0xfffffff307f78010),
    (0x0000000800600000, 0xfffffffc00f4c418),
    (0x0000000801e28000, 0xfffffffe13f28000),
    (0x0000000996684088, 0xffffffffffffc6b8),
    (0x0000000d08100000, 0xfffffffd88740000),
    (0x0000000f80110000, 0xffffffffc5118000),
]

ADDRESSES = [
    0x0000000000600000,
    0x0000000000868000,
    0x0000000040000000,
    0x0000000050040000,
    0x0000000106600010,
    0x0000000800600000,
    0x0000000801e28000,
    0x0000000996684088,
    0x0000000d08100000,
    0x0000000f80110000,
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


def from_badram(bad_ram: Sequence[tuple[int, int]] = BADRAM) -> Sequence[int | tuple[int, int]]:
    """
    Converts the badram format to the format used by ADDRESSES.
    That is, either a singular bad address, or a (start, stop) range of them.
    """

    addresses = []
    for start, mask in bad_ram:
        stop = start & mask
        if start == stop:
            addresses.append(start)
        else:
            addresses.append((start, stop))
    return addresses


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
    print("[")
    for value in from_badram():
        match value:
            case (start, stop):
                print(f"    (0x{start:016x}, 0x{stop:016x}),")
            case address:
                print(f"    0x{address:016x},")
    print("]")
