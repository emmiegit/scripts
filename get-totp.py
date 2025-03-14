#!/usr/bin/env python

import argparse
import re
import sys
import subprocess
from dataclasses import dataclass
from typing import Self
from urllib.parse import parse_qs, unquote, urlparse

from colorama import init as colorama_init, Fore


def first_or_none(params, key):
    try:
        return params[key][0]
    except KeyError:
        return None


def run_command(command):
    return subprocess.check_output(command).decode("utf-8")


@dataclass(frozen=True)
class TotpCode:
    name: str
    account: str
    secret: str
    digits: str
    period: str

    @staticmethod
    def fetch_all() -> list[Self]:
        totp_raw = run_command(["pass", "show", "misc/totp-codes"])
        totp_codes = []

        for line in totp_raw.splitlines():
            parts = urlparse(line)
            assert parts.netloc == "totp", "OTP kind not TOTP"
            assert parts.path.startswith("/")

            name = unquote(parts.path[1:])
            if ":" in name:
                name, account = name.split(":", 1)
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

    def get(self) -> str:
        command = ["oathtool", "--base32", "--totp"]
        if self.digits:
            command.append(f"--digits={self.digits}")
        if self.period:
            command.append(f"--time-step-size={self.period}")
        command.append(self.secret)
        return run_command(command).strip()

    @property
    def color_name(self):
        base = f"{Fore.MAGENTA}{self.name}{Fore.RESET}"

        if self.account is None:
            return base
        else:
            return f"{base} ({Fore.GREEN}{self.account}{Fore.RESET})"


def find_matching(totps, app_regex):
    matching = []

    for totp in totps:
        if app_regex.search(totp.name):
            matching.append(totp)

    return matching


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
    all_totps = TotpCode.fetch_all()

    # No arguments, list all app names
    if not args.app:
        print("List of all TOTP applications:")
        if not all_totps:
            print("* (no entries found)")
        for totp in all_totps:
            print(f"* {totp.color_name}: {totp.get()}")
        sys.exit(0)

    # Print TOTP codes for each app listed
    for app_pattern in args.app:
        app_regex = re.compile(app_pattern, re.IGNORECASE)
        totps = find_matching(all_totps, app_regex)
        if not totps:
            print(f"No matches for '{app_pattern}'", file=sys.stderr)
            exit_code += 1
            continue
        for totp in totps:
            print(f"{totp.color_name}: {totp.get()}")

    sys.exit(exit_code)
