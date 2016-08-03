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

class method_dialog:

    def find(self):
        self.parent_obj.find_one(str(self.var1.get()))

    def end(self):
        self.parent_obj.reset_counters()
        self.find_string = '!!END!!'
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.parent_obj = parent_obj

        self.function_list = []

        index = self.parent_obj.n.tabs().index(self.parent_obj.n.select())
        ed = self.parent_obj.eds[index]

        ed.return_function_names(self)

        self.textFrame = Frame(top)

        lst1 = self.function_list
        self.var1 = StringVar()
        self.dropdown = OptionMenu(self.textFrame, self.var1, *lst1)
        self.dropdown.pack()

        self.textFrame.pack()

        self.button = Button(top, text="Find Function", command=self.find)
        self.button.pack()

        self.button4 = Button(top, text="Cancel", command=self.end)
        self.button4.pack()

        self.parent_obj = parent_obj
