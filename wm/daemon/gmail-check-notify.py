#!/usr/bin/env python3

from xml.etree import ElementTree as etree
import atexit
import os
import signal
import subprocess
import time
import traceback
import urllib.request

PID_FILE = "/run/user/%d/gmail-notify.pid" % os.geteuid()

# Constants
GMAIL_FEED = "https://mail.google.com/gmail/feed/atom"
NS = "{http://purl.org/atom/ns#}"

# Options
GMAIL_CREDENTIALS = "/usr/local/scripts/dat/gmail.gpg"
DELAY = 60


def pid_exists(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def notify(summary, text=None):
    if text:
        os.system("notify-send '%s' '%s'" % (summary, text))
    else:
        os.system("notify-send '%s'" % (summary))


def create_pidfile():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as fh:
                pid = int(fh.read().rstrip())

            if pid_exists(pid):
                notify("Gmail notifier already running.")
            else:
                notify("Gmail notifier has died, but pid file remains.")
            exit(1)
        except:
            traceback.print_exc()
            notify("Unable to get pid from pidfile. Quitting gmail notifier.")
            exit(1)
    else:
        try:
            with open(PID_FILE, "w") as fh:
                fh.write("%d\n" % os.getpid())
        except:
            traceback.print_exc()
            notify("Unable to write to pidfile. Quitting gmail notifier.")
            exit(1)


def remove_pidfile():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as fh:
                pid = int(fh.read().rstrip())

            if os.getpid() == pid:
                os.unlink(PID_FILE)
        except:
            traceback.print_exc()
            notify("Error reading gmail notifier pid file.")


if __name__ == "__main__":
    create_pidfile()

    atexit.register(remove_pidfile)
    signal.signal(signal.SIGTERM, remove_pidfile)
    signal.signal(signal.SIGINT, remove_pidfile)
    signal.signal(signal.SIGHUP, remove_pidfile)

    if not os.path.exists(GMAIL_CREDENTIALS):
        notify("Can't find gmail credentials file.", GMAIL_CREDENTIALS);
        exit(1)

    try:
        cred = subprocess.check_output(("gpg", "-d", GMAIL_CREDENTIALS)).split(b'\n')
        user = cred[0].decode()
        passwd = cred[1].decode()
    except:
        traceback.print_exc()
        notify("Unable to extract gmail credentials.")
        exit(1)

    try:
        # Set up authentication for gmail
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm="mail.google.com",
                                  uri="https://mail.google.com/",
                                  user=user,
                                  passwd=passwd)
        opener = urllib.request.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        urllib.request.install_opener(opener)
        del cred, user, passwd
    except:
        traceback.print_exc()
        notify("Unable to authenticate with gmail.")
        exit(1)

    # Number of unread emails we've already told the user about
    unread = 0
    while True:
        try:
            with urllib.request.urlopen(GMAIL_FEED) as source:
                tree = etree.parse(source)
        except:
            traceback.print_exc()
            notify("Authentication failed.")
            time.sleep(DELAY)
            continue

        rawcount = tree.find(NS + "fullcount").text
        try:
            count = int(rawcount)
        except ValueError:
            traceback.print_exc()
            notify("Got a rawcount that's not an integer: \"%s\"" % (rawcount,))
            count = 0

        count -= unread
        if count:
            notify("%d new email%s" % (count, "" if count == 1 else "s"))
            unread += count

        try:
            time.sleep(DELAY)
        except:
            remove_pidfile()
