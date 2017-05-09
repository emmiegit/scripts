#!/usr/bin/env python
from __future__ import print_function, with_statement
import os

PROCFS = '/proc'

class OOMScore(object):
    def __init__(self, name):
        self.pid = int(name)
        self.name = name
        self.score = get_oom_score(name)
        self.exe = get_exe(name)

    def __lt__(self, other):
        return self.score < other.score
    def __gt__(self, other):
        return self.score > other.score
    def __le__(self, other):
        return self.score <= other.score
    def __ge__(self, other):
        return self.score >= other.score
    def __eq__(self, other):
        return self.pid == other.pid
    def __ne__(self, other):
        return not(self == other)
    def __nonzero__(self):
        return bool(self.score)
    __bool__ = __nonzero__
    def __str__(self):
        return "%d -- (%d) %s" % (self.score, self.pid, self.exe)

def get_oom_score(name):
    with open(os.path.join(PROCFS, name, 'oom_score')) as fh:
        score = int(fh.read())
    return score

def get_exe(name):
    try:
        return os.readlink(os.path.join(PROCFS, name, 'exe'))
    except:
        return ''

def get_oom_scores():
    scores = []
    for name in os.listdir(PROCFS):
        if not name.isdigit():
            continue
        scores.append(OOMScore(name))
    return scores

def print_worst(scores):
    for score in reversed(sorted(scores)):
        if score:
            print(score)

if __name__ == '__main__':
    scores = get_oom_scores()
    print_worst(scores)

