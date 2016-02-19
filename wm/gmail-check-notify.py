#!/usr/bin/env python3

import urllib.request
from xml.etree import ElementTree as etree
import os, subprocess, time

# Constants
GMAIL_FEED = "https://mail.google.com/gmail/feed/atom"
NS = "{http://purl.org/atom/ns#}"

# Options
GMAIL_CREDENTIALS = "/usr/local/scripts/dat/gmail.gpg"
DELAY = 60

def notify(summary, text=None):
    if text:
        os.system("notify-send '%s' '%s'" % (summary, text))
    else:
        os.system("notify-send '%s'" % (summary))

if not os.path.exists(GMAIL_CREDENTIALS):
    notify("Can't find gmail credentials file.", GMAIL_CREDENTIALS);
    exit(1)

try:
    cred = subprocess.check_output(("gpg", "-d", GMAIL_CREDENTIALS)).split(b'\n')
    user = cred[0].decode()
    passwd = cred[1].decode()
except:
    notify("Unable to extract gmail credentials.")
    exit(1)

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

# Number of unread emails we've already told the user about
unread = 0
while True:
    with urllib.request.urlopen(GMAIL_FEED) as source:
        tree = etree.parse(source)

    rawcount = tree.find(NS + "fullcount").text
    try:
        count = int(rawcount)
    except ValueError:
        notify("Got a rawcount that's not an integer: \"%s\"" % (rawcount,))
        count = 0

    count -= unread
    if count:
        notify("%d new email%s" % (count, "" if count == 1 else "s"))
        unread += count

    time.sleep(DELAY)

