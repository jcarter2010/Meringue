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
from subprocess import Popen
from subprocess import PIPE
import keyword
import re
from multiprocessing import Process
import paramiko
from access_ssh import access_ssh
from method_dialog import method_dialog
from editor import EditorClass
from find_and_replace_dialog import find_and_replace_dialog
from new_dialog import new_dialog
from new_folder_dialog import new_folder_dialog
from open_file_dialog import open_file_dialog
from change_color import change_color

class App:

    def open_file(self, path):
        print(path)
        if isfile(path):
            if not path in self.tab_names:
                pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
                ed = EditorClass(self.root, path)
                pane.add(ed.frame)
                self.n.add(pane, text=path)
                self.n.pack(fill='both', expand=1)
                w = self.root.winfo_width()
                h = self.root.winfo_height()
                #self.n.place(x=200, y=0, width=(w-200), height=h)
                self.tab_names.append(path)
                ed.text.config(insertbackground='white')
                ed.text.config(background=self.background)
                ed.text.config(foreground=self.foreground)
                with open(path, 'r') as f_in:
                    text = f_in.read()
                    lines = text.split('\n')
                    for line in lines:
                        ed.text.insert(END, line+'\n')
                ed.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
                ed.text.tag_configure("keyword", foreground=self.highlight_keyword)
                ed.text.tag_configure("function_name", foreground=self.highlight_function_name)
                ed.text.tag_configure("function", foreground=self.highlight_function)
                ed.text.tag_configure("boolean", foreground=self.highlight_boolean)
                ed.text.tag_configure("string", foreground=self.highlight_string)
                ed.text.tag_configure("number", foreground=self.highlight_number)
                ed.text.tag_configure("operator", foreground=self.highlight_operator)
                #ed.text.tag_configure('normal', foreground=self.highlight_normal)
                ed.text.tag_configure('comment', foreground=self.highlight_comment)
                ed.lnText.config(foreground=self.line_num_color)
                ed.lnText.config(background=self.line_num_background_color)
                #ed.text.event_generate("<Key>", when='tail')
                ed.syntax_coloring(None)
                #ed.color()
                self.eds.append(ed)
            self.n.select(self.tab_names.index(path))

    def change_ed_colors(self):
        for ed in self.eds:
            ed.text.config(insertbackground='white')
            ed.text.config(background=self.background)
            ed.text.config(foreground=self.foreground)
            ed.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
            ed.text.tag_configure("keyword", foreground=self.highlight_keyword)
            ed.text.tag_configure("function_name", foreground=self.highlight_function_name)
            ed.text.tag_configure("function", foreground=self.highlight_function)
            ed.text.tag_configure("boolean", foreground=self.highlight_boolean)
            ed.text.tag_configure("string", foreground=self.highlight_string)
            ed.text.tag_configure("number", foreground=self.highlight_number)
            ed.text.tag_configure("operator", foreground=self.highlight_operator)
            ed.lnText.config(foreground=self.line_num_color)
            ed.lnText.config(background=self.line_num_background_color)
            #ed.text.tag_configure('normal', foreground=self.highlight_normal)
            ed.text.tag_configure('comment', foreground=self.highlight_comment)
        self.tree.tag_configure('directory', background=self.background, foreground=self.dir_color)
        self.tree.tag_configure('file', background=self.background, foreground=self.file_color)
        self.menubar.config(background=self.file_bar_color)
        #self.pane.configure(background=self.pane_color)
        self.root.configure(background=self.background)
        self.menubar.config(background=self.file_bar_color, foreground=self.file_bar_text_color)
        ttk.Style().configure("TNotebook", background=self.notebook_background)

    def copy_click(self):
        index = self.n.tabs().index(self.n.select())
        self.eds[index].text.clipboard_clear()
        text = self.eds[index].text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.eds[index].text.clipboard_append(text)

    def cut_click(self):
        index = self.n.tabs().index(self.n.select())
        self.copy_click()
        self.eds[index].text.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def paste_click(self):
        index = self.n.tabs().index(self.n.select())
        text = self.eds[index].text.selection_get(selection='CLIPBOARD')
        self.eds[index].text.insert('insert', text)

    def recursive_find(self, rootDir):
        for lists in os.listdir(rootDir):
            path = os.path.join(rootDir, lists)
            self.files.append(path)
            if os.path.isdir(path):
                self.recursive_find(path)

    def list_files(self, path, tree, parent, full_path):
        self.files = [os.getcwd()]
        self.recursive_find(os.getcwd())
        counter = 0
        for f in self.files:
            if counter != 0:
                if os.name == 'posix':
                    if(isfile(f)):
                        tree.insert(f[:f.rfind('/')], 0, f, text=f[f.rfind('/') + 1:], tags = ('file',))
                    else:
                        tree.insert(f[:f.rfind('/')], 0, f, text=f[f.rfind('/') + 1:], tags = ('directory',))
                else:
                    if(isfile(f)):
                        tree.insert(f[:f.rfind('\\')], 0, f, text=f[f.rfind('\\') + 1:], tags = ('file',))
                    else:
                        tree.insert(f[:f.rfind('\\')], 0, f, text=f[f.rfind('\\') + 1:], tags = ('directory',))
            else:
                if os.name == 'posix':
                    tree.insert('', 3, f, text=f[f.rfind('/') + 1:], tags = ('directory',))
                else:
                    tree.insert('', 3, f, text=f[f.rfind('\\') + 1:], tags = ('directory',))
            counter = counter + 1
        return tree

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        self.open_file(item)


    def close_all_tabs(self):
        val = tkMessageBox.askokcancel('Open New Folder', "This will close all current tabs, continue?")
        if val:
            for i in range(0, len(self.n.tabs())):
                self.n.forget(0)
                del(self.tab_names[0])
                del(self.eds[0])
        return val

    def close_tab(self):
        index = self.n.tabs().index(self.n.select())
        self.n.forget(self.n.select())
        del(self.tab_names[index])
        del(self.eds[index])

    def open_click(self):
        #args = ['python2', 'open_file.py']
        #p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        #p.wait()
        #out = p.stdout.read().replace('\n', '')
        #if out.startswith('./') == False:
        #    out ='./' + out
        #if not out == '!!DO NOT OPEN!!':
        #    try:
        #        self.open_file(out)
        #    except:
        #        showerror("!!ERROR!!", "File does not exist")
        of = open_file_dialog(self.root, self, os.getcwd())

    def save_click(self):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
        if self.editing_pi:
            transport = paramiko.Transport((self.ip, 22))
            transport.connect(username=self.username, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            try:
                sftp.put(path,path[path.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):])
            except:
                print('Could not push for some reason')

    def save_type(self, event):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
        if self.editing_pi:
            transport = paramiko.Transport((self.ip, 22))
            transport.connect(username=self.username, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            #try:
            sftp.put(path,path[path.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):])
            #except:
            #    print('Could not push for some reason')

    def exit_click(self):
        sys.exit()

    def keyPressed(self, event):
        print("--")
        if event.keysym == 's':
            self.save_click

    def open_folder_click(self):
        val = self.close_all_tabs()
        if val:
            folder = askdirectory()
            os.chdir(folder)
            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)
            self.folder = folder
            self.lines[11] = self.lines[11][:self.lines[11].find('=')+1]+self.folder
            self.write_config()
            self.editing_pi = False

    def find_text_dialog(self):
        temp = find_and_replace_dialog(self.root, self)
        self.root.wait_window(temp.top)

    def find(self, f):
        index = self.n.tabs().index(self.n.select())
        ed = self.eds[index]
        ed.highlight_pattern(f, "highlight")

    def find_one(self, f):
        index = self.n.tabs().index(self.n.select())
        ed = self.eds[index]
        text = ed.text.get("1.0",END)
        count = text.count(f)
        if self.find_counter >= count:
            self.find_counter = 0
        ed.highlight_one(f, "highlight", self.find_counter)
        self.find_counter = self.find_counter + 1

    def replace(self, f, r):
        index = self.n.tabs().index(self.n.select())
        text = self.eds[index].text.get("1.0",END)
        self.eds[index].text.delete("1.0",END)
        text = text.replace(f, r, 1)
        self.eds[index].text.insert(END, text[:-1])

    def replace_all(self, f, r):
        index = self.n.tabs().index(self.n.select())
        text = self.eds[index].text.get("1.0",END)
        self.eds[index].text.delete("1.0",END)
        text = text.replace(f, r)
        self.eds[index].text.insert(END, text[:-1])

    def reset_counters(self):
        self.find_counter = 0

    def find_type(self, event):
        path = self.n.tab(self.n.select())['text']
        self.find_text_dialog()

    def tree_rename(self):
        item = self.tree.selection()[0]
        path = item
        found = True
        if found:
            args = ['python2', self.merengue_path + '/' + 'rename.py', 'test']
            p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
            p.wait()
            out = p.stdout.read().replace('\n', '')
            if not out == '!!DO NOT RENAME!!':
                i = path.rfind('/')
                try:
                    if i != -1:
                        os.rename(path, path[:path.rfind('/')]+'/'+out)
                    else:
                        os.rename(path, out)
                except:
                    print('file does not exist, not renaming anything but the tab')
                self.tree.delete(*self.tree.get_children())
                self.tree = self.list_files('.', self.tree, "", '.')
                self.tree.item(os.getcwd(), open=True)
                if self.editing_pi:
                    new_name = path[:path.rfind('/')]+'/'+out
                    new_name = new_name[new_name.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):]
                    transport = paramiko.Transport((self.ip, 22))
                    transport.connect(username=self.username, password=self.password)

                    sftp = paramiko.SFTPClient.from_transport(transport)
                    try:
                        sftp.rename(item[item.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):], new_name)
                    except:
                        print('not a file')
                    try:
                        sftp.rmdir(item[item.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):], new_name)
                    except:
                        print('not a directory')

    def delete(self):
        item = self.tree.selection()[0]
        try:
            os.remove(item)
            if self.editing_pi:
                transport = paramiko.Transport((self.ip, 22))
                transport.connect(username=self.username, password=self.password)

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.remove(item[item.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):])
                except:
                    print('not a file')
        except:
            print('Not a file')
        try:
            #os.rmdir(item)
            self.delete_file(item)
        except:
            print('Not a directory')
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
    def delete_file(self, path):
        dirs = [f for f in listdir(path) if not isfile(join(path, f))]
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for f in files:
            os.remove(path+'/'+f)
            if self.editing_pi:
                transport = paramiko.Transport((self.ip, 22))
                transport.connect(username=self.username, password=self.password)

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.remove(path[path.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):]+'/'+f)
                except:
                    print('not a file')
        for d in dirs:
            self.delete_file(path+'/'+d)
        os.rmdir(path)
        if self.editing_pi:
            transport = paramiko.Transport((self.ip, 22))
            transport.connect(username=self.username, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            try:
                pass
                sftp.rmdir(path[path.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):]+'/'+d)
            except:
                print('not a directory')


    def show_menu(self, event):
        self.directory_menu.post(event.x_root, event.y_root)

    def on_right_click(self, event):
        if len(self.tree.selection()) > 0:
            self.selected_file_dir = self.tree.selection()[0]
            self.show_menu(event)

    def tab_rename(self, event):
        path = self.n.tab(self.n.select())['text']
        args = ['python2', self.merengue_path + '/' + 'rename.py', path[path.rfind('/')+1:]]
        p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        p.wait()
        out = p.stdout.read().replace('\n', '')
        if not out == '!!DO NOT RENAME!!':
            self.n.tab(self.n.select(), text=out)

    def end_find(self, event):
        for ed in self.eds:
            ed.remove_highlight(None)

    def function_dialog(self, event):
        dialog = method_dialog(self.root, self)

    def ssh(self, event=None):
        dialog = access_ssh(self.root, self)

    def start(self, noOfEditors, noOfLines):
        '''
        scroll_style = ttk.Style()

        scroll_style.element_create("My.Scrollbar.trough", "from", "default")
        scroll_style.element_create("My.Scrollbar.bg", "from", "default")
        scroll_style.element_create("My.Scrollbar.activebackground", "from", "default")

        # Redefine the horizontal scrollbar layout to use the custom trough.
        # This one is appropriate for the 'vista' theme.
        scroll_style.layout("My.TScrollbar",
            [('My.Scrollbar.trough', {'children':
                [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                 ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                 ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                     [('Horizontal.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'nswe'})],
            'sticky': 'we'})])
        # Copy original style configuration and add our new custom configuration option.
        scroll_style.configure("My.TScrollbar", *scroll_style.configure("Horizontal.TScrollbar"))
        scroll_style.configure("My.TScrollbar", troughcolor="black")
        '''
        #s.configure('Tab_Style', background='cyan')
        self.read_config()
        self.pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
        ed = EditorClass(self.root, 'untitled')
        ed.text.config(insertbackground='white')
        ed.text.config(background=self.background)
        ed.text.config(foreground=self.foreground)
        #ed.vScrollbar.config(style="My.TScrollbar")
        ed.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
        ed.text.tag_configure("keyword", foreground=self.highlight_keyword)
        ed.text.tag_configure("function_name", foreground=self.highlight_function_name)
        ed.text.tag_configure("function", foreground=self.highlight_function)
        ed.text.tag_configure("boolean", foreground=self.highlight_boolean)
        ed.text.tag_configure("string", foreground=self.highlight_string)
        ed.text.tag_configure("number", foreground=self.highlight_number)
        ed.text.tag_configure("operator", foreground=self.highlight_operator)
        #ed.text.tag_configure('normal', foreground=self.highlight_normal)
        ed.text.tag_configure('comment', foreground=self.highlight_comment)
        ed.lnText.config(foreground=self.line_num_color)
        ed.lnText.config(background=self.line_num_background_color)

        self.pane.add(ed.frame)
        self.eds.append(ed)
        self.tree_frame = Frame(self.root, width=200)
        self.tree = ttk.Treeview(self.tree_frame)
        #self.tree["columns"]=("Files_and_Folders")
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
        self.tree.tag_configure('directory', background=self.background, foreground=self.dir_color)
        self.tree.tag_configure('file', background=self.background, foreground=self.file_color)
        ttk.Style().configure("Treeview", fieldbackground=self.background)
        self.treeScroll = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.treeScroll.configure(command=self.tree.xview)
        self.treeScroll.pack(side=TOP, fill=X)
        self.tree.configure(xscrollcommand=self.treeScroll.set)
        self.tree.bind("<3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(side=LEFT, fill=BOTH)
        self.tree_frame.pack(side=LEFT, fill=BOTH)
        #self.pane.configure(background=self.pane_color)
        self.pane.pack(fill='both', expand=1)
        self.n.add(self.pane, text='untitled')
        self.n.bind("<Double-1>", self.tab_rename)
        self.n.pack(side=LEFT, fill='both', expand=True)
        ttk.Style().configure("TNotebook", background=self.notebook_background)
        #ttk.Style().configure("TPanedwindow", background=self.pane_color, foreground=self.notebook_foreground)
        self.tab_names.append('untitled')

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_click)
        filemenu.add_command(label="Open Folder", command=self.open_folder_click)
        filemenu.add_command(label="Save", command=self.save_click)
        filemenu.add_command(label='Connect to Remote', command=self.ssh)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_click)
        self.menubar.add_cascade(label="File", menu=filemenu)
        optionsmenu = Menu(self.menubar, tearoff=0)
        optionsmenu.add_command(label="Change Colors", command=self.color_config)
        self.menubar.add_cascade(label="Options", menu=optionsmenu)
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About")
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        self.menubar.add_command(label="Close Tab", command=self.close_tab)
        self.menubar.config(background=self.file_bar_color, foreground=self.file_bar_text_color)

        self.root.configure(background=self.background)
        self.root.title("Merengue")
        self.root.bind('<Control-s>', self.save_type)
        self.root.bind('<Control-f>', self.find_type)
        #self.root.bind('<Control-Shift-p>', self.git_commands)
        self.root.bind('<Escape>', self.end_find)
        self.root.bind('<Control-r>', self.function_dialog)
        self.root.bind('<Control-h>', self.ssh)
        #self.root.bind("<Configure>", self.configure)
        self.root['bg'] = 'black'
        self.root.geometry('{}x{}'.format(600, 400))
        self.root.config(menu=self.menubar)

    def read_config(self):
        with open(self.merengue_path+'config.ini', 'r') as f_in:
            self.lines = f_in.read().split('\n')
            self.highlight_foreground = self.lines[0].split('=')[1]
            self.highlight_background = self.lines[1].split('=')[1]
            self.highlight_keyword = self.lines[2].split('=')[1]
            self.highlight_function_name = self.lines[3].split('=')[1]
            self.highlight_function = self.lines[4].split('=')[1]
            self.highlight_boolean = self.lines[5].split('=')[1]
            self.highlight_string = self.lines[6].split('=')[1]
            self.highlight_number = self.lines[7].split('=')[1]
            self.highlight_operator = self.lines[8].split('=')[1]
            #self.highlight_normal = self.lines[9].split('=')[1]
            self.highlight_comment = self.lines[9].split('=')[1]
            self.foreground = self.lines[10].split('=')[1]
            self.background = self.lines[11].split('=')[1]
            self.file_color = self.lines[12].split('=')[1]
            self.dir_color = self.lines[13].split('=')[1]
            self.line_num_color = self.lines[14].split('=')[1]
            self.line_num_background_color = self.lines[15].split('=')[1]
            self.file_bar_color = self.lines[16].split('=')[1]
            self.file_bar_text_color = self.lines[17].split('=')[1]
            self.notebook_background = self.lines[18].split('=')[1]
            self.folder = self.lines[19].split('=')[1]
        if not self.folder:
            self.folder = askdirectory()
            self.lines[19] = self.lines[19][:self.lines[19].find('=')+1]+self.folder
        self.write_config()
        os.chdir(self.folder)

    def new_file(self):
        nd = new_dialog(self.root, self)

    def new_file_func(self, name):
        item = self.tree.selection()[0]
        if not isfile(item):
            with open(item+'/'+name, 'w') as f_out:
                f_out.write('')
            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)
            if self.editing_pi:
                transport = paramiko.Transport((self.ip, 22))
                transport.connect(username=self.username, password=self.password)

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.put(item+'/'+name,item[item.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):]+'/'+name)
                except:
                    print('Could not push for some reason')
        else:
            tkMessageBox.showwarning("File Creation", "Please select the parent folder for the new file and then try creating it again")

    def new_folder(self):
        nfd = new_folder_dialog(self.root, self)

    def new_folder_func(self, name):
        item = self.tree.selection()[0]
        if not isfile(item):
            #with open(item+'/'+name, 'w') as f_out:
            #    f_out.write('')
            os.mkdir(item+'/'+name)
            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)
            if self.editing_pi:
                transport = paramiko.Transport((self.ip, 22))
                transport.connect(username=self.username, password=self.password)

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.mkdir(item[item.find(self.merengue_path + '/local/') + len(self.merengue_path + '/local/'):]+'/'+name)
                except:
                    print('Could not push for some reason')
        else:
            tkMessageBox.showwarning("File Creation", "Please select the parent folder for the new file and then try creating it again")

    def color_config(self):
        cc = change_color(self.root, self)

    def make_directory_menu(self, w):
        self.directory_menu = Menu(self.root, tearoff=0)
        self.directory_menu.add_command(label="Delete", command=self.delete)
        self.directory_menu.add_command(label="Rename", command=self.tree_rename)
        self.directory_menu.add_command(label='New File', command=self.new_file)
        self.directory_menu.add_command(label='New Folder', command=self.new_folder)
        #self.directory.menu.add_command(label='Copy', command=self.copy_item)
        #self.directory.menu.add_command(label='Paste', command=self.paste_item)

    def write_config(self):
        print('writing')
        with open(self.merengue_path+'config.ini', 'w') as f_out:
            for line in self.lines:
                f_out.write(line + '\n')
            f_out.flush()

    def __init__(self):
        self.merengue_path = os.path.realpath(__file__)
        self.merengue_path = self.merengue_path[:-11]
        #os.chdir(os.path.join(os.path.expanduser('~'), 'Documents'))
        self.root = Tk()
        img = PhotoImage(file=self.merengue_path + 'icon.gif')
        self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        #self.root.iconbitmap(self.merengue_path + '/' + 'merengue_icon.ico')
        self.eds = []
        self.n = ttk.Notebook(self.root)
        self.menubar = Menu(self.root)
        self.tab_names = []
        self.find_string = ''
        self.find_counter = 0
        self.selected_file_dir = ''
        self.tree_array = []
        self.remote_tree_array = []
        self.remote_tree_file_array = []
        self.editing_pi = False
        self.username = ''
        self.password = ''
        self.ip = ''
        self.new_file_or_folder_name = ''
        self.folder = ''
        self.highligh_foreground = ''
        self.highlight_background = ''
        self.highlight_keyword = ''
        self.highlight_function_name = ''
        self.highlight_function = ''
        self.highlight_boolean = ''
        self.highlight_string = ''
        self.highlight_number = ''
        self.highlight_operator = ''
        #self.highlight_normal = ''
        self.foreground = ''
        self.background = ''
        self.start(1, 9999)
        self.make_directory_menu(self.root)
        self.jump_counter = 0
        self.find_counter = 0
        self.recursive_delete('./local')
        self.sftp_stem = ''
        mainloop()

    def recursive_delete(self, rootDir):
        for lists in os.listdir(rootDir):
            path = os.path.join(rootDir, lists)
            if os.path.isdir(path):
                self.recursive_delete(path)
            else:
                try:
                    os.remove(path)
                except:
                    pass
            try:
                os.rmdir(path)
            except:
                print('cannot delete folder')

if __name__ == '__main__':
    App()
