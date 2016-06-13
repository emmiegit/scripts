#!/usr/bin/env python3

import codecs
import glob
import hashlib
import itertools
import os
import pickle
import sys

FILE_TREE_FILE = "filetree.pickle"
FILE_TREE_IGNORE_FILE = "filetree.ignore"
DEFAULT_IGNORE_TARGETS = (
    FILE_TREE_FILE,
    FILE_TREE_IGNORE_FILE,
    "*~",
    "*.bak",
    ".*.swp",
)


def get_file_tree(directory, ignore):
    ignored = set()
    for ignore_file in ignore:
        ignored = ignored.union(glob.glob(os.path.join(directory, ignore_file), recursive=True))

    filetree = {}
    for root, dirs, files in os.walk(directory, followlinks=True):
        for fn in files:
            path = os.path.join(root, fn)
            if path in ignored:
                continue

            try:
                with open(path, "rb") as fh:
                    hashsum = hashlib.md5(codecs.encode(fh.read(), "hex_codec")).digest()
                filetree[path] = hashsum
            except IOError as err:
                print("Unable to get checksum of \"%s\": %s." % (fn, err))

    return filetree


def compare_file_trees(old_tree, new_tree, ignore):
    created_files = set()
    removed_files = set()
    changed_files = set()

    for fn in set(itertools.chain(old_tree.keys(), new_tree.keys())):
        if fn in ignore:
            continue

        was_present = fn in old_tree.keys()
        is_present = fn in new_tree.keys()

        if not was_present and is_present:
            created_files.add(fn)
        elif was_present and not is_present:
            removed_files.add(fn)
        elif old_tree[fn] != new_tree[fn]:
            changed_files.add(fn)

    return created_files, removed_files, changed_files


def get_changed_files(directory,
        tree_storage_file=FILE_TREE_FILE,
        tree_ignore_file=FILE_TREE_IGNORE_FILE):

    if os.path.exists(tree_ignore_file):
        ignore = []
        with open(tree_ignore_file, "r") as fh:
            line = fh.readline()

            while line:
                ignore.append(line.rstrip())
                line = fh.readline()
    else:
        ignore = DEFAULT_IGNORE_TARGETS
        with open(tree_ignore_file, "w") as fh:
            for ignore_file in DEFAULT_IGNORE_TARGETS:
                fh.write(ignore_file)
                fh.write("\n")

    filetree = get_file_tree(directory, ignore)

    if os.path.exists(tree_storage_file):
        with open(tree_storage_file, "rb") as fh:
            try:
                oldfiletree = pickle.load(fh)
            except:
                print("Unable to read old directory tree in \"%s\"." % tree_storage_file)
                oldfiletree = {}
    else:
        oldfiletree = {}

    return compare_file_trees(oldfiletree, filetree, ignore)


def update_file_tree(directory, filetree):
    with open(tree_storage_file, "wb") as fh:
        pickle.dump(filetree, fh)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s directory [tree-storage-filename]" % sys.argv[0])
        exit(1)

    created, removed, changed = get_changed_files(sys.argv[1])

    for fn in created:
        print("+ %s" % fn)

    for fn in removed:
        print("- %s" % fn)

    for fn in changed:
        print("~ %s" % fn)

