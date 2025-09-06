#!/usr/bin/env python

import argparse
import asyncio
from glob import iglob
import os
import re
import shutil
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

TORRENT_DIRECTORY = "/media/media/temporary/wikicomma"
TORRENT_URL_REGEX = re.compile(r"/snapshots/[^\.]+\.torrent/[^\.]+\.torrent")
WIKICOMMA_URL_REGEX = re.compile(
    r"https://wikidot.dbotthepony.ru/snapshots/([^\.]+)\.torrent/?"
)


def download_torrent_files(torrent_directory, url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    # First, check if any *.torrent files exist
    torrent_glob = os.path.join(torrent_directory, "*.torrent")
    if next(iglob(torrent_glob), None) is not None:
        print(f"Existing {torrent_glob} files found, exiting")
        sys.exit(1)

    print("Downloading torrent files")
    for link in soup.select("td.fb-n a"):
        href = link["href"]
        if TORRENT_URL_REGEX.fullmatch(href) is None:
            # skip invalid links, like the ".." parent link
            print(f"Skipping invalid link: {href!r}")
            continue

        filename = os.path.basename(href)
        torrent_url = urljoin(url, href)

        r = requests.get(torrent_url, stream=True)
        torrent_file = os.path.join(torrent_directory, filename)
        with open(torrent_file, "wb") as file:
            print(f"+ {filename}")
            for chunk in r.iter_content(chunk_size=512):
                file.write(chunk)


async def main(args):
    match = WIKICOMMA_URL_REGEX.fullmatch(args.url)
    if match is None:
        print("Warning: URL does not match known Wikicomma torrent path")
        sys.exit(1)

    torrent_date = match[1]
    torrent_directory = os.path.join(TORRENT_DIRECTORY, torrent_date)

    try:
        os.makedirs(torrent_directory, exist_ok=True)
        download_torrent_files(torrent_directory, args.url)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url", help="The Wikicomma torrent directory")
    args = argparser.parse_args()
    asyncio.run(main(args))
