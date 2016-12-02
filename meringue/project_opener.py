#import everthing
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

class project_opener:

    def open(self):

        string = str(self.var1.get())
        index = self.projects.index(string)

        self.parent_obj.open_folder(self.paths[index])
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        #create the gui

        top = self.top = Toplevel(parent)

        self.parent_obj = parent_obj

        self.projects = []
        self.paths = []

        with open(self.parent_obj.meringue_path + '/data/projects.txt', 'r') as f_in:
            data = f_in.read()
            lines = data.split('\n')
            for line in lines:
                dat = line.split(';')
                if len(dat) > 1:
                    self.projects.append(dat[0])
                    self.paths.append(dat[1])

        self.textFrame = Frame(top)

        #Create out dropdown box for the user to select a variable to change

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Project Name:"
        self.entryLabel.grid(row=0, column=0, sticky=E+W)

        lst1 = self.projects
        self.var1 = StringVar()
        if len(self.projects) > 0:
            self.var1.set(self.projects[0])
        self.dropdown = OptionMenu(self.textFrame, self.var1, *lst1)
        self.dropdown.grid(row=1, column=0, sticky=E+W)
        self.dropdown['width'] = 50

        self.textFrame.pack()

        self.button = Button(self.textFrame, text="Open", command=self.open)
        self.button.grid(row=2, column=0, sticky=E+W)

        self.button4 = Button(self.textFrame, text="Cancel", command=self.cancel)
        self.button4.grid(row=3, column=0, sticky=E+W)

        self.parent_obj = parent_obj
