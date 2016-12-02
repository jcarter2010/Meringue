#Import stuff
#I really should comment this better

import sys
try:
    from Tkinter import *
    import Tkinter as tk
    import ttk
except:
    from tkinter import *
    import tkinter as tk
    import tkinter.ttk as ttk
from subprocess import PIPE, Popen
from tkColorChooser import askcolor

class change_color:

    def change(self):
        #try:

        #We want a dropdown box of all of the options, so get the selected item

        string = str(self.var1.get())
        index = self.function_list.index(string)

        color = askcolor()
        out = color

        print(out)

        #Get all of the config values, set the color values for the parameter to be changed, rewrite the config to save them
        #And change all of the colors for the items in the text editor then exit the dialog

        self.read_config()
        line = self.lines[index][:self.lines[index].find('=')]
        #hex = '#%02x%02x%02x' % (int(r), int(g), int(b))
        hex_code = out[1]
        line = line + '=' + hex_code
        self.lines[index] = line
        self.write_config()
        self.parent_obj.read_config()
        self.parent_obj.change_ed_colors()
        self.top.destroy()

    def write_config(self):

        #Write all of the corresponding values to the config file to save them

        with open(self.parent_obj.meringue_path+'data/meringue_config.ini', 'w') as f_out:
            for line in self.lines:
                f_out.write(line + '\n')
            f_out.flush()

    def read_config(self):

        #read all of the values from the congfig file

        with open(self.parent_obj.meringue_path+'data/meringue_config.ini', 'r') as f_in:
            self.lines = f_in.read().split('\n')
            self.foreground = self.lines[0].split('=')[1]
            self.foreground = self.foreground[:7]
            self.background = self.lines[1].split('=')[1]
            self.background = self.background[:7]
            self.file_color = self.lines[2].split('=')[1]
            self.file_color = self.file_color[:7]
            self.dir_color = self.lines[3].split('=')[1]
            self.dir_color = self.dir_color[:7]
            self.line_num_color = self.lines[4].split('=')[1]
            self.line_num_color = self.line_num_color[:7]
            self.line_num_background_color = self.lines[5].split('=')[1]
            self.line_num_background_color = self.line_num_background_color[:7]
            self.file_bar_color = self.lines[6].split('=')[1]
            self.file_bar_color = self.file_bar_color[:7]
            self.file_bar_text_color = self.lines[7].split('=')[1]
            self.file_bar_text_color = self.file_bar_text_color[:7]
            self.notebook_background = self.lines[8].split('=')[1]
            self.notebook_background = self.notebook_background[:7]
            self.highlight_foreground = self.lines[9].split('=')[1]
            self.highlight_foreground = self.highlight_foreground[:7]
            self.highlight_background = self.lines[10].split('=')[1]
            self.highlight_background = self.highlight_background[:7]
            self.token_keyword = self.lines[11].split('=')[1]
            self.token_keyword = self.token_keyword[:7]
            self.token_name = self.lines[12].split('=')[1]
            self.token_name = self.token_name[:7]
            self.token_literal = self.lines[13].split('=')[1]
            self.token_literal = self.token_literal[:7]
            self.token_string = self.lines[14].split('=')[1]
            self.token_string = self.token_string[:7]
            self.token_number = self.lines[15].split('=')[1]
            self.token_number = self.token_number[:7]
            self.token_operators = self.lines[16].split('=')[1]
            self.token_operators = self.token_operators[:7]
            self.token_punctuation = self.lines[17].split('=')[1]
            self.token_punctuation = self.token_punctuation[:7]
            self.token_comments = self.lines[18].split('=')[1]
            self.token_comments = self.token_comments[:7]
            self.token_generic = self.lines[19].split('=')[1]
            self.token_generic = self.token_generic[:7]
            self.folder = self.lines[20].split('=')[1]

    def end(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.parent_obj = parent_obj

        #all of the possible color values to change

        self.function_list = []

        with open(self.parent_obj.meringue_path+'data/meringue_config.ini', 'r') as f_in:
            lines = f_in.read().split('\n')
            for line in lines:
                self.function_list.append(line[:line.find('=')])

        print(self.function_list)

        self.textFrame = Frame(top)

        #Create out dropdown box for the user to select a variable to change

        lst1 = self.function_list
        self.var1 = StringVar()
        self.var1.set('highlight_foreground')
        self.dropdown = OptionMenu(self.textFrame, self.var1, *lst1)
        self.dropdown.grid(row=0, column=0, sticky=E+W)
        self.dropdown['width'] = 50

        #Add the necessary buttons

        self.button = Button(self.textFrame, text="Select Color", command=self.change)
        self.button.grid(row=1, column=0, sticky=E+W)

        self.button4 = Button(self.textFrame, text="Cancel", command=self.end)
        self.button4.grid(row=2, column=0, sticky=E+W)

        self.textFrame.grid()

        self.parent_obj = parent_obj
