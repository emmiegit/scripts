#!/usr/bin/env python3

from xml.etree import ElementTree as etree
import atexit
import os
import subprocess
import sys
import time
import traceback
import urllib.request

PID_FILE = f'/run/user/{os.geteuid()}/gmail-notify.pid'

# Constants
GMAIL_FEED = 'https://mail.google.com/gmail/feed/atom'
NS = r'{http://purl.org/atom/ns#}'

# Options
GMAIL_CREDENTIALS = '/usr/local/scripts/dat/gmail.gpg'
MAIN_DELAY = 60
BETWEEN_DELAY = 1

def pid_exists(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def notify(summary, text=None):
    args = ['notify-send', '--', summary]
    if text:
        args.append(text)
    subprocess.check_call(args)

def create_pidfile():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as fh:
                pid = int(fh.read().rstrip())

            if pid_exists(pid):
                notify("Gmail notifier already running.")
            else:
                notify("Gmail notifier has died, but pid file remains.")

            os.unlink(PID_FILE)
            exit(1)
        except:
            traceback.print_exc()
            notify("Unable to get pid from pidfile. Quitting gmail notifier.")
            exit(1)
    else:
        try:
            with open(PID_FILE, 'w') as fh:
                fh.write(f'{os.getpid()}\n')
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

def fork_off():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as ex:
        notify(f"Fork failed: {ex.errno} ({ex.strerror})")

def daemonize():
    # Have the parent exit
    fork_off()

    os.chdir('/')
    os.setsid()
    os.umask(0)

    # Have the second parent exit
    fork_off()

    # Redirect descriptors
    sys.stdout.flush()
    sys.stderr.flush()

    with open(os.devnull, 'r') as si:
        os.dup2(si.fileno(), sys.stdin.fileno())

    with open(os.devnull, 'a+') as so:
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(so.fileno(), sys.stderr.fileno())

    # Create pidfile and set up for its deletion
    create_pidfile()
    atexit.register(remove_pidfile)

class UnreadNotifier:
    __slots__ = (
        'unread',
    )

    def __init__(self):
        self.unread = 0

    def try_check(self, attempts=10):
        for _ in range(attempts):
            if self.check():
                return True

        # Exhausted all attempts
        notify("Authentication failed.")
        return False

    def check(self):
        try:
            with urllib.request.urlopen(GMAIL_FEED) as source:
                tree = etree.parse(source)

            time.sleep(BETWEEN_DELAY)
        except:
            traceback.print_exc()
            return False

        rawcount = tree.find(NS + "fullcount").text
        try:
            count = int(rawcount)
        except ValueError:
            traceback.print_exc()
            notify(f"Got a count that's not an integer: '{rawcount}'")
            self.count = 0
            return False

        count -= self.unread
        if count > 0:
            plural = '' if count == 1 else 's'
            notify(f"{count} new email{plural}")
            self.unread += count

        return True

    def main_loop(self):
        while True:
            self.try_check()
            time.sleep(MAIN_DELAY)

if __name__ == '__main__':
    if not os.path.exists(GMAIL_CREDENTIALS):
        notify("Can't find gmail credentials file.", GMAIL_CREDENTIALS)
        exit(1)

    try:
        cred = subprocess.check_output(['gpg', '-d', GMAIL_CREDENTIALS]).split(b'\n')
        user = cred[0].decode()
        passwd = cred[1].decode()
    except:
        traceback.print_exc()
        notify("Unable to extract gmail credentials.")
        exit(1)

    daemonize()

    try:
        # Set up authentication for gmail
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='mail.google.com',
                                  uri='https://mail.google.com/',
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

    notifier = UnreadNotifier()
    notifier.main_loop()
