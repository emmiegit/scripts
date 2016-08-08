#!!/usr/bin/env python2
__all__ = ["get_pass"]

from subprocess import check_output
import os.path

def get_pass():
    return check_output(["gpg", "-dq", os.path.expanduser("~/.mutt/passwd.gpg")]).strip("\n")

