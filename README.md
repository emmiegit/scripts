# scripts
A collection of scripts and other utilities I have written for my personal usage. All files are copyrighted under the MIT license as specified in `LICENSE` unless otherwise specified. The scripts in this directory invoke other resources in this repo via `/usr/local/scripts` or `~/Scripts`.

## Directory hiearchy
`apps` - Contains scripts to start certain applications or other processes on my computer.
`arch` - Scripts related to the archiving of files on my computer for long-term storage.
`dat` - Contains data to be used by scripts. Private or encrypted data will not be present.
`fun` - Scripts that don't serve any real purpose, and are just for fun.
`sbin` - Scripts that require root access.
`wip` - Scripts that are not complete, do not function properly, or are experimental. Do not expect anything in here to work.
`wm` - Scripts used by bindings (such as media keys) or by my window manager directly. See my dotfiles repo for more information.

## Script summaries
### Top level

#### charge-shutdown.py
A Windows script (for Cygwin) to predict the time needed to charge my phone, and turn off my computer then to prevent overcharging.

#### check-args.sh [<i>anything you want here</i>...]
Prints out all the arguments recieved by the script. Used for making debugging scripts by making sure you're passing arguments the way you think you are.

#### chperms.sh
Makes all `*.py` and `*.sh` files executable. Provides a function called `chperms`.

#### common-password.sh
Determines if your password is one of the most common 10,000 passwords. (If it is, change it immediately, it's a big security hazard for you)

#### detect-logitech-g710.sh
Determine if the interface directory provided by Wattos' Logitech G710+ driver is present or not.

#### fssync.sh
Provides a function called `fssync` that basically acts like rsync, but in both directions.

#### has-dependencies.sh <i>packge-name</i>...
Looks for the given packages on your system. By default, uses the pacman package manager for Arch Linux, though this can be easily changed.

#### hashsum.py <i>algorithm</i> <i>file-name</i>...
Allows hashing of whatever hash algorithms are supported by Python.

#### mkdesktop.sh [<i>desktop-file-name</i>] [<i>destination-directory</i>]
Makes a desktop file from the template in `dat/`. You can choose where you want it, though by default it goes to `~/Desktop`.

#### mouse-sensitivity.sh
Disables mouse acceleration under X. You may want to fiddle with the `Device Accel Constant Deceleration` value to get a mouse movement rate you like.

#### package.sh
Creates archives of the given directories to back them up by providing a function called `pack`.

#### parse-xml.sh
Takes piped input with XML data and either prints it in a `key:value` format or, if arguments are given, only prints the pairs for the given keys.

#### remove-duplicates.sh
Invokes `arch/hash-media.py` on the directories specified in the `$LOCATIONS` variable (inside the script).

#### sample-files.py <i>source-directory</i> <i>output-directory</i> <i>numebr-of-copies</i>
Randomly copies a user-specified number of files from a directory to another directory, named sequentially.

#### set-mime-type-defaults.sh <i>mime-type-regular-expression</i>...
Makes it easier to set lots of mime types via `xdg-mime` by specifying a regular expression that the mime types follow, and setting the default application to run them one at a time. Empty lines are left as-is, and the `.desktop` extension is added automatically and therefore unneeded.

#### trim-whitespace.sh
Provides a function called `trim_whitespace` that takes the first argument and removes any leading or trailing whitespace.

#### tryeditor.sh [<i>editor-to-try</i>]
Opens up the editor specified by the passed arguments, `$VISUAL`, `$EDITOR`, and then `vi` (in that order), to open a copy of Shakespeare's Hamlet to edit. When you are done, no changes to the original file are preserved, even if you save and quit.

#### update-all-git-repos.sh [<i>directory-of-git-repos</i>]
Checks all git repositories either in the current working directory or in the directory passed to it and determines whether they are ahead or behind. If they are behind, it automatically invokes `git pull --all` and `git gc --aggressive`.

#### vim-keyswap.sh
I have swapped my caps lock and escape keys since caps lock is a useless key and, as a vim user, I use escape all the time. This scripts will check if the keys are already swapped, and if not, invoke `xmodmap` to switch them.

### apps
This directory is pretty self-explanatory, and is pretty specific to my machine anyways. The only file that might be of interest is `gvim.sh`, which makes it so that opening files with Gvim create new tabs if Gvim is already running.

### arch
(todo)

#### hash-media.py <i>directory</i>...
Walks through a directory recursively and removes exact duplicates by renaming media files with their SHA1 hashsum. This program will read any `.ignore` files and will not rename any files specified inside.

#### varch.sh <i>destination-directory</i> [<i>password-file</i>] [<i>hash-script-location</i>]
Compresses or extracts an encrypted archive, removing exact duplicates and renaming certain file types via `hash-media.py`. Checks the password agains `dat/.archpasswd` to prevent typos. You can set your password by using the following:
```
echo your_password_here | sha1sum > dat/.archpasswd
```

#### dat
(todo)

#### fun
(todo)

#### sbin
(todo)

#### empty-cache.sh
Clears the I/O cache from the RAM. Note that this will slightly worsen I/O performance until the cache is rebuilt. I wrote it because I didn't like seeing my ram filled up.

#### wip
(todo)

#### wm
(todo)

