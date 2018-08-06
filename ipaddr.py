#!/usr/bin/env python3

import ipaddress
import sys

def make_6to4(addr4, prefix=b'\x20\x02'):
    baddr6 = b''.join((prefix, addr4.packed, b'\x00' * 10))
    return ipaddress.IPv6Address(baddr6)

FLAGS = (
    ('is_loopback', 'loopback'),
    ('is_unspecified', 'unspecified'),
    ('is_reserved', 'reserved'),
    ('is_multicast', 'multicast'),
    ('is_private', 'private'),
    ('is_global', 'global'),
    ('is_link_local', 'link local'),
    ('is_site_local', 'site local'),
)

def print_ipv4_info(addr):
    flags = []

    for attr, name in FLAGS:
        if getattr(addr, attr, False):
            flags.append(name)

    print("Address:  {}".format(addr))
    if flags:
        print("Flags:    {}".format(', '.join(flags)))
    print("6to4:     {}".format(make_6to4(addr)))
    print("Teredo:   {}".format(make_6to4(addr, b'\x20\x01')))
    print("Reverse:  {}".format(addr.reverse_pointer))

def print_ipv6_info(addr):
    flags = []

    for attr, name in FLAGS:
        if getattr(addr, attr, False):
            flags.append(name)

    print("Address:  {}".format(addr))
    if flags:
        print("Flags:    {}".format(', '.join(flags)))
    print("IPv4 map: {}".format(addr.ipv4_mapped))
    print("6to4:     {}".format(addr.sixtofour))
    print("Teredo:   {}".format(addr.teredo))
    print("Reverse:  {}".format(addr.reverse_pointer))

PRINTERS = {
    4: print_ipv4_info,
    6: print_ipv6_info,
}

if __name__ == '__main__':
    for i, s_addr in enumerate(sys.argv[1:]):
        addr = ipaddress.ip_address(s_addr)
        PRINTERS[addr.version](addr)

        if i < len(sys.argv[1:]) - 1:
            print("-------")
