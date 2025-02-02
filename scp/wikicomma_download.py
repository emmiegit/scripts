#!/usr/bin/env python

import argparse
import re
import os
import shutil
import subprocess
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

TORRENT_DIRECTORY = "/tmp/emmie/wikicomma"
DOWNLOADS_DIRECTORY = "/media/archive/temporary/wikicomma"
UPLOAD_SSH_SERVER = "rsync.net"
UPLOAD_SSH_PATH = "./wikicomma"

TORRENT_URL_REGEX = re.compile(r"/snapshots/[^\.]+\.torrent/[^\.]+\.torrent")
WIKICOMMA_URL_REGEX = re.compile(
    r"https://wikidot.dbotthepony.ru/snapshots/([^\.]+)\.torrent/?"
)


def run_command(command):
    print(f"Running {command}")
    subprocess.check_call(command)


def download_torrent_files(torrent_directory, url):
    r = requests.get(args.url)
    soup = BeautifulSoup(r.text, features="html.parser")
    torrent_files = []

    print("Downloading torrent files")
    for link in soup.select("td.fb-n a"):
        href = link["href"]
        if TORRENT_URL_REGEX.fullmatch(href) is None:
            # skip invalid links, like the ".." parent link
            continue

        torrent_url = urljoin(args.url, href)
        filename = os.path.basename(href)

        r = requests.get(torrent_url, stream=True)
        torrent_file = os.path.join(torrent_directory, filename)
        with open(torrent_file, "wb") as file:
            print(f"+ {filename}")
            for chunk in r.iter_content(chunk_size=512):
                file.write(chunk)
        torrent_files.append(torrent_file)
    return torrent_files


def download_torrent(torrent_file):
    print(f"Downloading Wikicomma torrent data ({torrent_file})")

    run_command(
        [
            "aria2c",
            "--continue",
            "--dir",
            DOWNLOADS_DIRECTORY,
            "--seed-time",
            "0",
            torrent_file,
        ]
    )
    torrent_name = os.path.basename(torrent_file)
    path = os.path.join(DOWNLOADS_DIRECTORY, torrent_name)
    assert os.path.isdir(path), f"Download for {torrent_file} did not write to {path}"
    return path


def upload_data(source, destination):
    print(f"Uploading Wikicomma data to remote server ({destination})")
    command = [
        "rsync",
        "--verbose",
        "--archive",
        "--compress",
        "--human-readable",
        "--partial",
        "--progress",
        source,
        destination,
    ]
    subprocess.check_call(command)


def cleanup_data(directory):
    print(f"Finished upload, deleting ({directory})")
    shutil.rmtree(download_path)


def transfer_torrents(torrent_date, torrent_files):
    destination_path = os.path.join(UPLOAD_SSH_PATH, torrent_date)
    destination = f"{UPLOAD_SSH_SERVER}:{destination_path}"

    for torrent_file in torrent_files:
        download_path = download_torrent(torrent_file)
        upload_data(download_path, destination)
        cleanup_data(download_path)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url")
    args = argparser.parse_args()

    match = WIKICOMMA_URL_REGEX.fullmatch(args.url)
    if match is None:
        print("Warning: URL does not match known Wikicomma torrent path")
        sys.exit(1)

    torrent_date = match[1]
    torrent_directory = os.path.join(TORRENT_DIRECTORY, torrent_date)
    os.makedirs(torrent_directory, exist_ok=True)
    os.makedirs(DOWNLOADS_DIRECTORY, exist_ok=True)

    torrent_files = download_torrent_files(torrent_directory, args.url)
    transfer_torrents(torrent_date, torrent_files)
