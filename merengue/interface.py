from interactive_paramiko import SSH
import os
try:
    import Tkinter
    from Tkinter import *
    import ttk
except:
    import tkinter as Tkinter
    from tkinter import *
    import tkinter.ttk as ttk
import time
import paramiko
import threading

class App:
    def __init__(self):

        print('Please enter your connection information')
        try:
            self.username = raw_input('Username: ')
            self.password = raw_input('Password: ')
            self.server = raw_input('Server IP: ')
            self.port = int(raw_input('Port: '))
        except:
            self.username = input('Username: ')
            self.password = input('Password: ')
            self.server = input('Server IP: ')
            self.port = int(input('Port: '))

        self.items = []
        self.folders = []
        self.files = []
        self.scroll_y = 30
        self.current_directory = '.'
        self.top = Tkinter.Tk()
        self.canvas = Canvas(self.top, width=800, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.Click)
        self.top.bind("<Up>", self.Scroll_Up)
        self.top.bind("<Down>", self.Scroll_Down)
        self.menubar = Menu(self.top)
        openmenu = Menu(self.menubar, tearoff=0)
        openmenu.add_command(label="Open", command=self.Open_Folder)
        self.menubar.add_cascade(label="Open", menu=openmenu)
        #openmenu = Menu(self.menubar, tearoff=0)
        terminalmenu = Menu(self.menubar, tearoff=0)
        terminalmenu.add_command(label="Open Terminal", command=self.Open_Terminal)
        self.menubar.add_cascade(label="Open Terminal", menu=terminalmenu)
        #terminalmenu = Menu(self.menubar, tearoff=0)
        self.connection = SSH(self.server, self.username, self.password, self.port, self)
        self.connection.openShell()
        self.top.config(menu=self.menubar)
        self.top.mainloop()

    def Scroll_Up(self, event):
        self.scroll_y = self.scroll_y - 600
        if self.scroll_y < 30:
            self.scroll_y = 30
        self.Draw()

    def Scroll_Down(self, event):
        self.scroll_y = self.scroll_y + 600
        self.Draw()

    def Open_Folder(self):
        self.connection.sendShell('ls --color=never')

    def Click(self, event):
        x, y = event.x, event.y
        if len(self.canvas.gettags('current')) > 0:
            index = int(self.canvas.gettags('current')[0])
            if index in self.folders:
                self.connection.sendShell('cd ' + self.tot[index])
                self.current_directory = self.current_directory + '/' + self.tot[index]
                time.sleep(1)
                self.connection.sendShell('ls --color=never')
            if index in self.files:
                print(self.tot[index])
                self.progress = ttk.Progressbar(self.canvas, orient="horizontal",length=800, mode="determinate")
                self.progress.place(x = 0, y = 0)
                self.progress["maximum"] = 100
                self.progress["value"] = 0
                transport = paramiko.Transport((self.server, self.port))
                self.progress["value"] = 25
                transport.connect(username = self.username, password = self.password)
                self.progress["value"] = 50
                sftp = paramiko.SFTPClient.from_transport(transport)
                self.progress["value"] = 75
                sftp.get(self.current_directory + '/' + self.tot[index], './singular_editing_local/' + self.tot[index], None)
                self.progress["value"] = 100
                time.sleep(0.5)
                self.progress.destroy()

    def Process_Output(self, command, output):
        if command == 'ls --color=never -d */':
            temp = output
            temp_command = command.replace(' ', '')
            print(temp[0])
            while temp_command.startswith(temp[0]):
                temp_command = temp_command.replace(temp[0], '', 1)
                del(temp[0])
                print(temp_command)
            self.current_folders = ['..'] + temp
            for folder in self.current_folders:
                if folder in self.all_files_and_folders:
                    del(self.all_files_and_folders[self.all_files_and_folders.index(folder)])
            self.tot = self.current_folders + self.all_files_and_folders
            self.Draw()
        if command == 'ls --color=never':
            temp = output
            temp_command = command.replace(' ', '')
            print(temp_command)
            while temp_command.startswith(temp[0]):
                temp_command = temp_command.replace(temp[0], '', 1)
                del(temp[0])
                print(temp_command)
            self.all_files_and_folders = temp
            self.connection.sendShell('ls --color=never -d */')

    def Draw(self):
        self.canvas.delete('all')
        for widget in self.canvas.winfo_children():
            widget.destroy()
        x = 10
        y = self.scroll_y
        counter = 0
        index = 0
        self.items = []
        self.folders = []
        self.files = []
        for f in self.current_folders:
            lab = Label(self.canvas, text=f)
            lab.place(x = x, y = y + 90)
            self.canvas.create_rectangle(x + 5, y + 10, x + 65, y + 80, tags=str(index), fill="#D2B48C")
            self.canvas.create_rectangle(x + 5, y, x + 25, y + 10, tags=str(index), fill="#D2B48C")
            self.canvas.create_rectangle(x, y + 10, x + 5, y + 80, tags=str(index), fill="#8B4513")
            self.items.append(f)
            self.folders.append(index)
            index = index + 1
            counter = counter + 1
            x = x + 80
            if counter == 8:
                counter = 0
                x = 10
                y = y + 120
        for f in self.all_files_and_folders:
            lab = Label(self.canvas, text=f)
            lab.place(x = x, y = y + 90)
            self.canvas.create_rectangle(x, y, x + 70, y + 80, tags=str(index), fill="white")
            self.items.append(f)
            self.files.append(index)
            index = index + 1
            counter = counter + 1
            x = x + 80
            if counter == 8:
                counter = 0
                x = 10
                y = y + 120

    def Open_Terminal(self):
        
