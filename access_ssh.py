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
import paramiko
from remote_file_chooser import remote_file_chooser

class access_ssh:

    def connect(self):
        username = self.entryWidget.get()
        host = self.entryWidget2.get()
        password = self.entryWidget3.get()

        self.remote_tree_array = []
        self.remote_tree_file_array = []

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)

            print('Installing tree')

            tkMessageBox.showwarning("SSH Connect", "Intalling 'tree' command onto the system -- this might take a while")

            stdin, stdout, stderr = ssh.exec_command('sudo apt-get -y install tree')
            stdin.close()

            for line in stdout.read().splitlines():
                print('%s$: %s' % (host, line))

            for line in stderr.read().splitlines():
                print('%s$: %s' % (host, line + "\n"))

            print('Running and capturing directories')

            tkMessageBox.showwarning("SSH Connect", "Pulling the directory structure -- please wait")

            stdin, stdout, stderr = ssh.exec_command('tree -f -i -l -d')
            stdin.close()

            f_outfile = open(self.parent_obj.merengue_path+'temp.txt', 'w')

            counter = 0
            for line in stdout.read().splitlines():
                if ' -> ' in line:
                    self.parent_obj.remote_tree_array.append(line[:line.find(' -> ')])
                else:
                    self.parent_obj.remote_tree_array.append(line)

            self.parent_obj.remote_tree_array = self.parent_obj.remote_tree_array[:-1]

            rfc = remote_file_chooser(self.top, self.parent_obj, username, host, password, ssh)

        except:
            tkMessageBox.showwarning("SSH Connect", "Something failed -- Please try again")

        ssh.close()

        self.top.destroy()

    def cancel(self):
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.textFrame = Frame(top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Username:"
        self.entryLabel.pack()

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.pack()

        self.entryLabel2 = Label(self.textFrame)
        self.entryLabel2["text"] = "IP Address/Hostname:"
        self.entryLabel2.pack()

        self.entryWidget2 = Entry(self.textFrame)
        self.entryWidget2["width"] = 50
        self.entryWidget2.pack()

        self.entryLabel3 = Label(self.textFrame)
        self.entryLabel3["text"] = "Password:"
        self.entryLabel3.pack()

        self.entryWidget3 = Entry(self.textFrame)
        self.entryWidget3["width"] = 50
        self.entryWidget3.pack()

        self.entryWidget.focus_set()

        self.textFrame.pack()

        self.button = Button(top, text="Connect", command=self.connect)
        self.button.pack()

        self.button2 = Button(top, text='Done', command=self.cancel)
        self.button2.pack()

        self.parent_obj = parent_obj
