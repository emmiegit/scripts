#!/usr/bin/env python

import argparse
import os
import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


WIKICOMMA_URL_REGEX = re.compile(
    r"https://wikidot.dbotthepony.ru/snapshots/[^\.]+\.torrent/?"
)
TORRENT_URL_REGEX = re.compile(r"/snapshots/[^\.]+\.torrent/[^\.]+\.torrent")
DOWNLOADS_DIR = os.path.expanduser("~/incoming")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url")
    args = argparser.parse_args()

    if WIKICOMMA_URL_REGEX.fullmatch(args.url) is None:
        print(f"Warning: URL does not match known Wikicomma torrent path")

    r = requests.get(args.url)
    soup = BeautifulSoup(r.text, features="html.parser")

    for link in soup.select("td.fb-n a"):
        href = link["href"]
        if TORRENT_URL_REGEX.fullmatch(href) is None:
            # skip invalid links, like the ".." parent link
            continue

        torrent_url = urljoin(args.url, href)
        filename = os.path.basename(href)

        r = requests.get(torrent_url, stream=True)
        with open(os.path.join(DOWNLOADS_DIR, filename), "wb") as file:
            print(f"+ {filename}")
            for chunk in r.iter_content(chunk_size=512):
                file.write(chunk)
