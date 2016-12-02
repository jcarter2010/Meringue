#import everything, some of these are not needed I believe so I need to take care of taking those out
try:
    from Tkinter import *
    import Tkinter as tk
    import ttk
    import tkFileDialog
    import tkMessageBox
    from tkFileDialog import askdirectory
except:
    from tkinter import *
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkMessageBox
    from tkinter.filedialog import askdirectory
import os
from os import listdir
from os.path import isfile, join
from os import walk
import paramiko
from remote_file_chooser import remote_file_chooser

class about_dialog:

    def close(self):
        self.top.destroy()

    def __init__(self, parent):

        self.top = Tk()

        self.textFrame = Frame(self.top)

        self.entryLabel4 = Label(self.textFrame, justify=LEFT)
        self.entryLabel4["text"] = "Welcome to the Meringue text editor.\n\nKEYBOARD SHORTCUTS\n----------------\n\
[Ctrl]-[h] -- Connect to remote machine\n\
[Ctrl]-[q] -- Highlight all instances of a selected piece of code\n\
[Ctrl]-[f] -- Find and replace dialog\n\
[Ctrl]-[e] -- Hide/display the file explorer on the side\n\
[Right Alt] -- Hide/display the menubar"
        self.entryLabel4.pack()

        self.textFrame.pack()

        #Add the necessary buttons

        self.button = Button(self.top, text="Close", command=self.close)
        self.button.pack()

        mainloop()
