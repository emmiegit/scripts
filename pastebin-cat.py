#!/usr/bin/env python3

import re
import sys
import urllib.request

PASTEBIN_URL_REGEX = re.compile(r'https?://pastebin.com/(?:[a-z]+/)?(\w+)')

def download_pastebin(pb_url):
    match = PASTEBIN_URL_REGEX.match(pb_url)
    if match is None:
        print(f"'{pb_url}' does not appear to be a Pastebin URL", file=sys.stderr)
        return None
    raw_url = f"https://pastebin.com/raw/{match.group(1)}"

    print(f"Downloading '{raw_url}'...", file=sys.stderr)
    response = urllib.request.urlopen(raw_url)
    charset = response.info().get_param('charset', 'utf-8')
    data = response.read()
    text = data.decode(charset)
    return text + '\n'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} URL...", file=sys.stderr)
        exit(1)

    ret = 0
    for url in sys.argv[1:]:
        paste = download_pastebin(url)
        if paste is None:
            ret = 1
        print(paste)
    exit(ret)

