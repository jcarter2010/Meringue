try:
    from Tkinter import *
    import Tkinter as tk
    import tkMessageBox
except:
    from tkinter import *
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox

class open_file_dialog:

    def open_file(self):

        #attempt to get the parent to open a file, if it fails tell the user

        try:
            print(self.entryWidget.get())
            self.parent_obj.open_file(self.entryWidget.get())
        except:
            tkMessageBox.showwarning("Open Error", "File does not exist")

        self.top.destroy()

    def end(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj, parent_path):

        #create the gui

        self.top = Toplevel(parent)

        self.parent_obj = parent_obj

        self.top.title("Open File")
        self.top["padx"] = 40
        self.top["pady"] = 20

        self.textFrame = Frame(self.top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "File to open:"
        self.entryLabel.pack(side=LEFT)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.insert(0, parent_path + '/')
        self.entryWidget.pack(side=LEFT)
        self.entryWidget.focus_set()

        self.textFrame.pack()

        self.button = Button(self.top, text="Open", command=self.open_file)
        self.button.pack()

        self.button2 = Button(self.top, text="Cancel", command=self.end)
        self.button2.pack()
