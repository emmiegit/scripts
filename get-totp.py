#!/usr/bin/env python

import argparse
import re
import sys
import subprocess
from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urlparse

from colorama import init as colorama_init, Fore


@dataclass(frozen=True)
class TotpCode:
    name: str
    account: str
    secret: str
    digits: str
    period: str


def first_or_none(params, key):
    try:
        return params[key][0]
    except KeyError:
        return None

def get_totp_codes():
    totp_raw = subprocess.check_output(["pass", "show", "misc/totp-codes"]).decode("utf-8")
    totp_codes = []

    for line in totp_raw.splitlines():
        parts = urlparse(line)
        assert parts.netloc == "totp", "OTP kind not TOTP"
        assert parts.path.startswith("/")

        name = unquote(parts.path[1:])
        if ":" in name:
            name, account = name.split(":")
        else:
            account = None

        params = parse_qs(parts.query)
        secret = first_or_none(params, "secret")
        digits = first_or_none(params, "digits")
        period = first_or_none(params, "period")
        totp_codes.append(
            TotpCode(
                name=name,
                account=account,
                secret=secret,
                digits=digits,
                period=period,
            )
        )

    return totp_codes

def get_totp(entry):
    command = ["oathtool", "--base32", "--totp"]
    if entry.digits:
        command.append(f"--digits={entry.digits}")
    if entry.period:
        command.append(f"--time-step-size={entry.period}")
    command.append(entry.secret)

    raw_output = subprocess.check_output(command)
    return raw_output.decode("utf-8").strip()

def find_matching(totp_codes, app_regex):
    matching = []

    for entry in totp_codes:
        if app_regex.search(entry.name):
            matching.append(entry)

    return matching

def format_name(entry):
    base = f"{Fore.MAGENTA}{entry.name}{Fore.RESET}"

    if entry.account is None:
        return base
    else:
        return f"{base} ({Fore.GREEN}{entry.account}{Fore.RESET})"


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="get-totp.py",
        description="Fetch TOTP codes from the command line",
    )
    argparser.add_argument(
        "app",
        nargs="*",
        help="Which application(s) to show codes for. If not specified, show all applications.",
    )
    args = argparser.parse_args()

    exit_code = 0
    colorama_init()
    totp_codes = get_totp_codes()

    # No arguments, list all app names
    if not args.app:
        print("List of all TOTP applications:")
        if not totp_codes:
            print("* (no entries found)")
        for entry in totp_codes:
            totp = get_totp(entry)
            print(f"* {format_name(entry)}: {totp}")

        sys.exit(0)

    # Print TOTP codes for each app listed
    for app_pattern in args.app:
        app_regex = re.compile(app_pattern, re.IGNORECASE)
        entries = find_matching(totp_codes, app_regex)
        if not entries:
            print(f"No matches for '{app_pattern}'", file=sys.stderr)
            exit_code += 1
            continue

        for entry in entries:
            totp = get_totp(entry)
            print(f"{format_name(entry)}: {totp}")

    sys.exit(exit_code)
