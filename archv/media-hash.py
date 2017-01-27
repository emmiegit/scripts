#!/usr/bin/python2
from __future__ import print_function, with_statement
import hashlib, os, re, sys, traceback, time

ASK_FOR_CONFIRMATION = True
DRY_RUN = False
MEDIA_TYPES = (
    'png',
    'jpg',
    'jpeg',
    'gif',
    'tif',
    'tiff',
    'bmp',
    'svg',
    'webm',
    'wmv',
    'mp4',
    'mkv',
    'm4a',
    'mp3',
    'ogg',
    'opus',
    'aac',
)

def confirmation(fn):
    global ASK_FOR_CONFIRMATION
    if ASK_FOR_CONFIRMATION:
        response = raw_input("Would you like to delete \"%s\"?\n[Y/n/a/q] " % fn).lower()

        if response in ("always", "a"):
            ASK_FOR_CONFIRMATION = False
            return True
        elif response in ("quit", "stop", "q"):
            print("Stopping hashing...")
            exit(1)
        else:
            return response in ("yes", "y", "")
    else:
        return True

def get_hash(fn):
    with open(fn, 'rb') as fh:
       return hashlib.sha1(fh.read()).hexdigest()

def is_media(fn):
    for ext in MEDIA_TYPES:
        if fn.lower().endswith(".%s" % ext):
            return True
    return False

def wildcard_to_regex(pattern):
    return re.escape(pattern).replace('\\*', '.*').replace('\\?', '.?') + '$'

def dirify(folder):
    if not folder.endswith(os.path.sep):
        return folder + os.path.sep
    else:
        return folder

def transform_file_ext(ext):
    return ext.lower().replace('jpeg', 'jpg')

def matches(pattern, string):
    return bool(re.search(wildcard_to_regex(pattern), string))

def log(string, perm=False):
    if perm:
        log.line_length = 0
        if log.needs_newline:
            print("\n%s" % string)
        else:
            print(string)
    else:
        if log.line_length:
            print("\r%s\r" % (' ' * log.line_length), end='')
        print(string, end='')
        log.line_length = len(string)
        sys.stdout.flush()
    log.needs_newline = not perm

log.line_length = 0
log.needs_newline = False

def get_ignored_files(path, ignore, ignoredirs):
    global errors

    try:
        with open(path, 'r') as fh:
            for line in fh.readlines():
                line = line.strip()
                if not line.startswith('#'):
                    if line.endswith(os.sep):
                        ignoredirs.add(os.path.dirname(path) + os.sep + line)
                    else:
                        ignore.add(os.path.dirname(path) + os.sep + line)
    except KeyboardInterrupt:
        exit(1)
    except SystemExit:
        exit(1)
    except:
        log("Error reading %s, skipping directory for safety." % path, True)
        errors += 1
        traceback.print_exc(None, err_fh)
        ignoredirs.add(path)
    finally:
        log("Got %d pattern%s from %s" % (len(ignore) + len(ignoredirs), ('s' if (len(ignore) + len(ignoredirs) - 1) else ''), path), True)


