#!/usr/bin/python
import os, sys

def draw_corner(phrase):
    print(phrase)
    for c in phrase[1:]:
        print(c)

def draw_box(phrase):
    print(phrase)
    leng = len(phrase)
    spaces = ' ' * (leng - 2)
    for i in range(leng - 2):
        print("%s%s%s" % (phrase[i + 1], spaces, phrase[leng - i - 2]))
    print(phrase[::-1])

def draw_square(phrase):
    for i in range(len(phrase)):
        print(phrase)
        phrase = phrase[1:] + phrase[0]

def print_usage():
    print("Usage: %s [options] phrase" % sys.argv[0].split(os.sep)[-1])

if __name__ == "__main__":
    options = {"box" : False, "square" : False, "spaces" : False}
    args = sys.argv

    if len(args) == 1:
        print_usage()
        exit(1)
    elif args[-1] in ("-h", "--help"):
        print_usage()
        print("Available options:")
        print("  -b  --box    Draw the text around in a box.")
        print("  -h  --help   Print this help text.")
        print("  -s  --square Draw the text in a solid square.")
        print("  -S  --spaces Add spaces in between each character.")
        exit(0)

    while len(args) > 1:
        if args[0][0] == '-':
            if args[0][1] == '-':
                if arg == "--box":
                    options["box"] = True
                elif arg == "--square":
                    options["square"] = True
                elif arg == "--spaces":
                    options["spaces"] = True
                else:
                    print("Unknown option: '%s'" % args[0])
                    exit(1)
            else:
                for arg in args[0][1:]:
                    if arg == 'b':
                        options["box"] = True
                    elif arg == 's':
                        options["square"] = True
                    elif arg == 'S':
                        options["spaces"] = True
                    else:
                        print("Unknown option: '%s'" % arg)
                        exit(1)
        args = args[1:]

    phrase = ' '.join(args).upper()

    if options["spaces"]:
        phrase = ' '.join(tuple(phrase)) + " "

    if options["square"]:
        draw_square(phrase)
    elif options["box"]:
        draw_box(phrase)
    else:
        draw_corner(phrase)

