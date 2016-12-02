from Tkinter import *
import Tkinter as tk
import tkMessageBox
import tkFileDialog

class open_file_dialog:

    def open_file(self):

        #attempt to get the parent to open a file, if it fails tell the user

        try:
            print(self.file)
            self.parent_obj.open_file(self.file)
        except:
            pass

    def __init__(self, parent, parent_obj, parent_path):
        self.parent_obj = parent_obj

        self.file = tkFileDialog.askopenfilename()

        self.open_file()