def hash_media(dir_to_explore, err_fh, pause=False):
    if not os.path.isdir(dir_to_explore):
        log("\"%s\" is not a directory." % dir_to_explore, True)
        return 1

    global errors
    start_time = time.time()
    old_files_fn = "%s/hash-renamed-files.txt" % dir_to_explore
    try:
        last_mtime = os.stat(old_files_fn).st_mtime
    except:
        last_mtime = 0
    old_files_fh = open(old_files_fn, 'a')

    changed = 0
    errors = 0
    ignoredirs = set()
    allfiles = {}

    os.chdir(dir_to_explore)

    if DRY_RUN:
        log("NOTE: This is a dry run, no files will be changed.")

    for cd, subdirs, files in os.walk(dir_to_explore):
        ignorethis = False
        _dir = dirify(cd)

        for pattern in ignoredirs:
            if matches(pattern, _dir):
                log("Ignoring %s..." % _dir)
                ignorethis = True
                break

        if ignorethis:
            continue

        cd = dirify(os.path.abspath(cd))
        log("Processing \"%s\" (%d files)..." % (_dir, len(files)))
        del _dir, ignorethis

        ignore = set()

        # Added "_ignore" for Windows users, just like "_vimrc".
        for _fn in (".ignore", "_ignore"):
            if _fn in files and os.path.exists(cd + _fn):
                get_ignored_files(cd + _fn, ignore, ignoredirs)
        del _fn

        if cd + "*" in ignore:
            continue

        for fn in files:
            if not is_media(fn):
                continue

            abs_fn = cd + fn

            for pattern in ignore:
                if matches(pattern, abs_fn):
                    continue

            try:
                if os.stat(abs_fn).st_ctime < last_mtime:
                    continue
            except:
                log("Skipping over \"%s\"." % fn, True)
                continue

            try:
                hashsum = get_hash(abs_fn)
            except KeyboardInterrupt:
                exit(1)
            except SystemExit:
                exit(1)
            except:
                log("Unable to calculate hash for \"%s\"." % fn, True)
                errors += 1
                traceback.print_exc(None, err_fh)
                continue

            new_fn = "%s.%s" % (hashsum, transform_file_ext(fn.split('.')[-1]))
            abs_new_fn = cd + new_fn

            if abs_fn != abs_new_fn:
                try:
                    if os.path.exists(abs_new_fn):
                        log("Found collision for \"%s\": removing \"%s\"..." % (new_fn, fn), True)
                        try:
                            if not DRY_RUN and confirmation(abs_fn):
                                os.remove(abs_fn)
                                old_files_fh.write("\"%s\" deleted.\n" % (abs_fn,))
                            changed += 1
                            continue
                        except KeyboardInterrupt:
                            exit(1)
                        except SystemExit:
                            exit(1)
                        except:
                            log("Unable to remove \"%s\"." % (fn,), True)
                            errors += 1
                            traceback.print_exc(None, err_fh)
                    else:
                        log("Renaming \"%s\" -> \"%s\"." % (abs_fn, abs_new_fn), True)
                        if not DRY_RUN:
                            os.rename(abs_fn, abs_new_fn)
                            old_files_fh.write("\"%s\" -> \"%s\"\n" % (abs_fn, abs_new_fn))
                        changed += 1
                except KeyboardInterrupt:
                    exit(1)
                except SystemExit:
                    exit(1)
                except:
                    log("Unable to rename \"%s\"." % fn, True)
                    traceback.print_exc(None, err_fh)
                    errors += 1

          # if new_fn in allfiles.keys():
          #     print("Found collision for \"%s\" at \"%s\"..." % (new_fn, cd))
          #     print("(Original at \"%s\")" % (allfiles[new_fn],))
          #     try:
          #         if not DRY_RUN and confirmation(abs_new_fn):
          #             os.remove(abs_new_fn)
          #             old_files_fh.write("\"%s\" deleted\n" % (abs_fn,))
          #         changed += 1
          #         continue
          #     except:
          #         log("Unable to remove \"%s\"." % (fn,), True)
          #         errors += 1
          #         traceback.print_exc(None, err_fh)
          # else:
          #     allfiles[new_fn] = cd

    log("Done: %d files changed with %d errors in %.2f seconds." % (changed, errors, time.time() - start_time))

    if pause:
        raw_input("Press enter to continue: ")
        print("\r                        \r", end='')

    return errors

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: %s [target-directory]..." % (sys.argv[0].split(os.sep)[-1]))
            print("Only these file extensions will be affected: %s" % (' '.join(MEDIA_TYPES)))
            print("Place .ignore files in directories with lists of files for this program to leave as-is.")
            exit(0)
        if not os.path.exists(sys.argv[1]) or not os.path.isdir(sys.argv[1]):
            print("No such directory exists: \"%s\"" % sys.argv[1])
            exit(1)
        errors = 0
        with open("%s/hash-errors.txt" % (os.path.dirname(sys.argv[0])), 'a+') as err_fh:
            for path in sys.argv[1:]:
                errors += hash_media(path, err_fh)
        exit()
    else:
       print("Usage: %s [directory]." % (os.path.basename(sys.argv[0])))
       exit(1)

