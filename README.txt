Merengue

A Raspberry Pi/Linux Text Editor (Now with Python and Java syntax coloring!)

This works on Windows now! Well, at least Windows 10, that's all I've tested it on.  You can even connect to a Raspberry Pi and edit its files remotely.  It just looks incredibly ugly.  Linux looks much much better, so go with Linux.

Keep in mind, this is still in its very early stages and very much a work in progress.  There will be a lot of bugs, just giving you fair warning.

In order to run this, download the repository as a .zip and put it wherever you want it.  After doing that just unzip it to the directory where you want to keep it, then open up a terminal window and type:

  python2 meringue.py

don't use the setup.py script.  I am still testing that and it doesn't work whatsoever, so just ignore it.

The first time you run it, it will ask you for the default directory to open with a directory selection dialog.  Just pick whichever directory you like (preferably one that doesn't have a ton of folders and files because then it will take absolutely ages to load up).

After this, every time open Merengue it will open up to that directory.
You can change this folder by going to 'file > open folder'

[ctrl]+[f] is find and replace, and [ctrl]-[q] is variable highlighting.  Select whichever variable you want by click and drag (or double click) and then press the key combo and it will highlight all instances of the variable in your current tab that is open. Also, [ctrl]-[h] is to connect to a remote linux machine (be careful, this will install the 'tree' command on the remote machine in order to pull the directory structure).

You can also double click on the file (the green items) in the directory tree on the left hand side to open them. Furthermore, you can right click on them to pull up a menu of actions that you can take such as delete, rename, copy, paste, create a new file, and create a new folder.

Double click on the tab in the file you are working on to change its name.

If you click 'options > change color' it will give you a dropdown box with all of the color variables for the program.  Select one and then hit 'select color' and it will give you a way to select a new color for the element in order to customize your text editing experience.

Click the 'close tab' button to close the current open tab.

The 'about' button doesn't work yet, but I'll be putting all of this information into there after I get all of the functionality working.

If anyone has any suggestions as to what I should add, email me at jcarter2010@comcast.net

REQUIREMENTS:
	Paramiko
	ImageTk
	colorama
	
