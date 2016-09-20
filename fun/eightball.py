#!/bin/python
from __future__ import print_function
import random
import sys

###############################
#          _......._          #
#       .-:::::::::::-.       #
#     .:::::::::::::::::.     #
#    :::::::' .-. `:::::::    #
#   :::::::  :   :  :::::::   #
#  ::::::::  :   :  ::::::::  #
#  :::::::::._`-'_.:::::::::  #
#  :::::::::' .-. `:::::::::  #
#  ::::::::  :   :  ::::::::  #
#   :::::::  :   :  :::::::   #
#    :::::::._`-'_.:::::::    #
#     `:::::::::::::::::'     #
#       `-:::::::::::-'       #
#          `'''''''`          #
###############################

try:
    input = raw_input
except NameError:
    pass

answers = (
    'It is certain.',
    'My reply is no.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes, definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    "Don't count on it.",
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.',
)

interactive_mode = (len(sys.argv) == 1)
if interactive_mode:
    print("Ask me your question.")
    input("> ")

print(random.choice(answers))

if interactive_mode:
    input()

