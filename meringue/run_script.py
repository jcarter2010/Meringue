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
import sys
from subprocess import Popen, PIPE
import threading
import time


class run_script_python_2:

    def read_output(self):
        time.sleep(1)
        num_of_lines = 0
        while True:
            try:
                line = self.p.stdout.readline()
                if line != '':
                    num_of_lines = num_of_lines + 1
                    text = str(line)
                    self.v.set(self.v.get() + '\n' + text)
                line = self.p.stderr.readline()
                if line != '':
                    num_of_lines = num_of_lines + 1
                    text = str(line)
                    self.v.set(self.v.get() + '\n' + text)
                if num_of_lines > 20:
                    lines = self.v.get().split('\n')
                    text = '\n'.join(lines[1:])
                    self.v.set(text)
            except:
                #print('no pipe')
                pass
    def enter_press(self, event):
        try:
            self.p.stdin.write(bytes(self.entryWidget.get() + '\n'))
        except:
            pass

    def __init__(self, filename, parent):

        self.filename = filename

        self.first_enter = True

        self.top = Toplevel(parent)

        self.top.title("Run Script")
        self.top.geometry('{}x{}'.format(600, 400))

        self.textFrame = Frame(self.top)
        self.textFrame.grid(sticky=N+S+E+W)

        for x in range(60):
            Grid.columnconfigure(self.textFrame, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(self.textFrame, y, weight=1)

        self.v = StringVar()
        self.output = Label(self.textFrame, textvariable=self.v, justify=LEFT, bg='black', fg='lime')
        #self.output['height'] = 20

        self.output.grid(row=0, sticky=N+S+E+W)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget.grid(row=1, sticky=N+S+E+W)
        self.entryWidget.focus_set()

        self.top.bind('<Return>', self.enter_press)
        #self.top.geometry('500x600')

        thread = threading.Thread(target=self.read_output)
        thread.daemon = True
        thread.start()

        self.p = Popen(['python2', self.filename], stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)

        mainloop()

#run_script('/home/jcarter2010/Documents/UIUC/PHYS_199_Week_5/homework.py')

class run_script_python_3:

    def read_output(self):
        time.sleep(1)
        num_of_lines = 0
        while True:
            try:
                line = self.p.stdout.readline()
                if line != '':
                    num_of_lines = num_of_lines + 1
                    text = str(line)
                    self.v.set(self.v.get() + '\n' + text)
                line = self.p.stderr.readline()
                if line != '':
                    num_of_lines = num_of_lines + 1
                    text = str(line)
                    self.v.set(self.v.get() + '\n' + text)
                if num_of_lines > 20:
                    lines = self.v.get().split('\n')
                    text = '\n'.join(lines[1:])
                    self.v.set(text)
            except:
                #print('no pipe')
                pass
    def enter_press(self, event):
        try:
            self.p.stdin.write(bytes(self.entryWidget.get() + '\n'))
        except:
            pass

    def __init__(self, filename, parent):

        self.filename = filename

        self.first_enter = True

        self.top = Toplevel(parent)

        self.top.title("Run Script")
        self.top["padx"] = 40
        self.top["pady"] = 20

        self.textFrame = Frame(self.top)

        self.v = StringVar()
        self.output = Label(self.textFrame, textvariable=self.v, justify=LEFT, bg='black', fg='lime', relief=SUNKEN)
        self.output['height'] = 20

        self.output.grid(row=0, column=0, sticky=E+W)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget.grid(row=1, column=0, sticky=E+W)
        self.entryWidget.focus_set()

        self.textFrame.grid()

        self.top.bind('<Return>', self.enter_press)
        #self.top.geometry('500x600')

        thread = threading.Thread(target=self.read_output)
        thread.daemon = True
        thread.start()

        self.p = Popen(['python', self.filename], stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)

        mainloop()

#run_script('/home/jcarter2010/Documents/UIUC/PHYS_199_Week_5/homework.py')
