#!/bin/python
from __future__ import with_statement
from os.path import expanduser
import re, os, sys

APP_DIRS = ("/usr/share/applications/", expanduser("~/.local/share/applications/"))
APP_NAME_RE = re.compile(r"(?:.*\n)*Name=(.*)\n(?:.*\n)")
APP_EXEC_RE = re.compile(r"(?:.*\n)*Exec=(.*)\n(?:.*\n)")
APP_COMM_RE = re.compile(r"(?:.*\n)*Comment=(.*)\n(?:.*\n)")

def list_if_match(appdir, fn, regex, options):
    if not appdir.endswith('/'):
        appdir = appdir + '/'

    with open(appdir + fn, 'r') as fh:
        contents = fh.read()

        try:
            name = APP_NAME_RE.match(contents).group(1)
        except AttributeError:
            return

        try:
            execn = APP_EXEC_RE.match(contents).group(1)
        except AttributeError:
            return

        try:
            comment = APP_COMM_RE.match(contents).group(1)
        except AttributeError:
            return

        if re.findall(regex, name, options["REGEX_FLAGS"]) or (options["SEARCH_ONLY_NAME"] and re.findall(regex, comment, options["REGEX_FLAGS"])):
            if options["SHOW_FILENAME"] and options["SHOW_COMMENT"]:
                print("%s (%s%s)\n\t%s\n\t%s" % (appdir, name, fn, comment, execn))
            elif options["SHOW_FILENAME"]:
                print("%s (%s)" % (name, fn))
            elif options["SHOW_COMMENT"]:
                print("%s\n\t%s" % (name, comment))
            else:
                print(name)

def usage():
    print("Usage: %s [options] pattern" % (sys.argv[0].split("/")[-1]))

def help_and_quit():
    usage()
    print("Available options:")
    print(" -c --casesensitive Perform a case-sensitive search.")
    print(" -h --help          Prints this help text and quits.")
    print(" -n --nofilename    Don't print the filenames of matches.")
    print(" -o --onlynames     Only search application names.")
    print(" -r --regex         Use regular expression instead of basic wildcards.")
    print(" -s --showcomment   Print the comment of the application.")
    exit(0)

def version_and_quit():
    print("Findapp version 0.2")
    print("Copyright (C) 2015 by Ammon Smith.")
    print("Licensed under the MIT License.")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        usage()
        exit(1)

    regex = sys.argv[-1]
    options = {
        "USE_REGEX" : False,
        "SHOW_FILENAME" : True,
        "SEARCH_ONLY_NAME" : False,
        "REGEX_FLAGS" : re.IGNORECASE,
        "SHOW_COMMENT" : False,
    }

    def ASSIGN_FLAG(key, value):
        options[key] = value

    def REMOVE_FLAG(key, value):
        options[key] &= ~value

    def TRIGGER_FLAG(key):
        if FLAGS.get(key, lambda: True)():
            print("Unknown option or flag: '%s'" % key)
            exit(1)

    FLAGS = {
        "h"    : help_and_quit,
        "help" : help_and_quit,
        "v"       : version_and_quit,
        "version" : version_and_quit,
        "o"         : lambda: ASSIGN_FLAG("SEARCH_ONLY_NAME", False),
        "onlynames" : lambda: ASSIGN_FLAG("SEARCH_ONLY_NAME", False),
        "r"     : lambda: ASSIGN_FLAG("USE_REGEX", True),
        "regex" : lambda: ASSIGN_FLAG("USE_REGEX", True),
        "n"          : lambda: ASSIGN_FLAG("SHOW_FILENAME", False),
        "nofilename" : lambda: ASSIGN_FLAG("SHOW_FILENAME", False),
        "c"             : lambda: REMOVE_FLAG("REGEX_FLAGS", re.IGNORECASE),
        "casesensitive" : lambda: REMOVE_FLAG("REGEX_FLAGS", re.IGNORECASE),
        "s"             : lambda: ASSIGN_FLAG("SHOW_COMMENT", True),
        "showcomment"   : lambda: ASSIGN_FLAG("SHOW_COMMENT", True),
    } 

    if regex == "-h" or regex == "--help":
        help_and_quit()

    for opt in sys.argv[1:-1]:
        if opt.startswith("--"):
            TRIGGER_FLAG(opt[2:])
        elif opt.startswith("-") and len(opt) == 2:
            TRIGGER_FLAG(opt[1])
        else:
            if opt[0] == "-":
                opt = opt[1:]
            for flag in opt:
                TRIGGER_FLAG(flag)
        
    if not options["USE_REGEX"]:
        regex = regex.replace("\\", "\\\\") \
                     .replace(".", "\\.")   \
                     .replace("*", ".*")    \
                     .replace("?", ".?")

    for appdir in APP_DIRS:
        for fn in os.walk(appdir).next()[2]:
            list_if_match(appdir, fn, regex, options)

