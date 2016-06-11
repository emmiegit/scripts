#!/usr/bin/env python3
import codecs
import hashlib
import itertools
import os
import pickle
import sys

FILE_TREE_FILE_NAME = "filetree.pickle"


def get_file_tree():
    filetree = {}
    for root, dirs, files in os.walk(sys.argv[1], followlinks=True):
        for fn in files:
            try:
                with open(fn, "rb") as fh:
                    hashsum = hashlib.md5(codecs.encode(fh.read(), "hex_codec")).digest()
                filetree[os.path.join(root, fn)] = hashsum
            except IOError as err:
                print("Unable to get checksum of \"%s\": %s." % (fn, err))

    return filetree


def compare_file_trees(old_tree, new_tree):
    created_files = []
    removed_files = []
    changed_files = []

    for fn in set(itertools.chain(old_tree.keys(), new_tree.keys())):
        was_present = fn in old_tree.keys()
        is_present = fn in new_tree.keys()

        if not was_present and is_present:
            created_files.append(fn)
        elif was_present and not is_present:
            removed_files.append(fn)
        elif old_tree[fn] != new_tree[fn]:
            changed_files.append(fn)

    return created_files, removed_files, changed_files


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: %s directory" % sys.argv[0])
        exit(1)

    filetree = get_file_tree()

    if os.path.exists(FILE_TREE_FILE_NAME):
        with open(FILE_TREE_FILE_NAME, "rb") as fh:
            oldfiletree = pickle.load(fh)

        created, removed, changed = compare_file_trees(oldfiletree, filetree)

        for fn in created:
            print("+ %s" % fn)
        for fn in removed:
            print("- %s" % fn)
        for fn in changed:
            print("~ %s" % fn)

    with open(FILE_TREE_FILE_NAME, "wb") as fh:
        pickle.dump(filetree, fh)

