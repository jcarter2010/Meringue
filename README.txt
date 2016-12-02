# Merengue #

## Written by John Carter ##
###### Last updated 12/02/2016 ######

----------------

A Raspberry Pi Linux Windows and OS X text editor

----------------

ABOUT

----------------

  This works on Windows now! Well, at least Windows 10, that's all I've tested it on.  You can even connect to a Raspberry Pi and edit its files remotely.  It just looks incredibly ugly.  Linux looks much much better, so go with Linux.  Also, a few versions ago it kind of worked on OS X, so if you want to try running it on that go ahead and please tell me about any bugs and how it runs.

  Keep in mind, this is still in its very early stages and very much a work in progress.  There will be a lot of bugs, just giving you fair warning.

  In order to run this, download the repository as a .zip and put it wherever you want it.  After doing that just unzip it to the directory where you want to keep it, then open up a terminal window within the 'meringue' directory and type:

    python2 meringue.py

  Don't use the setup.py script.  I am still testing that and it doesn't work whatsoever, so just ignore it.

  The first time you run it, it will ask you for the default directory to open with a directory selection dialog.  Just pick whichever directory you like (preferably one that doesn't have a ton of folders and files because then it will take absolutely ages to load up).

  After this, every time open Merengue it will open up to that directory.
  You can change this folder by going to 'file > open folder'

----------------

Commands:

----------------

  + [ctrl]+[f] is find and replace

  + [ctrl]-[q] is variable highlighting.
    Select whichever variable you want by click and drag (or double click) and then press the key combo and it will highlight all instances of the variable in your current tab that is open.

  + [ctrl]-[h] is to connect to a remote Linux machine.

  + [ctrl]-[r] is to refresh the syntax highlighting
    Current syntax highlighting supported:
      * Python
      * PlainText
      * Html/Javascript
      * Xml
      * Html/Php
      * Perl6
      * Ruby
      * Ini/Init
      * Apache 'Conf'
      * Bash Scripts
      * Diffs
      * C#
      * MySql


  + Double click on the files in the directory tree on the left hand side to open them
    Right click on them to pull up a menu of actions that you can take such as delete, rename, copy, paste, create a new file, and create a new folder.

  + Double click on the tab in the file you are working on to change its name.

  + Click 'edit > Change Editor Colors' it will give you a dropdown box with all of the color variables for the program.
    Select one and then hit 'select color' and it will give you a way to select a new color for the element in order to customize your text editing experience.

  + Right click on a tab to close it

----------------

If anyone has any suggestions as to what I should add, email me at jcarter2010@comcast.net

-----------------

REQUIREMENTS:

-----------------

  + Paramiko

  + Pygments

-----------------

TO DO:

-----------------

  + Fix adding tabs to multiple lines

  + go to line

  + more color customizations (for example, escape sequences, chars etc.)

  + fix project manager
