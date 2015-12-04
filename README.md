# scripts
A collection of scripts and other utilities I have written for my personal usage.

#### backup.sh
A simple script to use Duplicity to create encrypted incremental backups since Deja-dup is a broken mess. You need to install and configure `duply`. This script makes it possible to automate backups by adding this script to a cron job, as well as automatically adding/removing your password from the config file. (Since storing passwords in plaintext is insecure). You can set your password by hashing it: `echo your_salt_here-your_password_here | sha256sum > .bakpasswd'

#### charge_shutdown.py
A Windows script to predict the time needed to charge my phone, and turn off my computer then to prevent overcharging.

#### empty_cache.sh
Clears the I/O cache from the RAM. Requires sudo access.

#### findapp.py
A python file to look in the `/usr/share/applications/` directory used by some WMs to store `.desktop` files by application name.

#### hash_media.py <i>directories...</i>
Walks through a directory recursively and removes exact duplicates by renaming media files to their SHA1 sum.

#### hashsum.py <i>algorithm</i> <i>files...</i>
Finds the hashsums of files in the absense of commands like `md5sum`.

#### mkdesktop.sh <i>[desktop-file-name]</i> <i>[destination]</i>
Creates and opens a `.desktop` file with the specified name on the desktop.

#### package.sh
Defines a source-able `pack` function which creates a `.rar` file from the specified directory. Alternatively, you can specify certain `pack` targets within the script and make it an executable instead of a library.

#### sample_files.py <i>source-directory</i> <i>output-directory</i> <i>number-of-file</i>
Randomly samples some files from a directory and copies them to another directory. The copies will be numbered starting from zero.

#### tryedit.sh <i>[file-to-edit]</i>
Opens up your `$EDITOR` to allow you to play around with a file. When you are done, no changes to the original file are preserved, even if you save and quit. The default file is `.hamlet`.

#### varch.sh <i>destination-directory</i> <i>[password-file]</i> <i>[hash-script]</i>
Compressing/extracting an encrypted archive, removing duplicates and renaming files using `hash_media.py`. Checks the password against `.passwd` to prevent typos. You can create a new password using the following command:
```bash
echo your_password_here | sha1sum > .passwd
```
