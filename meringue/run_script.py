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


class run_script:

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
        self.output = Label(self.textFrame, textvariable=self.v, justify=LEFT)
        self.output["width"] = 180
        self.output['height'] = 20

        self.output.pack(side=TOP, fill=Y, expand = 1)

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 180
        self.entryWidget.pack(side=BOTTOM)
        self.entryWidget.focus_set()

        self.textFrame.pack(fill=BOTH, expand=1)

        self.top.bind('<Return>', self.enter_press)
        self.top.geometry('500x600')

        thread = threading.Thread(target=self.read_output)
        thread.daemon = True
        thread.start()

        try:
            self.p = Popen(['python', self.filename], stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)
        except:
            self.p = Popen(['python2', self.filename], stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)

        mainloop()

#run_script('/home/jcarter2010/Documents/UIUC/PHYS_199_Week_5/homework.py')
