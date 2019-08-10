#!/usr/bin/python3

import re
import sys

from bs4 import BeautifulSoup
from urllib.request import urlopen

SCP_SERIES_REGEX = re.compile(r'/scp-[0-9]{3,4}')

def count_slots(url):
    with urlopen(url) as response:
        data = response.read()

    empty_slots = 0
    total_slots = 0
    scps = set()

    soup = BeautifulSoup(data, 'html.parser')
    for link in soup.select('.series a'):
        href = link.get('href')
        if href is None or SCP_SERIES_REGEX.match(href) is None:
            continue

        if href in scps:
            continue

        scps.add(href)
        total_slots += 1
        if link.get('class') == ['newpage']:
            empty_slots += 1

    return empty_slots, total_slots

def get_series_url(number):
    if number == 1:
        return 'http://www.scp-wiki.net/scp-series'
    else:
        return f'http://www.scp-wiki.net/scp-series-{number}'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        series = int(sys.argv[1])
    else:
        series = 5

    url = get_series_url(series)
    print(f'Counting slots in {url}...')
    empty, total = count_slots(url)
    print(f'{empty} / {total} slots empty ({empty/total*100:.2f}%)')
