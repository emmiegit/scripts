#!/usr/bin/env python3
from getpass import getpass
import atexit
import json
import os
import shutil
import signal
import subprocess
import sys

try:
    import ft_diff
except ImporError:
    print("Cannot find file tree difference library ft_diff.", file=sys.stderr)
    exit(1)


def handle_signal(signum, frame):
    clean_up(1)


def clean_up():
    if lock_file:
        os.unlink(lock_file)


def sanity_test_config(config):
    success = True

    if "archive-directory" not in config.keys():
        print("Key \"archive-directory\" not specified in config file.", file=sys.stderr)
        success = False
    elif not os.path.isdir(os.path.expanduser(config["archive-directory"])):
        print("Specified archive directory does not exist: %s" % config["archive-directory"], file=sys.stderr)
        success = False

    if "lock-file" not in config.keys():
        print("Key \"lock-file\" not found, using default.", file=sys.stderr)
        config["lock-file"] = ".%s.lock"

    if "hash-script" not in config.keys():
        print("Key \"hash-script\" not specified in config file.", file=sys.stderr)
        success = False

    if "back-up-old-archive" not in config.keys() or type(config["back-up-old-archive"]) != bool:
        print("Key \"back-up-old-archive\" not found or invalid, backing up archive anyways.", file=sys.stderr)
        config["back-up-old-archive"] = True

    if "clear-recent" not in config.keys() or type(config["clear-recent"]) != bool:
        print("Key \"clear-recent\" not found or invalid, not clearing recent files.", file=sys.stderr)
        config["clear-recent"] = False

    if "test-archive" not in config.keys() or type(config["test-archive"]) != bool:
        print("Key \"test-archive\" not found or invalid, not testing archive.", file=sys.stderr)
        config["test-archive"] = True

    config["archive-directory"] = os.path.expanduser(config["archive-directory"])
    config["hash-script"] = os.path.expanduser(config["hash-script"])
    config["archive-file"] = os.path.join(config["archive-directory"], name + ".7z")

    return success


def clear_recent_documents():
    print("Clearing recent documents...")
    with open(os.path.expanduser("~/.local/share/recently-used.xbel"), "w") as fh:
        pass

    print("Clearing thumbnails...")
    if os.path.isdir(os.path.expanduser("~/.thumbnails")):
        for fn in glob.glob(os.path.expanduser("~/.thumbnails/normal/*")):
            os.unlink(fn)
        for fn in glob.glob(os.path.expanduser("~/.thumbnails/large/*")):
            os.unlink(fn)
    else:
        for fn in glob.glob(os.path.expanduser("~/.cache/thumbnails/normal/*")):
            os.unlink(fn)
        for fn in glob.glob(os.path.expanduser("~/.cache/thumbnails/large/*")):
            os.unlink(fn)


def add_files(name, archive_dir, created, config, passwd, icon="+"):
    created_list = []

    for fn in created:
        print("%s %s" % (icon, fn))
        created_list.append(os.path.join(name, os.path.basename(fn)))

    if not created_list:
        print("Warn: files to add is empty")
        return

    arguments = ["7z", "a", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"]]
    subprocess.Popen(arguments + created_list, stdout=subprocess.DEVNULL)
    print("Command: %s" % (arguments + created_list))


def remove_files(name, archive_dir, removed, config, passwd):
    removed_list = []

    for fn in removed:
        print("- %s" % fn)
        removed_list.append(os.path.join(name, os.path.basename(fn)))

    if not removed_list:
        print("Warn: files to remove is empty")
        return

    arguments = ["7z", "d", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"]]
    subprocess.Popen(arguments + removed_list, stdout=subprocess.DEVNULL)
    print("Command: %s" % (arguments + removed_list))


def create_archive(name, archive_dir, config, passwd):
    print("[New archive]")
    while True:
        passwd = getpass("Password: ")
        passwd2 = getpass("Password again: ")

        if passwd != passwd2:
            print("Passwords do not match.")
        else:
            break

    print("Hashing images...")
    subprocess.run([config["hash-script"], archive_dir])
    print("Adding files...")
    subprocess.run(["7z", "a", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"], archive_dir])
    print("Removing old files...")
    #shutil.rmtree(archive_dir)
    if config["clear-recent"]:
        clear_recent_documents()


def compress_archive(name, archive_dir, config):
    print("[Compressing]")
    passwd = getpass("Password: ")
    print("Hashing images...")
    subprocess.run([config["hash-script"], archive_dir])
    print("Checking file diff...")
    created, removed, changed = ft_diff.get_changed_files(archive_dir)
    print("Backing up old archive...")
    shutil.copy2(config["archive-file"], config["archive-file"] + "~")
    if created:
        print("Adding new files...")
        add_files(name, archive_dir, created, config, passwd)
    if removed:
        print("Removing deleted files...")
        remove_files(name, archive_dir, removed, config, passwd)
    if changed:
        print("Changing modified files...")
        add_files(name, archive_dir, changed, config, passwd, icon="~")
    if not (created or removed or changed):
        print("Note: no changes to archive.")
    if config["test-archive"]:
        print("Testing archive...")
        subprocess.run(["7z", "t", "-p%s" % passwd, config["archive-file"]])
    print("Removing old files...")
    #shutil.rmtree(archive_dir)
    if config["clear-recent"]:
        clear_recent_documents()


def extract_archive(name, archive_dir, config):
    print("[Extracting]")
    passwd = getpass("Password: ")
    subprocess.run(["7z", "x", "-p%s" % passwd, config["archive-file"]])


if __name__ == "__main__":
    global lock_file
    lock_file = None

    atexit.register(clean_up)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGHUP, handle_signal)

    if len(sys.argv) < 2:
        name = input("Which archive would you like to access? ")
    else:
        name = sys.argv[1]

    if len(sys.argv) < 3:
        config_file = "/usr/local/scripts/dat/varch.json"
    else:
        config_file = sys.argv[2]

    with open(config_file, "r") as fh:
        config = json.load(fh)

    if not sanity_test_config(config):
        exit(1)

    lock_file = os.path.join(config["archive-directory"], config["lock-file"] % name)

    if os.path.exists(lock_file):
        print("This archive is being processed by another process.")
        exit(1)

    with open(lock_file, "w") as fh:
        pass

    archive_extracted_dir = os.path.join(config["archive-directory"], name)

    if os.path.isdir(archive_extracted_dir):
        if not os.path.isfile(config["archive-file"]):
            create_archive(name, archive_extracted_dir, config)
        else:
            compress_archive(name, archive_extracted_dir, config)
    elif not os.path.isfile(config["archive-file"]):
        print("[Error]")
        print("Cannot find archive at \"%s\".", config["archive_file"])
        clean_up()
        exit(1)
    else:
        extract_archive(name, archive_extracted_dir, config)

