#!/usr/bin/env python

import argparse
from glob import iglob
import os
import re
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
RSYNC_RETRIES = 3

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
        torrent_url = urljoin(args.url, href)

        r = requests.get(torrent_url, stream=True)
        torrent_file = os.path.join(torrent_directory, filename)
        with open(torrent_file, "wb") as file:
            print(f"+ {filename}")
            for chunk in r.iter_content(chunk_size=512):
                file.write(chunk)


def download_torrent(torrent_file):
    print(f"Downloading Wikicomma torrent data ({torrent_file})")

    run_command(
        [
            "aria2c",
            "--continue",
            "--dir",
            DOWNLOADS_DIRECTORY,
            "--max-concurrent-downloads",
            "8",
            "--split",
            "8",
            "--http-accept-gzip",
            "true",
            "--seed-time",
            "0",
            torrent_file,
        ]
    )
    torrent_name, _ = os.path.splitext(os.path.basename(torrent_file))
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
        "--delete-after",
        source,
        destination,
    ]

    # Retry a few times in case of errors
    for _ in range(RSYNC_RETRIES):
        try:
            run_command(command)
            break
        except subprocess.CalledProcessError as exc:
            print(f"rsync error: {exc}")
            continue


def cleanup_data(torrent_file, download_dir):
    print("Finished upload")
    print(f"Deleting {torrent_file}")
    os.remove(torrent_file)  # since we use *.torrent files to track status

    print(f"Deleting {download_dir}")
    shutil.rmtree(download_dir)  # temporary storage before upload


def transfer_torrents(torrent_date, torrent_directory):
    destination_path = os.path.join(UPLOAD_SSH_PATH, torrent_date)
    destination = f"{UPLOAD_SSH_SERVER}:{destination_path}"

    torrent_glob = os.path.join(torrent_directory, "*.torrent")
    processed_torrent = False
    for torrent_file in iglob(torrent_glob):
        download_path = download_torrent(torrent_file)
        upload_data(download_path, destination)
        cleanup_data(torrent_file, download_path)
        processed_torrent = True

    if not processed_torrent:
        print("Nothing to do (did you run with -t first?)")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-t",
        "--fetch-torrents",
        dest="fetch_torrents",
        action="store_true",
        help="One-time job to fetch all the *.torrent files to pull from",
    )
    argparser.add_argument("url")
    args = argparser.parse_args()

    match = WIKICOMMA_URL_REGEX.fullmatch(args.url)
    if match is None:
        print("Warning: URL does not match known Wikicomma torrent path")
        sys.exit(1)

    torrent_date = match[1]
    torrent_directory = os.path.join(TORRENT_DIRECTORY, torrent_date)

    try:
        if args.fetch_torrents:
            # Run the fetch-torrents action, then exit
            os.makedirs(torrent_directory, exist_ok=True)
            download_torrent_files(torrent_directory, args.url)
        else:
            # Otherwise, assuming torrent files exist, and then download/upload
            os.makedirs(DOWNLOADS_DIRECTORY, exist_ok=True)
            transfer_torrents(torrent_date, torrent_directory)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)
