#!/usr/bin/env python3
from socket import *
from time import localtime
from os import geteuid
import random, sys, signal

def handle_exit(signal, frame):
    sys.exit(0)

def handle_sigusr1(signal, frame):
    load_quotes()

def load_quotes(*args, **kwargs):
    global quotes
    with open("/usr/local/scripts/dat/quotes.txt", 'r') as fh:
        quotes = fh.read().split("\n")

def get_quote():
    global quotes
    loc = localtime()
    random.seed(loc.tm_year << 16 | loc.tm_yday)
    return random.choice(quotes)

def listen():
    while True:
        connection, address = sock.accept()
        message = "\nHello, %s.\nHere is today's quote of the day:\n\n%s\n\n" % (address[0], get_quote())
        connection.send(bytearray(message, "UTF-8"))
        connection.close()

if __name__ == "__main__":
    if geteuid() != 0:
        print("You must be root to bind to ports below 1024.")
        exit(1)

    sock = socket(AF_INET, SOCK_STREAM) # Creates TCP socket
    sock.bind(("", 17)) # host, port
    sock.listen(5)

    signal.signal(signal.SIGUSR1, load_quotes)
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    load_quotes()
    listen()

