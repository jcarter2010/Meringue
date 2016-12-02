#!/usr/bin/env python2

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
from pkg_resources import resource_stream
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
from code_display import DisplayClass
from find_and_replace_dialog import find_and_replace_dialog
from remote_file_chooser import remote_file_chooser
from new_dialog import new_dialog
from new_folder_dialog import new_folder_dialog
from open_file_dialog import open_file_dialog
from change_color import change_color
from interface import Paramiko_Interface
from create_config import create_config
from run_script import run_script_python_2
from run_script import run_script_python_3
from about_dialog import about_dialog
from project_opener import project_opener
from project_manager import project_manager

class App:

    def open_file(self, path):
        if isfile(path):
            if not path in self.tab_names:
                pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
                ed = EditorClass(self.root, path, self)
                pane.add(ed.frame)
                self.n.add(pane, text=path)
                self.n.grid(row=0, column=1, rowspan=40, sticky=N+S+E+W)
                w = self.root.winfo_width()
                h = self.root.winfo_height()
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
                self.eds.append(ed)

                #self.dis.place(x=100, y=0)
                #self.dis.destroy()
                #self.set_display_text(path)
                #ed.color()

            self.n.select(self.tab_names.index(path))

    def update_display(self, start, end):
        #self.dis.highlight_current(start, end)
        pass

    def reset_display_text(self):
        self.n.tab(self.n.select())['text']
        try:
            self.pane.destroy()
        except:
            pass
        self.pane = PanedWindow(self.display_frame, orient=HORIZONTAL, opaqueresize=True)
        self.dis = DisplayClass(self.display_frame, path)
        self.pane.add(self.dis.frame)
        self.pane.grid(row=0, column=0, rowspan=40, columnspan=60, sticky=N+S+E+W)
        self.dis.text.config(insertbackground='white')
        self.dis.text.config(background=self.background)
        self.dis.text.config(foreground=self.foreground)
        with open(path, 'r') as f_in:
            text = f_in.read()
            lines = text.split('\n')
            for line in lines:
                self.dis.text.insert(END, line+'\n')
        self.dis.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
        self.dis.text.tag_configure("keyword", foreground=self.highlight_keyword)
        self.dis.text.tag_configure("function_name", foreground=self.highlight_function_name)
        self.dis.text.tag_configure("function", foreground=self.highlight_function)
        self.dis.text.tag_configure("boolean", foreground=self.highlight_boolean)
        self.dis.text.tag_configure("string", foreground=self.highlight_string)
        self.dis.text.tag_configure("number", foreground=self.highlight_number)
        self.dis.text.tag_configure("operator", foreground=self.highlight_operator)
        #self.dis.text.tag_configure('normal', foreground=self.highlight_normal)
        self.dis.text.tag_configure('comment', foreground=self.highlight_comment)
        self.dis.text.tag_configure('current_selection', background='#555555')
        #self.dis.lnText.config(foreground=self.line_num_color)
        #self.dis.lnText.config(background=self.line_num_background_color)
        #self.dis.text.event_generate("<Key>", when='tail')
        self.dis.syntax_coloring(None)
        self.dis.text.config(state=DISABLED)

        #self.display_frame.add(self.dis)

    def set_display_text(self, path):
        try:
            self.pane.destroy()
        except:
            pass
        self.pane = PanedWindow(self.display_frame, orient=HORIZONTAL, opaqueresize=True)
        self.dis = DisplayClass(self.display_frame, path)
        self.pane.add(self.dis.frame)
        self.pane.pack(fill='both', expand=1)
        self.dis.text.config(insertbackground='white')
        self.dis.text.config(background=self.background)
        self.dis.text.config(foreground=self.foreground)
        with open(path, 'r') as f_in:
            text = f_in.read()
            lines = text.split('\n')
            for line in lines:
                self.dis.text.insert(END, line+'\n')
        self.dis.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
        self.dis.text.tag_configure("keyword", foreground=self.highlight_keyword)
        self.dis.text.tag_configure("function_name", foreground=self.highlight_function_name)
        self.dis.text.tag_configure("function", foreground=self.highlight_function)
        self.dis.text.tag_configure("boolean", foreground=self.highlight_boolean)
        self.dis.text.tag_configure("string", foreground=self.highlight_string)
        self.dis.text.tag_configure("number", foreground=self.highlight_number)
        self.dis.text.tag_configure("operator", foreground=self.highlight_operator)
        #self.dis.text.tag_configure('normal', foreground=self.highlight_normal)
        self.dis.text.tag_configure('comment', foreground=self.highlight_comment)
        self.dis.text.tag_configure('current_selection', background='#555555')
        #self.dis.lnText.config(foreground=self.line_num_color)
        #self.dis.lnText.config(background=self.line_num_background_color)
        #self.dis.text.event_generate("<Key>", when='tail')
        self.dis.syntax_coloring(None)
        self.dis.text.config(state=DISABLED)


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

    def close_tab_event(self, event):
        index = self.n.tabs().index(self.n.select())
        self.n.forget(self.n.select())
        del(self.tab_names[index])
        del(self.eds[index])

    def open_click(self):
        of = open_file_dialog(self.root, self, os.getcwd().replace('\\', '/'))

    def save_click(self):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd().replace('\\', '/'), open=True)
        if self.editing_pi:
            transport = paramiko.Transport((self.ip, 22))
            transport.connect(username=self.username, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            try:
                sftp.put(path,path[path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
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
            try:
                sftp.put(path,path[path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
            except:
                print('Could not push for some reason')

    def exit_click(self):
        sys.exit()

    def keyPressed(self, event):
        print("--")
        if event.keysym == 's':
            self.save_click

    def open_folder_click(self):
        val = self.close_all_tabs()
        if val:
            folder = askdirectory().replace('\\', '/')
            os.chdir(folder)
            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)
            self.folder = folder
            self.lines[19] = self.lines[19][:self.lines[19].find('=')+1]+self.folder
            self.write_config()
            self.editing_pi = False

    def open_folder(self, folder):
        val = self.close_all_tabs()
        if val:
            os.chdir(folder)
            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)
            self.folder = folder
            self.lines[19] = self.lines[19][:self.lines[19].find('=')+1]+self.folder
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

    def undo_command(self):
        index = self.n.tabs().index(self.n.select())
        self.eds[index].undo(None)

    def redo_command(self):
        index = self.n.tabs().index(self.n.select())
        self.eds[index].redo(None)

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
            args = ['python2', self.meringue_path + '/' + 'rename.py', 'test']
            p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
            p.wait()
            out = p.stdout.read().replace('\n', '')
            if not out == '!!DO NOT RENAME!!':
                i = path.replace('\\', '/').rfind('/')
                try:
                    if i != -1:
                        os.rename(path, path[:path.rfind('/')]+'/'+out)
                    else:
                        os.rename(path, out)
                except:
                    print('file does not exist, not renaming anything but the tab')
                self.tree.delete(*self.tree.get_children())
                self.tree = self.list_files('.', self.tree, "", '.')
                self.tree.item(os.getcwd().replace('\\', '/'), open=True)
                if self.editing_pi:
                    new_name = path[:path.rfind('/')]+'/'+out
                    new_name = new_name[new_name.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):]
                    transport = paramiko.Transport((self.ip, 22))
                    transport.connect(username=self.username, password=self.password)

                    sftp = paramiko.SFTPClient.from_transport(transport)
                    try:
                        sftp.rename(item[item.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):], new_name)
                    except:
                        print('not a file')
                    try:
                        sftp.rmdir(item[item.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):], new_name)
                    except:
                        print('not a directory')

    def delete(self):
        if tkMessageBox.askyesno("Delete", "Delte this file or folder?"):
            item = self.tree.selection()[0]
            try:
                os.remove(item)
                if self.editing_pi:
                    transport = paramiko.Transport((self.ip, 22))
                    transport.connect(username=self.username, password=self.password)

                    sftp = paramiko.SFTPClient.from_transport(transport)
                    try:
                        sftp.remove(item[item.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
                    except:
                        print('not a file')
            except:
                print('Not a file')
            try:
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
                    sftp.remove(path[path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):]+'/'+f)
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
                sftp.rmdir(path[path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):]+'/'+d)
            except:
                print('not a directory')


    def show_menu(self, event):
        self.directory_menu.post(event.x_root, event.y_root)

    def on_right_click(self, event):
        if len(self.tree.selection()) > 0:
            self.selected_file_dir = self.tree.selection()[0]
            self.show_menu(event)

    def save_project(self):
        with open(self.meringue_path + '/data/projects.txt', 'w') as f_out:
            f_out.write('TEMP;{}'.format(self.folder))

    def tab_rename(self, event):
        path = self.n.tab(self.n.select())['text']
        if os.name == 'nt':
            print(self.meringue_path)
            args = ['python', self.meringue_path + 'rename.py', path[path.rfind('\\')+1:]]
        else:
            args = ['python2', self.meringue_path + 'rename.py', path[path.rfind('/')+1:]]
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

    def open_terminal(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system('gnome-terminal')
        if sys.platform == 'darwin':
            os.system('open Terminal')
        if sys.platform == 'win32':
            os.system('start cmd')

    def open_project(self):
        project_opener(self.root, self)

    def manage_projects(self):
        project_manager(self.root, self)

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
        try:
            self.read_config()
        except:
            create_config(self.meringue_path)
            self.read_config()
        '''
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
        '''
        ttk.Style().configure('TFrame', fieldbackground=self.background, background=self.background)
        self.tree_frame = Frame(self.root, bg=self.background, width=200, height=10000)
        #ttk.Style().configure('TFrame', fieldbackground=self.background, background=self.background)
        #self.tree_frame = Frame(self.root, bg=self.background, width=200, height=10000)
        self.bg_frame = Frame(self.tree_frame, width=200, height=10000, bg=self.background)
        #self.display_frame = Frame(self.root, width=150, height=10000, bg=self.background)
        self.tree = ttk.Treeview(self.tree_frame)
        #self.tree["columns"]=("Files_and_Folders")
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
        if os.name != 'nt':
            self.tree.tag_configure('directory', background=self.background, foreground=self.dir_color)
            self.tree.tag_configure('file', background=self.background, foreground=self.file_color)
            ttk.Style().configure("Treeview", fieldbackground=self.background, background=self.background)
        self.treeScroll = ttk.Scrollbar(self.tree_frame, orient=VERTICAL)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.grid(row=0, column=1, rowspan=40, sticky=N+S)
        self.tree.configure(xscrollcommand=self.treeScroll.set)
        self.tree.bind("<3>", self.on_right_click)
        self.tree.bind("<2>", self.on_right_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.grid(row=0, column=0, rowspan=40, sticky=N+S)
        self.tree_frame.grid(row=0, column=0, rowspan=40, sticky=N+S)
        #self.display_frame.pack(side=RIGHT, fill=Y, expand=0)
        #self.pane.pack(fill='both', expand=1)
        #self.n.add(self.pane, text='untitled')
        self.n.bind("<Double-1>", self.tab_rename)
        self.n.bind('<3>', self.close_tab_event)
        self.n.bind('<2>', self.close_tab_event)
        #self.n.bind("<1>", self.reset_display_text)
        self.n.grid(row=0, column=1, rowspan=40, columnspan=60, sticky=N+S+E+W)
        ttk.Style().configure("TNotebook", background=self.notebook_background)
        #ttk.Style().configure("TPanedwindow", background=self.pane_color, foreground=self.notebook_foreground)
        #self.tab_names.append('untitled')

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_click)
        filemenu.add_command(label="Open Folder", command=self.open_folder_click)
        filemenu.add_command(label="Save", command=self.save_click)
        filemenu.add_command(label="Close Tab", command=self.close_tab)
        filemenu.add_separator()
        filemenu.add_command(label='Open Project', command = self.open_project)
        filemenu.add_command(label='Save Project', command = self.save_project)
        filemenu.add_command(label='Manage Projects', command = self.manage_projects)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_click)
        self.menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo_command)
        editmenu.add_command(label="Redo", command=self.redo_command)
        editmenu.add_separator()
        editmenu.add_command(label="Change Editor Colors", command=self.color_config)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        viewmenu = Menu(self.menubar, tearoff=0)
        viewmenu.add_command(label="Toggle Menubar", command=self.hide_show_menubar_command)
        viewmenu.add_command(label="Toggle File Explorer", command=self.hide_show_tree_command)
        self.menubar.add_cascade(label="View", menu=viewmenu)
        #optionsmenu = Menu(self.menubar, tearoff=0)
        #optionsmenu.add_command(label="Change Colors", command=self.color_config)
        #self.menubar.add_cascade(label="Options", menu=optionsmenu)
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.open_about)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        #self.menubar.add_command(label="Close Tab", command=self.close_tab)
        terminalmenu = Menu(self.menubar, tearoff=0)
        terminalmenu.add_command(label="Local Terminal", command=self.open_terminal)
        terminalmenu.add_command(label="Remote Terminal", command=self.open_remote_terminal)
        self.menubar.add_cascade(label="Open Terminal", menu=terminalmenu)
        remotemenu = Menu(self.menubar, tearoff=0)
        remotemenu.add_command(label='Connect to Remote', command=self.ssh)
        #remotemenu.add_command(label='Edit Directory', command=self.remote_folder_choose)
        remotemenu.add_command(label="Open Explorer", command=self.paramiko_interface_open)
        self.menubar.add_cascade(label="Remote Actions", menu=remotemenu)
        #runmenu = Menu(self.menubar, tearoff=0)
        runmenu = Menu(self.menubar, tearoff=0)
        runmenu.add_command(label='Python 2', command=self.run_file_python_2)
        runmenu.add_command(label='Python 3', command=self.run_file_python_3)
        self.menubar.add_cascade(label="Run File", menu=runmenu)
        #self.menubar.add_command(label="Open Terminal", command=self.open_terminal)
        self.menubar.config(background=self.file_bar_color, foreground=self.file_bar_text_color)
        self.root.configure(background=self.background)
        self.root.title("meringue")
        self.root.bind('<Control-s>', self.save_type)
        self.root.bind('<Control-f>', self.find_type)
        #self.root.bind('<Control-Shift-p>', self.git_commands)
        self.root.bind('<Escape>', self.end_find)
        #self.root.bind('<Control-r>', self.function_dialog)
        self.root.bind('<Control-h>', self.ssh)
        self.root.bind('<Alt_R>', self.hide_show_menubar);
        self.root.bind('<Control-e>', self.hide_show_tree);
        #self.root.bind("<Configure>", self.configure)
        self.root['bg'] = 'black'
        self.root.geometry('{}x{}'.format(600, 400))
        self.root.config(menu=self.menubar)
        if os.name == 'nt':
            ttk.Style().theme_use('default')

        for x in range(60):
            Grid.columnconfigure(self.n, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(self.n, y, weight=1)

        for x in range(60):
            Grid.columnconfigure(self.tree, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(self.tree, y, weight=1)

        for x in range(60):
            Grid.columnconfigure(self.tree_frame, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(self.tree_frame, y, weight=1)

        for x in range(60):
            Grid.columnconfigure(self.root, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(self.root, y, weight=1)

        self.hide_menubar = True;
        self.hide_tree = True;
        self.emptyMenu = Menu(self.root)

    def open_about(self):
        about_dialog(self)

    def hide_show_menubar(self, event):
        if self.hide_menubar:
            self.root.config(menu=self.emptyMenu)
            self.hide_menubar = False;
        else:
            self.root.config(menu=self.menubar)
            self.hide_menubar = True

    def hide_show_tree(self, event):
        if self.hide_tree:
            self.tree_frame.grid_forget()
            self.hide_tree = False
        else:
            self.tree_frame.grid(row=0, column=0, rowspan=40, sticky=N+S)
            self.hide_tree = True

    def hide_show_menubar_command(self):
        self.hide_show_menubar(None)

    def hide_show_tree_command(self):
        self.hide_show_tree(None)

    def run_file_python_2(self):
        index = self.n.tabs().index(self.n.select())
        print(self.tab_names[index])
        run_script_python_2(self.tab_names[index], self.root)

    def run_file_python_3(self):
        index = self.n.tabs().index(self.n.select())
        print(self.tab_names[index])
        run_script_python_3(self.tab_names[index], self.root)

    def paramiko_interface_open(self):
        Paramiko_Interface(self, self.username, self.password, self.ip, self.port)

    def remote_folder_choose(self):
        #We're going to store the directory tree here

        self.remote_tree_array = []

        #Let's ssh into the remote machine

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, username=self.username, password=self.password, port=int(self.port))

            #Capture the directory output

            print('Running and capturing directories')

            tkMessageBox.showwarning("SSH Connect", "Pulling the directory structure -- please wait")

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

            #Go to letting the user select the directory that they want

            rfc = remote_file_chooser(self, self, self.username, self.ip, self.password, ssh, int(self.port))

        except:

            #If something failed throw an error message

            tkMessageBox.showwarning("SSH Connect", "Something failed -- Please try again")

        ssh.close()
    def open_remote_terminal(self):
        self.current_directory = '.'
        if sys.platform == "win32":
            try:
                #os.system('start python ' + self.meringue_path + 'paramiko_terminal.py "{}" {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
                os.system('start python "' + self.meringue_path + 'paramiko_terminal.py" "{}" {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            except:
            #    try:
            #        os.system('start python2 paramiko_terminal.py {} {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            #    except:
                pass
        if sys.platform == "darwin":
            #try:
            #    os.system('open python paramiko_terminal.py {} {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            #except:
            try:
                os.system('open python2 "' + self.meringue_path + 'paramiko_terminal.py" "{}" {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            except:
                pass
        if sys.platform == "linux" or sys.platform == "linux2":
            #try:
            #    os.system('xterm -hold -e python paramiko_terminal.py {} {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            #except:
            try:
                os.system('xterm -e python2 "' + self.meringue_path + 'paramiko_terminal.py" "{}" {} {} {} {}'.format(self.current_directory, self.ip, self.username, self.password, self.port))
            except:
                pass


    def copy_file(self):
        if len(self.tree.selection()) > 0:
            item = self.tree.selection()[0]
            self.copy_path = item

    def paste_file(self):
        if self.copy_path != '':
            if len(self.tree.selection()) > 0:
                item = self.tree.selection()[0]
                dirs = [item+'/'+f for f in listdir(item) if not isfile(join(item, f))]
                files = [item+'/'+f for f in listdir(item) if isfile(join(item, f))]
                if not isfile(item):
                    f_name = self.copy_path[self.copy_path.rfind('/')+1:]

                    write_path = item+'/'+f_name
                    if isfile(self.copy_path):
                        counter = 1
                        temp_write_path = write_path
                        while temp_write_path in files:
                            temp_write_path = write_path+'.'+str(counter)
                            counter = counter + 1
                        write_path = temp_write_path
                        with open(write_path, 'w') as f_out:
                            with open(self.copy_path, 'r') as f_in:
                                text = f_in.read()
                                f_out.write(text)
                    else:
                        counter = 1
                        temp_write_path = write_path
                        while temp_write_path in dirs:
                            temp_write_path = write_path+'.'+str(counter)
                            counter = counter + 1
                        write_path = temp_write_path
                        self.recursive_paste(write_path)
                copy_path = ''
                if self.editing_pi:
                    transport = paramiko.Transport((self.ip, 22))
                    transport.connect(username=self.username, password=self.password)

                    sftp = paramiko.SFTPClient.from_transport(transport)
                    try:
                        sftp.put(write_path, write_path[write_path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
                    except:
                        print('not a file')
                        self.recursive_paste_sftp(write_path, sftp)


            self.tree.delete(*self.tree.get_children())
            self.tree = self.list_files('.', self.tree, "", '.')
            self.tree.item(os.getcwd(), open=True)

    def recursive_paste(self, path):
        os.mkdir(path)
        dirs = [f for f in listdir(self.copy_path) if not isfile(join(self.copy_path, f))]
        files = [f for f in listdir(self.copy_path) if isfile(join(self.copy_path, f))]
        for f in files:
            with open(path+'/'+f, 'w') as f_out:
                with open(self.copy_path+'/'+f, 'r') as f_in:
                    text = f_in.read()
                    f_out.write(text)
        for d in dirs:
            self.recursive_paste(path+'/'+d)

    def recursive_paste_sftp(self, path, sftp):
        sftp.mkdir(path[path.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
        dirs = [path+'/'+f for f in listdir(path) if not isfile(join(path, f))]
        files = [path+'/'+f for f in listdir(path) if isfile(join(path, f))]
        print(dirs)
        print(files)
        for f in files:
            sftp.put(f, f[f.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):])
        for d in dirs:
            self.recursive_paste(d, sftp)

    def read_config(self):
        with open(self.meringue_path + '/data/meringue_config.ini', 'r') as f_in:
            self.lines = f_in.read().split('\n')
            self.highlight_foreground = self.lines[0].split('=')[1]
            self.highlight_foreground = self.highlight_foreground[:7]
            self.highlight_background = self.lines[1].split('=')[1]
            self.highlight_background = self.highlight_background[:7]
            self.highlight_keyword = self.lines[2].split('=')[1]
            self.highlight_keyword = self.highlight_keyword[:7]
            self.highlight_function_name = self.lines[3].split('=')[1]
            self.highlight_function_name = self.highlight_function_name[:7]
            self.highlight_function = self.lines[4].split('=')[1]
            self.highlight_function = self.highlight_function[:7]
            self.highlight_boolean = self.lines[5].split('=')[1]
            self.highlight_boolean = self.highlight_boolean[:7]
            self.highlight_string = self.lines[6].split('=')[1]
            self.highlight_string = self.highlight_string[:7]
            self.highlight_number = self.lines[7].split('=')[1]
            self.highlight_number = self.highlight_number[:7]
            self.highlight_operator = self.lines[8].split('=')[1]
            self.highlight_operator = self.highlight_operator[:7]
            #self.highlight_normal = self.lines[9].split('=')[1]
            self.highlight_comment = self.lines[9].split('=')[1]
            self.highlight_comment = self.highlight_comment[:7]
            self.foreground = self.lines[10].split('=')[1]
            self.foreground = self.foreground[:7]
            self.background = self.lines[11].split('=')[1]
            self.background = self.background[:7]
            self.file_color = self.lines[12].split('=')[1]
            self.file_color = self.file_color[:7]
            self.dir_color = self.lines[13].split('=')[1]
            self.dir_color = self.dir_color[:7]
            self.line_num_color = self.lines[14].split('=')[1]
            self.line_num_color = self.line_num_color[:7]
            self.line_num_background_color = self.lines[15].split('=')[1]
            self.line_num_background_color = self.line_num_background_color[:7]
            self.file_bar_color = self.lines[16].split('=')[1]
            self.file_bar_color = self.file_bar_color[:7]
            self.file_bar_text_color = self.lines[17].split('=')[1]
            self.file_bar_text_color = self.file_bar_text_color[:7]
            self.notebook_background = self.lines[18].split('=')[1]
            self.notebook_background = self.notebook_background[:7]
            self.folder = self.lines[19].split('=')[1]
        if not self.folder:
            self.folder = askdirectory()
            self.lines[19] = self.lines[19][:self.lines[19].find('=')+1]+self.folder
        self.write_config()
        try:
            os.chdir(self.folder)
        except:
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
                    sftp.put(item+'/'+name,item[item.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):]+'/'+name)
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
                    sftp.mkdir(item[item.find(self.meringue_path + '/local/') + len(self.meringue_path + '/local/'):]+'/'+name)
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
        self.directory_menu.add_command(label="Copy", command=self.copy_file)
        self.directory_menu.add_command(label="Paste", command=self.paste_file)
        self.directory_menu.add_command(label='New File', command=self.new_file)
        self.directory_menu.add_command(label='New Folder', command=self.new_folder)
        #self.directory.menu.add_command(label='Copy', command=self.copy_item)
        #self.directory.menu.add_command(label='Paste', command=self.paste_item)


    def write_config(self):
        print('writing')
        with open(self.meringue_path + '/data/meringue_config.ini', 'w') as f_out:
            for line in self.lines:
                f_out.write(line + '\n')
            f_out.flush()

    def __init__(self):
        self.meringue_path = os.path.realpath(__file__)
        if os.name == 'nt':
            self.meringue_path = self.meringue_path[:self.meringue_path.rfind('\\') + 1]
        else:
            self.meringue_path = self.meringue_path[:self.meringue_path.rfind('/') + 1]
        print(self.meringue_path)
        sys.stdout.flush()
        #os.chdir(os.path.join(os.path.expanduser('~'), 'Documents'))
        self.root = Tk()
        img = PhotoImage(file=self.meringue_path + 'icon.gif')
        self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        #self.root.iconbitmap(self.meringue_path + '/' + 'icon.gif')
        self.eds = []
        self.n = ttk.Notebook(self.root)
        self.menubar = Menu(self.root)
        self.tab_names = []
        self.find_string = ''
        self.find_counter = 0
        self.copy_path = ''
        self.selected_file_dir = ''
        self.tree_array = []
        self.remote_tree_array = []
        self.remote_tree_file_array = []
        self.editing_pi = False
        self.username = ''
        self.password = ''
        self.ip = ''
        self.port = 22
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
        try:
            if os.name == 'posix':
                os.makedirs(self.meringue_path+'local')
            else:
                os.makedirs(self.meringue_path.replace('\\', '/')+'local')
        except:
            pass
        if os.name == 'posix':
            self.recursive_delete(self.meringue_path+'local')
        else:
            self.recursive_delete(self.meringue_path.replace('\\', '/')+'local')
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
                pass

def __main__(self):
    App()

def main():
    App()

if __name__ == '__main__':
    main()
