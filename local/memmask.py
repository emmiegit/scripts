#!/usr/bin/env python

from typing import Sequence

ADDRESSES = [
    0x000000000062c010,
    0x0000000004060000,
    0x00000000106bdcd8,
    0x000000001febdcd8,
    0x000000002de88a40,
    0x0000000040160000,
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
]


def build_memmap(addresses: Sequence[int] = ADDRESSES) -> str:
    sep = r"\\\$"
    parts = ",".join(f"4K{sep}0x{address:016x}" for address in addresses)
    return f"memmap={parts}"

if __name__ == "__main__":
    print(build_memmap())
