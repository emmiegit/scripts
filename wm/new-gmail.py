#!/usr/bin/env python3

import urllib.request
from xml.etree import ElementTree as etree
from getpass import getpass

user=input("Enter your gmail username: ")
passwd=getpass("Enter your gmail password: ")

# Enter your username and password below within quotes below, in place of ****.
# Set up authentication for gmail
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='mail.google.com',
                          uri='https://mail.google.com/',
                          user=user,
                          passwd=passwd)
opener = urllib.request.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib.request.install_opener(opener)

gmail = 'https://mail.google.com/gmail/feed/atom'
NS = '{http://purl.org/atom/ns#}'
with urllib.request.urlopen(gmail) as source:
    tree = etree.parse(source)
fullcount = tree.find(NS + 'fullcount').text

print(fullcount + ' new')

