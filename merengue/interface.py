from interactive_paramiko import SSH
import os
try:
    from Tkinter import *
    import Tkinter as Tkinter
    import ttk
    import tkFileDialog
    import tkMessageBox
    from tkFileDialog import askdirectory
except:
    from tkinter import *
    import tkinter as Tkinter
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkMessageBox
    from tkinter.filedialog import askdirectory
import time
import paramiko
import threading
import ImageTk
import Image

class Paramiko_Interface:
    def __init__(self, parent_obj, username, password, server, port):

        '''
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
        '''
        self.parent_obj = parent_obj

        self.username = username
        self.password = password
        self.server = server
        self.port = int(port)

        self.items = []
        self.folders = []
        self.files = []
        self.scroll_y = 30
        self.current_directory = '.'
        self.top = Tkinter.Toplevel()
        self.canvas = Canvas(self.top, width=800, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.Click)
        self.canvas.bind("<Button-3>", self.Right_Click)
        self.top.bind("<Up>", self.Scroll_Up)
        self.top.bind("<Down>", self.Scroll_Down)
        self.menubar = Menu(self.top)
        #self.menubar.add_command(label="Help", command=self.display_commands)
        #openmenu = Menu(self.menubar, tearoff=0)
        #openmenu.add_command(label="Open", command=self.Open_Folder)
        #self.menubar.add_cascade(label="Open", menu=openmenu)
        #openmenu = Menu(self.menubar, tearoff=0)
        #terminalmenu = Menu(self.menubar, tearoff=0)
        #terminalmenu.add_command(label="Open Terminal", command=self.Open_Terminal)
        #self.menubar.add_cascade(label="Open Terminal", menu=terminalmenu)
        #terminalmenu = Menu(self.menubar, tearoff=0)
        self.connection = SSH(self.server, self.username, self.password, self.port, self)
        self.connection.openShell()
        time.sleep(4)
        self.Open_Folder()
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
                self.current_directory = self.current_directory + '/' + self.tot[index]
                self.connection.sendShell('cd ' + self.tot[index] + ' && ls --color=never')
                #time.sleep(2)
                #self.connection.sendShell()
            '''
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
            '''

    def clone_dir(self, dir_name):

        #Warn the user that this might take a while
        self.remote_tree_array = []

        tkMessageBox.showwarning("SSH Connect", "Cloning the chosen directory -- this can take a long time if there are a lot of files. Please wait")

        #go to the correct directory for cloning the remote tree

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server, username=self.username, password=self.password, port=int(self.port))

        #Capture the directory output

        print('Running and capturing directories')

        #tkMessageBox.showwarning("SSH Connect", "Pulling the directory structure -- please wait")

        stdin, stdout, stderr = ssh.exec_command('tree -f -i -l -d')
        stdin.close()

        #Extract the name of all of the directories from the tree and store them

        for line in stdout.read().splitlines():
            if ' -> ' in line:
                self.remote_tree_array.append(line[:line.find(' -> ')])
            else:
                self.remote_tree_array.append(line)

        #Elimiate the top directory as it is not needed

        self.remote_tree_array = self.remote_tree_array[:-1]


        if self.parent_obj.editing_pi:
            os.chdir('../..')

        #assign all the necessary parameters

        host = self.server
        port = self.port
        password = self.password
        username = self.username

        #tell the parent what the parametrs are, this will be used later to store the values for easier access

        #self.parent_obj.username = username
        #self.parent_obj.password = password
        #self.parent_obj.ip = self.ip

        #get the remote tree and change to the 'local' directory for tree creation

        tree = self.remote_tree_array
        #file_tree = self.parent_obj.remote_tree_file_array
        os.chdir(self.parent_obj.merengue_path + '/local')
        print(os.getcwd())

        #for each directory in the tree go through and create it in 'local' for preperation of cloning

        for item in tree:
            if item.startswith(dir_name):
                os.makedirs(item)
        os.chdir(dir_name)

        #setup sftp from paramiko

        self.parent_obj.sftp_stem = dir_name[dir_name.find('./') + 2:]

        transport = paramiko.Transport((host, int(port)))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.chdir(dir_name[dir_name.find('./') + 2:])

        #copy all of the files from the selected tree

        self.copy_files('', sftp)

        #reset the treeview on the left side of the interface

        self.parent_obj.tree.delete(*self.parent_obj.tree.get_children())
        self.parent_obj.tree = self.parent_obj.list_files('.', self.parent_obj.tree, "", '.')
        self.parent_obj.tree.item(os.getcwd(), open=True)

        #tell the interface that we're editing remote files

        self.parent_obj.editing_pi = True
        self.top.destroy()

    def copy_files(self, path, sftp):

        dirlist = sftp.listdir(path)
        for files in dirlist:

            #for every file try to pull it

            if files.startswith('.') == False:
                try:
                    print(' -> Attempting to download: "{}", and saving it {}'.format(files, files))
                    print(path + '/' + files)
                    print(' --> remotepath stat: {}'.format(sftp.stat(files)))
                    sftp.get(files, files)
                except:

                    #if it's a directory then go into it and do the same thing

                    os.chdir(files)
                    sftp.chdir(files)
                    self.copy_files('', sftp)
                    sftp.chdir('..')
                    os.chdir('..')

    def Right_Click(self, event):
        x, y = event.x, event.y
        if len(self.canvas.gettags('current')) > 0:
            index = int(self.canvas.gettags('current')[0])
            if index in self.folders:
                '''
                self.connection.sendShell('cd ' + self.tot[index])

                time.sleep(0.5)
                self.connection.sendShell('ls --color=never')
                '''
                self.current_directory = self.current_directory + '/' + self.tot[index]
                self.clone_dir(self.current_directory)
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
                sftp.get(self.current_directory + '/' + self.tot[index], self.parent_obj.merengue_path + 'singular_editing_local/' + self.tot[index], None)
                self.progress["value"] = 100
                time.sleep(0.5)
                self.progress.destroy()

    def Process_Output(self, command, output):
        if command == 'ls --color=never -d */':
            temp = output
            temp_command = command.replace(' ', '')
            if len(temp) > 0:
                while temp_command.startswith(temp[0]):
                    temp_command = temp_command.replace(temp[0], '', 1)
                    del(temp[0])
            self.current_folders = ['..'] + temp
            for folder in self.current_folders:
                if folder in self.all_files_and_folders:
                    del(self.all_files_and_folders[self.all_files_and_folders.index(folder)])
            self.tot = self.current_folders + self.all_files_and_folders
            self.Draw()
        if command == 'ls --color=never':
            temp = output
            temp_command = command.replace(' ', '')
            #print(temp_command)
            if len(temp) > 0:
                while temp_command.startswith(temp[0]):
                    temp_command = temp_command.replace(temp[0], '', 1)
                    del(temp[0])
                    print(temp_command)
                self.all_files_and_folders = temp
                self.connection.sendShell('ls --color=never -d */')
        #self.Draw()

    def Draw(self):
        #folder_img = ImageTk.PhotoImage(Image.open('./resources/folder_image.png'))
        #file_img = ImageTk.PhotoImage(Image.open('./resources/file_image.png'))
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
            #lab2 = Label(self.canvas, image = folder_img)
            #lab2.place(x=x, y=y)
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
            #lab2 = Label(self.canvas, image = file_img)
            #lab2.place(x=x, y=y)
            self.items.append(f)
            self.files.append(index)
            index = index + 1
            counter = counter + 1
            x = x + 80
            if counter == 8:
                counter = 0
                x = 10
                y = y + 120

    #def Open_Terminal(self):
