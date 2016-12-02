#import stuff
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

class find_and_replace_dialog:

    #tell the parent to find all instances of the item the user typed in
    def find(self):
        self.parent_obj.find(self.entryWidget.get())

    #tell the parent to find one instance of the item the user typed in
    def find_one(self):
        self.parent_obj.find_one(self.entryWidget.get())

    #tell the parent to replace items
    def replace(self):
        self.parent_obj.replace(self.entryWidget.get(), self.entryWidget2.get())

    #tell the parent to replace all instances of the items
    def replace_all(self):
        self.parent_obj.replace_all(self.entryWidget.get(), self.entryWidget2.get())

    def end(self):
        self.parent_obj.reset_counters()
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        #create all the gui -- see access_ssh.py and change_color.py for a explanation

        top = self.top = Toplevel(parent)

        self.textFrame = Frame(top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Find:"
        self.entryLabel["width"] = 20
        self.entryLabel.grid(row=0, column=0)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.grid(row=0, column=1)
        self.entryWidget.focus_set()

        self.entryLabel2 = Label(self.textFrame)
        self.entryLabel2["text"] = "Replace:"
        self.entryLabel2.grid(row=1, column=0)

        self.entryWidget2 = Entry(self.textFrame)
        self.entryWidget2["width"] = 50
        self.entryWidget2.grid(row=1, column=1)

        self.textFrame.grid()

        self.button = Button(self.textFrame, text="Find All", command=self.find)
        self.button.grid(row=2, column=0, columnspan=2, sticky=E+W)

        self.button1 = Button(self.textFrame, text="Find Next", command=self.find_one)
        self.button1.grid(row=3, column=0, columnspan=2, sticky=E+W)

        self.button2 = Button(self.textFrame, text="Replace", command=self.replace)
        self.button2.grid(row=4, column=0, columnspan=2, sticky=E+W)

        self.button3 = Button(self.textFrame, text="Replace All", command=self.replace_all)
        self.button3.grid(row=5, column=0, columnspan=2, sticky=E+W)

        self.button4 = Button(self.textFrame, text="Done", command=self.end)
        self.button4.grid(row=6, column=0, columnspan=2, sticky=E+W)

        self.parent_obj = parent_obj
