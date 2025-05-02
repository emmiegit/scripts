#!/usr/bin/env python3

import os
import re
from stat import S_ISDIR, S_ISREG
import subprocess
import sys

ID3_INFO_REGEX = re.compile(r"=== ([^ ]+) \(.+\): (.+)")


def run_command(command):
    print(f"Running {command}")
    subprocess.check_call(command)


def is_opus(path):
    _, ext = os.path.splitext(path)
    return ext.casefold() == ".opus"


def valid_tags(path):
    result = subprocess.run(
        ["opustags", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def needs_repair(path):
    return is_opus(path) and not os.path.islink(path) and not valid_tags(path)


def get_id3_tags(path):
    metadata = {}
    output = subprocess.check_output(["id3info", path]).decode("utf-8")
    for line in output.split("\n"):
        match = ID3_INFO_REGEX.match(line)
        if match is None:
            continue

        tag, value = match[1], match[2]
        if not value:
            continue

        # See https://docs.mp3tag.de/mapping-table/
        match tag:
            # Standard tags
            case "TPE1":
                metadata["--artist"] = value
            case "TPE2":
                metadata["--album-artist"] = value
            case "TALB":
                metadata["--album"] = value
            case "TIT2":
                metadata["--title"] = value
            case "TRCK":
                metadata["--track"] = value
            case "COMM":
                metadata["--comment"] = value
            case "TYER":
                metadata["--year"] = value
            case "TCON":
                metadata["--genre"] = value
            # Other tags
            case "TMED":
                metadata["-X"] = f"MEDIATYPE={value}"
            case "TPUB":
                metadata["-X"] = f"PUBLISHER={value}"
            case "TPOS":
                metadata["-X"] = f"DISCNUMBER={value}"
            case "TORY":
                metadata["-X"] = f"ORIGYEAR={value}"
            # Ignored
            case "TXXX" | "UFID" | "APIC" | "TCMP" | "TSOP" | "TSO2" | "TDAT":
                pass
            # Unknown
            case _:
                raise ValueError(f"Unknown ID3 tag: {tag}")

    return metadata


def repair_file(path):
    if not needs_repair(path):
        return

    print(f"Repairing file {path}")

    # Retrieve existing tags
    metadata = get_id3_tags(path)

    # Clear ID3 tags
    run_command(["id3convert", "-s", path])

    # Re-apply tags using autotag in non-automatic mode (lol)
    arguments = ["tagit", "-x"]
    for key, value in metadata.items():
        arguments.extend((key, value))
    arguments.append(path)
    run_command(arguments)


def repair_directory(directory):
    for root, dirs, files in os.walk(directory):
        print(f"Checking {root} ({len(dirs)} directories, {len(files)} files)")

        for file in files:
            path = os.path.join(root, file)
            repair_file(path)


def repair_path(path):
    stat = os.stat(path)
    if S_ISREG(stat.st_mode):
        repair_file(path)
    elif S_ISDIR(stat.st_mode):
        repair_directory(path)
    else:
        # Let's not bother with character devices or whatever
        raise ValueError(f"Invalid file type: {path}")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        repair_path(path)
