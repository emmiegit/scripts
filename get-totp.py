#!/usr/bin/python3

import json
import sys
import subprocess

from colorama import init as colorama_init, Fore

def get_totp_codes():
    totp_json = subprocess.check_output(["pass", "show", "misc/totp-codes"])
    totp_codes = json.loads(totp_json)
    return { entry["name"]: entry for entry in totp_codes }

def get_totp(secret):
    raw_output = subprocess.check_output(["oathtool", "--base32", "--totp", secret])
    return raw_output.decode("utf-8").strip()

def find_most_similar(totp_data, search_name):
    case_insensitive = search_name.islower()

    for name, entry in totp_data.items():
        if case_insensitive:
            name = name.lower()

        if search_name in name:
            return entry

    return None

if __name__ == "__main__":
    exit_code = 0
    colorama_init()
    totp_data = get_totp_codes()

    # No arguments, list all app names
    if len(sys.argv) < 2:
        print("List of all TOTP applications:")
        if not totp_data:
            print("* (no entries found)")
        for name in totp_data:
            totp = get_totp(totp_data[name]["secret"])
            print(f"* {Fore.MAGENTA}{name}{Fore.RESET}: {totp}")

        sys.exit(0)

    # Print TOTP codes for each app listed
    for app_name in sys.argv[1:]:
        entry = find_most_similar(totp_data, app_name)
        if entry is None:
            print(f"No match for '{app_name}'", file=sys.stderr)
            exit_code = 1
            continue

        name = entry["name"]
        totp = get_totp(entry["secret"])
        print(f"{Fore.MAGENTA}{name}{Fore.RESET}: {totp}")

    sys.exit(exit_code)
