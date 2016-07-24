#!/usr/bin/python2.7

from Tkinter import *
import Tkinter as tk
import ttk
import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen
from subprocess import PIPE
from tkMessageBox import *
import keyword


class EditorClass(object):

    UPDATE_PERIOD = 100 #ms
    editors = []
    updateId = None

    def __init__(self, master, filename):
        self.__class__.editors.append(self)
        self.fname = filename
        self.lineNumbers = ''
        # A frame to hold the three components of the widget.
        self.frame = Frame(master, bd=2, relief=SUNKEN)
        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)
        # The Text widget holding the line numbers.
        self.lnText = Text(self.frame,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'darkgrey',
                foreground = 'magenta',
                state='disabled'
        )
        self.lnText.pack(side=LEFT, fill='y')
        # The Main Text Widget
        self.text = Text(self.frame,
                width=16,
                bd=0,
                padx = 4,
                undo=True,
                background = 'black',
                foreground = 'white',
                wrap = NONE
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)
        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.text.yview)
        if self.__class__.updateId is None:
            self.updateAllLineNumbers()
        self.text.bind('<Key>', self.syntax_coloring)
        self.text.bind('<4>', self.syntax_coloring)
        self.text.bind('<5>', self.syntax_coloring)

    def getLineNumbers(self):
        x = 0
        line = '0'
        col= ''
        ln = ''
        # assume each line is at least 6 pixels high
        step = 6
        nl = '\n'
        lineMask = '    %s\n'
        indexMask = '@0,%d'
        for i in range(0, self.text.winfo_height(), step):
            ll, cc = self.text.index( indexMask % i).split('.')
            if line == ll:
                if col != cc:
                    col = cc
                    ln += nl
            else:
                line, col = ll, cc
                ln += (lineMask % line)[-5:]
        return ln

    def updateLineNumbers(self):
        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')

    @classmethod
    def updateAllLineNumbers(cls):
        if len(cls.editors) < 1:
            cls.updateId = None
            return
        for ed in cls.editors:
            ed.updateLineNumbers()
        cls.updateId = ed.text.after(
            cls.UPDATE_PERIOD,
            cls.updateAllLineNumbers)

    def syntax_coloring(self, event):
        self.highlight_numbers(event)
        #self.reset_var_names(event)
        self.highlight_keywords(event)
        self.highlight_function_names(event)
        self.highlight_functions(event)
        self.highlight_True_False(event)
        self.highlight_operators(event)
        self.highlight_strings(event)
    #def open_file(self):
    #    ext_widget.index(Tkinter.INSERT),

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        start = self.text.index(start)
        end = self.text.index(end)
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.text.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_keywords(self, event):
        if self.fname.endswith('.py'):
            tag = 'keyword'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            for pattern in keyword.kwlist:
                start = self.text.index(start)
                end = self.text.index(end)
                self.text.mark_set("matchStart", start)
                self.text.mark_set("matchEnd", start)
                self.text.mark_set("searchLimit", end)

                count = tk.IntVar()
                while True:
                    index = self.text.search('\y' + pattern + '\y', "matchEnd","searchLimit", count=count, regexp=regexp)
                    if index == "": break
                    if count.get() == 0: break # degenerate pattern which matches zero-length strings
                    self.text.mark_set("matchStart", index)
                    self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                    self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_function_names(self, event):
        if self.fname.endswith('.py'):
            tag = 'function_name'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('def .*\\(', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                index = arr[0] + '.' + str(int(arr[1]) + 4)
                count_temp = str(int(count.get()) - 5)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_functions(self, event):
        if self.fname.endswith('.py'):
            tag = 'function'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('\\..*\\(', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                index = arr[0] + '.' + str(int(arr[1]) + 1)
                count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def reset_var_names(self, event):
        if self.fname.endswith('.py'):
            tag = 'normal'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            #for i in range(0, 10):
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('[a-zA-Z\d]+', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                #arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 1)
                #count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")


    def highlight_numbers(self, event):
        if self.fname.endswith('.py'):
            tag = 'number'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            #for i in range(0, 10):
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('[^a-zA-Z](\d+)', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                #arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 1)
                #count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_operators(self, event):
        if self.fname.endswith('.py'):
            tag = 'operator'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('[\\(\\)\\+\\\\\-\\*\\/\\.\\]\\[\\=]', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                #arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 1)
                #count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_True_False(self, event):
        if self.fname.endswith('.py'):
            tag = 'boolean'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('\yTrue\y', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 4)
                #count_temp = str(int(count.get()) - 5)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('\yFalse\y', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 4)
                count_temp = str(int(count.get()) - 5)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_strings(self, event):
        if self.fname.endswith('.py'):
            tag = 'string'
            start=self.text.index('@0,0')
            end=self.text.index('@0,%d' % self.text.winfo_height())
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search('".*"', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                #arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 1)
                #count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.text.search("'.*'", "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                #arr = index.split('.')
                #index = arr[0] + '.' + str(int(arr[1]) + 1)
                #count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def remove_highlight(self, pattern, tag, start="1.0", end="end", regexp=False):
        start = self.text.index(start)
        end = self.text.index(end)
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.text.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_remove(tag, "matchStart", "matchEnd")

class Tree_Node:
    global name
    global nodes

    def __init__(self, n):
        self.name = n
        self.nodes = []

class App:

    def open_file(self, path):
        if self.check_if_file(path):
            if not path in self.tab_names:
                pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
                ed = EditorClass(self.root, path)
                pane.add(ed.frame)
                self.n.add(pane, text=path)
                self.n.pack(fill='both', expand=1)
                self.tab_names.append(path)
                ed.text.config(insertbackground='white')
                with open(path, 'r') as f_in:
                    text = f_in.read()
                    lines = text.split('\n')
                    for line in lines:
                        ed.text.insert(END, line+'\n')
                ed.text.tag_configure("highlight", background="blue", foreground='orange')
                ed.text.tag_configure("keyword", foreground='red')
                ed.text.tag_configure("function_name", foreground='yellow')
                ed.text.tag_configure("function", foreground='orange')
                ed.text.tag_configure("boolean", foreground='green')
                ed.text.tag_configure("string", foreground='magenta')
                ed.text.tag_configure("number", foreground='cyan')
                ed.text.tag_configure("operator", foreground='blue')
                ed.text.tag_configure('normal', foreground='white')
                ed.text.syntax_coloring(None)
                self.eds.append(ed)
            self.n.select(self.tab_names.index(path))

    def find_path(self, path, node, fname):
        if fname == node.name:
            return(node.name, True)
        for tree_node in node.nodes:
            path_temp, found = self.find_path(node.name, tree_node, fname)
            if found:
                path = node.name + '/' + path_temp
                return path, True
        return '', False

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

    def check_if_file(self, path):
        temp_path = path[:path.rfind('/')]
        fname = path[path.rfind('/')+1:]
        if temp_path == '':
            temp_path = '.'
        print(temp_path + '|' + path)
        files = [f for f in listdir(temp_path) if isfile(join(temp_path, f))]
        if fname in files:
            return True
        return False

    def list_files(self, path, tree, parent):
        tree.insert(parent, 3, path, text=path, tags = ('directory',))
        files = [f for f in listdir(path) if isfile(join(path, f))]
        dirs = [d for d in listdir(path) if not isfile(join(path, d))]
        tn = Tree_Node(path)
        for d in dirs:
            tree, n2 = self.list_files(d, tree, path)
            tn.nodes.append(n2)
        for f in files:
                tree.insert(path, 3, f, text=f, tags = ('file',))
                tn.nodes.append(Tree_Node(f))
        return tree, tn

    def on_double_click(self, event):
            item = self.tree.selection()[0]
            path, found = self.find_path('', self.tree_array, item)
            if found:
                self.open_file(path)

    def close_tab(self):
        index = self.n.tabs().index(self.n.select())
        self.n.forget(self.n.select())
        del(self.tab_names[index])
        del(self.eds[index])

    def open_click(self):
        args = ['python2', 'open_file.py']
        p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        p.wait()
        out = p.stdout.read().replace('\n', '')
        if not out == '!!DO NOT OPEN!!':
            try:
                self.open_file(out)
            except:
                showerror("!!ERROR!!", "File does not exist")

    def save_click(self):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        print(self.eds[index].text.get("1.0",END))
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree, self.tree_array = self.list_files('.', self.tree, "")
        self.tree.item(".", open=True)

    def save_type(self, event):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        print(self.eds[index].text.get("1.0",END))
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree, self.tree_array = self.list_files('.', self.tree, "")
        self.tree.item(".", open=True)

    def exit_click(self):
        sys.exit()

    def keyPressed(self, event):
        print "--"
        if event.keysym == 's':
            self.save_click

    def find_type(self, event):
        path = self.n.tab(self.n.select())['text']
        args = ['python2', 'find_and_replace.py']
        p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        p.wait()
        out = p.stdout.read().replace('\n', '')
        f_index = out.index('!!FIND!!')
        if f_index != -1:
            self.find_string = out[8:]
            r_index = out.find('!!REPLACE!!')
            if r_index == -1:
                for ed in self.eds:
                    ed.highlight_pattern(out[8:], "highlight")
            else:
                self.find_string = self.find_string[:self.find_string.find('!!REPLACE!!')]
                r_string = out[out.find('!!REPLACE!!') + 11:]
                index = 0
                for ed in self.eds:
                    print(self.find_string + '|' + r_string)
                    text = self.eds[index].text.get("1.0",END)
                    self.eds[index].text.delete("1.0",END)
                    text = text.replace(self.find_string, r_string)
                    self.eds[index].text.insert(END, text)
                    index = index + 1

    def tree_rename(self):
        item = self.selected_file_dir
        path, found = self.find_path('.', self.tree_array, item)
        if found:
            args = ['python2', 'rename.py', 'test']
            p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
            p.wait()
            out = p.stdout.read().replace('\n', '')
            if not out == '!!DO NOT RENAME!!':
                i = path.rfind('/')
                print(i)
                try:
                    if i != -1:
                        os.rename(path, path[:path.rfind('/')]+'/'+out)
                    else:
                        os.rename(path, out)
                except:
                    print('file does not exist, not renaming anything but the tab')
        self.tree.delete(*self.tree.get_children())
        self.tree, self.tree_array = self.list_files('.', self.tree, "")
        self.tree.item(".", open=True)

    def delete_file(self):
        item = self.selected_file_dir
        path, found = self.find_path('.', self.tree_array, item)
        if found:
            try:
                os.remove(path)
            except:
                print('Not a file')
            try:
                os.rmdir(path)
            except:
                print('Not a directory')
        self.tree.delete(*self.tree.get_children())
        self.tree, self.tree_array = self.list_files('.', self.tree, "")
        self.tree.item(".", open=True)

    def show_menu(self, event):
        #w = self.tree
        #w = e.widget
        #the_menu.entryconfigure("Cut",
        #command=lambda: w.event_generate("<<Cut>>"))
        #the_menu.entryconfigure("Copy",
        #command=lambda: w.event_generate("<<Copy>>"))
        #the_menu.entryconfigure("Paste",
        #command=lambda: w.event_generate("<<Paste>>"))
        #self.directory_menu.add_command("Delete", command=delete_file)
        #self.directory_menu.add_command("Rename", command=tree_rename)
        #self.directory_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
        self.directory_menu.post(event.x_root, event.y_root)

    def on_right_click(self, event):
        #try:
        if len(self.tree.selection()) > 0:
            self.selected_file_dir = self.tree.selection()[0]
            self.show_menu(event)
        #except:
        #    print('nothing selected')
    def tab_rename(self, event):
        path = self.n.tab(self.n.select())['text']
        args = ['python2', 'rename.py', path[path.rfind('/')+1:]]
        p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        p.wait()
        out = p.stdout.read().replace('\n', '')
        if not out == '!!DO NOT RENAME!!':
            self.n.tab(self.n.select(), text=out)

    def end_find(self, event):
        for ed in self.eds:
            ed.remove_highlight(self.find_string, "highlight")

    def start(self, noOfEditors, noOfLines):
        self.pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
        ed = EditorClass(self.root, 'untitled')
        ed.text.config(insertbackground='white')
        ed.text.tag_configure("highlight", background="blue", foreground='orange')
        ed.text.tag_configure("keyword", foreground='red')
        ed.text.tag_configure("function_name", foreground='yellow')
        ed.text.tag_configure("function", foreground='orange')
        ed.text.tag_configure("boolean", foreground='green')
        ed.text.tag_configure("string", foreground='magenta')
        ed.text.tag_configure("number", foreground='cyan')
        ed.text.tag_configure("operator", foreground='blue')
        ed.text.tag_configure('normal', foreground='white')
        self.pane.add(ed.frame)
        self.eds.append(ed)
        self.tree = ttk.Treeview(self.root)
        self.tree, self.tree_array = self.list_files('.', self.tree, "")
        self.tree.item(".", open=True)
        self.tree.tag_configure('directory', background='black', foreground='magenta')
        self.tree.tag_configure('file', background='black', foreground='lime')
        ttk.Style().configure("Treeview", fieldbackground="black")
        self.tree.bind("<3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(side=LEFT, fill=BOTH)
        self.pane.pack(fill='both', expand=1)
        self.n.add(self.pane, text='untitled')
        #self.n.bind("<3>", self.on_right_click)
        self.n.bind("<Double-1>", self.tab_rename)
        self.n.pack(fill='both', expand=1)
        self.tab_names.append('untitled')

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_click)
        filemenu.add_command(label="Save", command=self.save_click)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_click)
        self.menubar.add_cascade(label="File", menu=filemenu)
        #editmenu = Menu(self.menubar, tearoff=0)
        #editmenu.add_command(label="Cut", command=self.cut_click)
        #editmenu.add_command(label="Copy", command=self.copy_click)
        #editmenu.add_command(label="Paste", command=self.cut_click)
        #self.menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About")
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        self.menubar.add_command(label="Close Tab", command=self.close_tab)

        self.root.configure(background='black')
        self.root.title("Merengue")
        self.root.bind('<Control-s>', self.save_type)
        self.root.bind('<Control-f>', self.find_type)
        self.root.bind('<Escape>', self.end_find)
        self.root.config(menu=self.menubar)
        #w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        #self.root.overrideredirect(1)
        #self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.attributes("-zoomed", True)

    def make_directory_menu(self, w):
        self.directory_menu = Menu(self.root, tearoff=0)
        self.directory_menu.add_command(label="Delete", command=self.delete_file)
        self.directory_menu.add_command(label="Rename", command=self.tree_rename)

    def __init__(self):
        self.root = Tk()
        self.eds = []
        self.n = ttk.Notebook(self.root)
        self.menubar = Menu(self.root)
        self.tab_names = []
        self.find_string = ''
        self.selected_file_dir = ''
        self.tree_array = []
        self.start(1, 9999)
        self.make_directory_menu(self.root)
        mainloop()

if __name__ == '__main__':
    path = os.path.abspath(__file__)
    print(path)
    App()
