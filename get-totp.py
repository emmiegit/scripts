#!/usr/bin/python3

import re
import sys
import subprocess
from collections import namedtuple
from urllib.parse import parse_qs, unquote, urlparse

from colorama import init as colorama_init, Fore

TotpCode = namedtuple("OtpInfo", ("name", "account", "secret", "digits", "period"))


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
        totp_codes.append(TotpCode(name=name, account=account, secret=secret, digits=digits, period=period))

    return totp_codes

def get_totp(code):
    command = ["oathtool", "--base32", "--totp"]
    if code.digits:
        command.append(f"--digits={code.digits}")
    if code.period:
        command.append(f"--time-step-size={code.period}")
    command.append(code.secret)

    raw_output = subprocess.check_output(command)
    return raw_output.decode("utf-8").strip()

def find_matching(totp_codes, app_regex):
    matching = []

    for entry in totp_codes:
        if app_regex.search(entry.name):
            matching.append(entry)

    return matching

if __name__ == "__main__":
    exit_code = 0
    colorama_init()
    totp_codes = get_totp_codes()

    # No arguments, list all app names
    if len(sys.argv) < 2:
        print("List of all TOTP applications:")
        if not totp_codes:
            print("* (no entries found)")
        for code in totp_codes:
            totp = get_totp(code)
            print(f"* {Fore.MAGENTA}{code.name}{Fore.RESET}: {totp}")

        sys.exit(0)

    # Print TOTP codes for each app listed
    for app_pattern in sys.argv[1:]:
        app_regex = re.compile(app_pattern, re.IGNORECASE)
        entries = find_matching(totp_codes, app_regex)
        if not entries:
            print(f"No matches for '{app_pattern}'", file=sys.stderr)
            exit_code = 1
            continue

        for entry in entries:
            totp = get_totp(entry)
            print(f"{Fore.MAGENTA}{entry.name}{Fore.RESET}: {totp}")

    sys.exit(exit_code)
