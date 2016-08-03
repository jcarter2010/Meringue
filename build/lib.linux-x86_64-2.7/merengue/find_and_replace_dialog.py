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

    def find(self):
        self.parent_obj.find(self.entryWidget.get())

    def find_one(self):
        self.parent_obj.find_one(self.entryWidget.get())

    def replace(self):
        self.parent_obj.replace(self.entryWidget.get(), self.entryWidget2.get())

    def replace_all(self):
        self.parent_obj.replace_all(self.entryWidget.get(), self.entryWidget2.get())

    def end(self):
        self.parent_obj.reset_counters()
        self.find_string = '!!END!!'
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.textFrame = Frame(top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Find:"
        self.entryLabel.pack()

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.pack()
        self.entryWidget.focus_set()

        self.entryLabel2 = Label(self.textFrame)
        self.entryLabel2["text"] = "Replace:"
        self.entryLabel2.pack()

        self.entryWidget2 = Entry(self.textFrame)
        self.entryWidget2["width"] = 50
        self.entryWidget2.pack()

        self.textFrame.pack()

        self.button = Button(top, text="Find All", command=self.find)
        self.button.pack()

        self.button1 = Button(top, text="Find Next", command=self.find_one)
        self.button1.pack()

        self.button2 = Button(top, text="Replace", command=self.replace)
        self.button2.pack()

        self.button3 = Button(top, text="Replace All", command=self.replace_all)
        self.button3.pack()

        self.button4 = Button(top, text="Done", command=self.end)
        self.button4.pack()

        self.parent_obj = parent_obj

        #self.root.mainloop()
