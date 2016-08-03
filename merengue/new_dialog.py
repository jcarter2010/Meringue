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

class new_dialog:

    def find(self):
        self.parent_obj.new_file_func(self.entryWidget.get())
        self.top.destroy()

    def end(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.parent_obj = parent_obj

        self.function_list = []

        index = self.parent_obj.n.tabs().index(self.parent_obj.n.select())
        ed = self.parent_obj.eds[index]

        ed.return_function_names(self)

        self.textFrame = Frame(top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Name:"
        self.entryLabel.pack()
        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.pack()
        self.entryWidget.focus_set()

        self.textFrame.pack()

        self.button = Button(top, text="Create New", command=self.find)
        self.button.pack()

        self.button4 = Button(top, text="Cancel", command=self.end)
        self.button4.pack()

        self.parent_obj = parent_obj
