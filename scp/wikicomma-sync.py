#!/usr/bin/env python3

"""
Downloads Wikicomma torrent files and then uploads each via rsync
"""

import argparse
import asyncio
import os
import re
import shutil
from typing import Final

DOWNLOAD_DIRECTORY: Final[str] = "/media/media/temporary/wikicomma"

WIKICOMMA_DATE_REGEX: Final[re.Pattern[str]] = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})-[0-9]{2}-[0-9]{2}-[0-9]{2}"
)

UPLOAD_SSH_SERVER: Final[str] = "rsync.net"  # params set in .ssh/config
UPLOAD_SSH_PATH: Final[str] = "./wikicomma"

# Helpers


class CalledProcessError(RuntimeError):
    def __init__(self, error_code: int, stderr: bytes):
        self.error_code = error_code
        self.stderr_bytes = stderr
        self.stderr_text = stderr.decode("utf-8")
        super().__init__(f"[{self.error_code}] {self.stderr_text}")


async def run_command(command: list[str], dry_run: bool = False) -> None:
    if dry_run:
        print(f"Running {command} (DRY-RUN)")
        return

    print(f"Running {command}")
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=None,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise CalledProcessError(proc.returncode, stderr)


def trim_wikicomma_date(value: str) -> str:
    """
    Converts a string like '2026-09-24-04-16-11' to just '2026-09-24'.
    """

    match = WIKICOMMA_DATE_REGEX.fullmatch(value)
    if match is None:
        raise ValueError(value)

    year, month, day = match[1], match[2], match[3]
    return f"{year}-{month}-{day}"


# Main functions


async def download_torrent(
    torrent_name: str,
    torrent_file_path: str,
    download_directory: str,
) -> None:
    command = [
        "aria2c",
        "--dir",
        download_directory,
        "--max-tries=3",
        "--retry-wait=10",
        "--max-concurrent-downloads=8",
        "--split=8",
        "--http-accept-gzip=true",
        "--seed-time=0",
        torrent_file_path,
    ]

    try:
        print(f"Downloading {torrent_name}")
        await run_command(command)
    except CalledProcessError as error:
        # Write out failure
        print(f"Download exited with exit code {error.exit_code}")
        path = os.path.join(download_directory, f"{torrent_name}-download-stderr")
        with open(path, "w") as file:
            file.write(error.stderr_text)
            file.write("\n")


async def upload_data(
    torrent_name: str,
    directory_path: str,
    date: str,
) -> None:
    torrent_name = os.path.basename(directory_path)
    destination = f"{UPLOAD_SSH_SERVER}:{UPLOAD_SSH_PATH}/{date}"
    command = [
        "rsync",
        "--verbose",
        "--archive",
        "--compress",
        "--human-readable",
        "--partial",
        "--progress",
        directory_path,
        destination,
    ]

    try:
        print(f"Uploading {torrent_name} to {UPLOAD_SSH_PATH}/{date}")
        await run_command(command)
    except CalledProcessError as error:
        # Write out failure
        print(f"Download exited with exit code {error.exit_code}")
        path = os.path.join(
            os.path.dirname(directory_path),
            f"{torrent_name}-upload-stderr",
        )
        with open(path, "w") as file:
            file.write(error.stderr_text)
            file.write("\n")


def cleanup_data(directory_path: str) -> None:
    print(f"Deleting download directory '{directory_path}'")
    shutil.rmtree(directory_path)


async def main(torrent_file_path: str) -> None:
    date = os.path.basename(os.path.dirname(torrent_file_path))  # assumes parent directory is the wikicomma torrent list
    date = trim_wikicomma_date(date)
    torrent_name, _ = os.path.splitext(os.path.basename(torrent_file_path))

    print(f"Running sync for {torrent_name} on {date}")
    await download_torrent(torrent_name, torrent_file_path, DOWNLOAD_DIRECTORY)
    download_path = os.path.join(DOWNLOAD_DIRECTORY, torrent_name)
    await upload_data(torrent_name, download_path, date)
    cleanup_data(download_path)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "torrent-file",
        nargs="?",
        type=str,
        help="Path to a Wikicomma *.torrent file",
    )
    args = argparser.parse_args()
    asyncio.run(main(args.torrent_file))
