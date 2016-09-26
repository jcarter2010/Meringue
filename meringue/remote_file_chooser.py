#import stuff

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

class remote_file_chooser:

    def double_click(self, event):

        #get the directory that the user selected and open it

        item = self.tree.selection()[0]
        self.clone_dir(item)

    def clone_dir(self, dir_name):

        #Warn the user that this might take a while

        tkMessageBox.showwarning("SSH Connect", "Cloning the chosen directory -- this can take a long time if there are a lot of files. Please wait")

        #go to the correct directory for cloning the remote tree

        if self.parent_obj.editing_pi:
            os.chdir('../..')

        #assign all the necessary parameters

        host = self.ip
        port = self.port
        password = self.password
        username = self.username

        #tell the parent what the parametrs are, this will be used later to store the values for easier access

        #self.parent_obj.username = username
        #self.parent_obj.password = password
        #self.parent_obj.ip = self.ip

        #get the remote tree and change to the 'local' directory for tree creation

        tree = self.parent_obj.remote_tree_array
        file_tree = self.parent_obj.remote_tree_file_array
        os.chdir(self.parent_obj.merengue_path + '/local')

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

    def __init__(self, parent, parent_obj, username, ip, password, ssh, port):

        #create the gui

        top = self.top = Toplevel(parent)
        self.parent_obj = parent_obj

        self.textFrame = Frame(top)

        self.tree = ttk.Treeview(self.top)
        self.tree.tag_configure('directory', background='black', foreground='magenta')
        ttk.Style().configure("Treeview", fieldbackground="#000000")
        self.treeScroll = ttk.Scrollbar(self.textFrame, orient=VERTICAL)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side=RIGHT, fill=Y, expand=1)

        for f in self.parent_obj.remote_tree_array:
            self.tree.insert(f[:f.rfind('/')], 0, f, text=f[f.rfind('/') + 1:], tags='directory')

        self.tree.pack(side=LEFT, fill=BOTH, expand=1)

        self.textFrame.pack(fill=BOTH, expand=1)

        self.tree.bind('<Double-1>', self.double_click)

        self.username = username
        self.ip = ip
        self.password = password
        self.ssh = ssh
        self.port = port
