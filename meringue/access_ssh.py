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

class access_ssh:

    def connect(self):
        #Get the parameters for ssh and sftp from the user dialog
        username = self.entryWidget.get()
        host = self.entryWidget2.get()
        password = self.entryWidget3.get()
        port = self.entryWidget4.get()

        self.parent_obj.username = username
        self.parent_obj.ip = host
        self.parent_obj.password = password
        self.parent_obj.port = port

        self.top.destroy()

    def cancel(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.textFrame = Frame(top)

        #Labels and entry boxes to describe user input and capture it

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Username:"
        self.entryLabel['width'] = 20
        self.entryLabel.grid(row=0, column=0)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.grid(row=0, column=1)

        self.entryLabel2 = Label(self.textFrame)
        self.entryLabel2["text"] = "IP Address/Hostname:"
        self.entryLabel2.grid(row=1, column=0)

        self.entryWidget2 = Entry(self.textFrame)
        self.entryWidget2["width"] = 50
        self.entryWidget2.grid(row=1, column=1)

        self.entryLabel3 = Label(self.textFrame)
        self.entryLabel3["text"] = "Password:"
        self.entryLabel3.grid(row=2, column=0)

        self.entryWidget3 = Entry(self.textFrame, show='*')
        self.entryWidget3["width"] = 50
        self.entryWidget3.grid(row=2, column=1)

        self.entryLabel4 = Label(self.textFrame)
        self.entryLabel4["text"] = "Port:"
        self.entryLabel4.grid(row=3, column=0)

        self.entryWidget4 = Entry(self.textFrame)
        self.entryWidget4["width"] = 50
        self.entryWidget4.grid(row=3, column=1)

        #Set focus to the top box so they don't have to go over and click on it

        self.entryWidget.focus_set()

        self.textFrame.grid()

        #Add the necessary buttons

        self.button = Button(self.textFrame, text="Connect", command=self.connect)
        self.button.grid(row=4, column=0, columnspan=2, sticky=E+W)

        self.button2 = Button(self.textFrame, text='Done', command=self.cancel)
        self.button2.grid(row=5, column=0, columnspan=2, sticky=E+W)

        self.parent_obj = parent_obj
