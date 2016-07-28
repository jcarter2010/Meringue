# Merengue
A Raspberry Pi/Linux/Windows (even though it looks pretty ugly on Windows)/Mac (maybe? I haven't tested it yet) Text Editor

Keep in mind, this is still in its very early stages and very much a work in progress.  There will be a lot of bugs, just giving you fair warning.

In order to run this, download the repository as a .zip and put it wherever you want it.  After doing that just unzip it to the directory where you want to keep it, then open up a terminal window and type:

  python merengue.py

Theoretically it should work for both python2 and python3, so it doesn't matter which one you use to run it.

The first time you run it, it will ask you for the default directory to open with a directory selection dialog.  Just pick whichever directory you like (preferably one that doesn't have a ton of folder s and files because then it will take absolutely ages to load up).

After this, every time open Merengue it will open up to that directory.  I'm still working on the ability to change the directory (at the moment Python is being a butt) so if you want to change it just go into the config.ini file and delete everythin after 'folder=' which will cause it to prompt you for the folder on startup again.
