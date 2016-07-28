#!/usr/bin/env python

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
from subprocess import Popen
from subprocess import PIPE
#from tkMessageBox import *
import keyword
from multiprocessing import Process


class find_and_replace_dialog:

    def find(self):
        self.parent_obj.find(self.entryWidget.get())

    def find_one(self):
        self.parent_obj.find_one(self.entryWidget.get())

    def replace(self):
        self.parent_obj.replace(self.entryWidget.get(), self.entryWidget2.get())

    def replace_all(self):
        self.parent_obj.replace_all(self.entryWidget.get(), self.entryWidget2.get())

    def end(self):
        self.parent_obj.reset_counters()
        self.find_string = '!!END!!'
        self.top.destroy()

    def __init__(self, parent, parent_obj):

        top = self.top = Toplevel(parent)

        self.textFrame = Frame(top)

        self.entryLabel = Label(self.textFrame)
        self.entryLabel["text"] = "Find:"
        self.entryLabel.pack()

        self.entryWidget = Entry(self.textFrame)
        self.entryWidget["width"] = 50
        self.entryWidget.pack()

        self.entryLabel2 = Label(self.textFrame)
        self.entryLabel2["text"] = "Replace:"
        self.entryLabel2.pack()

        self.entryWidget2 = Entry(self.textFrame)
        self.entryWidget2["width"] = 50
        self.entryWidget2.pack()

        self.textFrame.pack()

        self.button = Button(top, text="Find All", command=self.find)
        self.button.pack()

        self.button1 = Button(top, text="Find Next", command=self.find_one)
        self.button1.pack()

        self.button2 = Button(top, text="Replace", command=self.replace)
        self.button2.pack()

        self.button3 = Button(top, text="Replace All", command=self.replace_all)
        self.button3.pack()

        self.button4 = Button(top, text="Done", command=self.end)
        self.button4.pack()

        self.parent_obj = parent_obj

        #self.root.mainloop()

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
        self.text.bind('<Key>', self.syntax_coloring_after_type)
        #self.text.bind('<4>', self.syntax_coloring)
        #self.text.bind('<5>', self.syntax_coloring)
        self.text.bind('<Tab>', self.tab)
        self.text.bind('<Return>', self.enter)
        self.text.bind('<Escape>', self.remove_highlight)
        self.text.bind('<Control-q>', self.highlight_variable)
        #self.text.bind('<MouseWheel>', self.syntax_coloring)
        #self.text.bind('<1>', self.syntax_coloring)

    def enter(self, event):
        start = float(int(float(self.text.index(INSERT))))
        s = self.text.get(str(start), str(int(start))+'.1000')
        indent = re.match(r"\s*", s).group()
        self.text.insert(INSERT, '\n' + indent)
        return 'break'

    def tab(self, event):
        self.text.insert(INSERT, " " * 4)
        return 'break'

    def getLineNumbers(self):
        x = 0
        line = '0'
        col= ''
        ln = ''
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

    def remove_all_tags(self, start, end, event):
        self.text.tag_remove('string', start, end)
        self.text.tag_remove('boolean', start, end)
        self.text.tag_remove('operator', start, end)
        self.text.tag_remove('number', start, end)
        #self.text.tag_remove('highlight', '1.0', END)
        self.text.tag_remove('function', start, end)
        self.text.tag_remove('keyword', start, end)
        self.text.tag_remove('function_name', start, end)

    def syntax_coloring(self, event):
        start = '1.0'
        end = END
        self.remove_all_tags(start, end, event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        #self.remove_all_tags(event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        self.highlight_function_names(start, end, event)
        self.highlight_functions(start, end, event)
        self.highlight_True_False(start, end, event)
        self.highlight_operators(start, end, event)
        self.highlight_strings(start, end, event)
        self.highlight_comments(start, end, event)
        self.highlight_multiline_comments(start, end, event)

    def syntax_coloring_after_type(self, event):
        start=self.text.index('@0,0')
        end=self.text.index('@0,%d' % self.text.winfo_height())
        self.remove_all_tags(start, end, event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        self.highlight_function_names(start, end, event)
        self.highlight_functions(start, end, event)
        self.highlight_True_False(start, end, event)
        self.highlight_operators(start, end, event)
        self.highlight_strings(start, end, event)
        self.highlight_comments(start, end, event)
        self.highlight_multiline_comments(start, end, event)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        self.remove_highlight(None)
        start = self.text.index(start)
        end = self.text.index(end)
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)
        count = tk.IntVar()
        counter = 0
        while True:
            index = self.text.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_add(tag, "matchStart", "matchEnd")
            if counter == 0:
            	self.text.see(index)
            counter = counter + 1
        self.syntax_coloring(None)

    def highlight_one(self, pattern, tag, c, start="1.0", end="end", regexp=False):
        self.remove_highlight(None)
        start = self.text.index(start)
        end = self.text.index(end)
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)
        count = tk.IntVar()
        counter = 0
        while True:
            index = self.text.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            if counter == c:
                self.text.tag_add(tag, "matchStart", "matchEnd")
                self.text.see(index)
            counter = counter + 1
        self.syntax_coloring(None)

    def highlight_keywords(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'keyword'
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
                    if count.get() == 0: break
                    self.text.mark_set("matchStart", index)
                    self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                    self.text.tag_add(tag, "matchStart", "matchEnd")
                    self.text.see(index)

    def highlight_function_names(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'function_name'
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
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_functions(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'function'
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
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_numbers(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'number'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('[^a-zA-Z](\d+)', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_operators(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'operator'
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
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_comments(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'comment'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('[^\'\"]#.*\n', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_multiline_comments(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'comment'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\"\"\".*\"\"\"', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_remove("matchStart", "matchEnd")
                self.text.tag_add(tag, "matchStart", "matchEnd")
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search("\'\'\'(.|\n)*\'\'\'", "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_remove("matchStart", "matchEnd")
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_True_False(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'boolean'
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
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\yFalse\y', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                count_temp = str(int(count.get()) - 5)
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_strings(self, start, end, event):
        if self.fname.endswith('.py'):
            tag = 'string'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search(r'"(.*?)"', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search(r"'(.*?)'", "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def remove_highlight(self, start, end, event):
        self.text.tag_remove('highlight', '1.0', END)

    def highlight_variable(self, event):
        pattern = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        tag = "highlight"
        start = self.text.index('1.0')
        end = self.text.index(END)
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)
        count = tk.IntVar()
        while True:
            index = self.text.search('".*(?:'+pattern+').*"|('+pattern+')', "matchEnd", "searchLimit", count=count, regexp=True)
            if index == "": break
            if count.get() == 0: break
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_add(tag, "matchStart", "matchEnd")

class Tree_Node:
    global name
    global nodes

    def __init__(self, n):
        self.name = n
        self.nodes = []

class App:

    def open_file(self, path):
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
                ed.text.tag_configure('normal', foreground=self.highlight_normal)
                ed.text.tag_configure('comment', foreground=self.highlight_comment)
                #ed.text.event_generate("<Key>", when='tail')
                ed.syntax_coloring(None)
                #ed.color()
                self.eds.append(ed)
            self.n.select(self.tab_names.index(path))

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
        #self.folder = item
        #self.lines[11] = self.lines[11][:self.lines[11].find('=')+1]+self.folder
        #self.write_config()
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
        args = ['python2', 'open_file.py']
        p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
        p.wait()
        out = p.stdout.read().replace('\n', '')
        if out.startswith('./') == False:
            out ='./' + out
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
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)

    def save_type(self, event):
        path = self.n.tab(self.n.select())['text']
        index = self.n.tabs().index(self.n.select())
        print(self.eds[index].text.get("1.0",END))
        with open(path, 'w') as f_out:
            f_out.write(self.eds[index].text.get("1.0",END))
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)

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
            print(self.folder)

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
        path, found = self.find_path('.', self.tree_array, item)
        if found:
            args = ['python2', self.merengue_path + '/' + 'rename.py', 'test']
            p = Popen(args, stdin=PIPE, stdout=PIPE, shell=False)
            p.wait()
            out = p.stdout.read().replace('\n', '')
            if not out == '!!DO NOT RENAME!!':
                i = path.rfind('/')
                print(i)
                try:
                    if i != -1:
                        os.rename(path, path[:path.rfind('\\')]+'\\'+out)
                    else:
                        os.rename(path, out)
                except:
                    print('file does not exist, not renaming anything but the tab')
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)

    def delete_file(self):
        item = self.tree.selection()[0]
        try:
            os.remove(item)
        except:
            print('Not a file')
        try:
            os.rmdir(item)
        except:
            print('Not a directory')
        self.tree.delete(*self.tree.get_children())
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)

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

    def start(self, noOfEditors, noOfLines):
        self.read_config()
        self.pane = PanedWindow(self.n, orient=HORIZONTAL, opaqueresize=True)
        ed = EditorClass(self.root, 'untitled')
        ed.text.config(insertbackground='white')
        ed.text.tag_configure("highlight", background=self.highlight_background, foreground=self.highlight_foreground)
        ed.text.tag_configure("keyword", foreground=self.highlight_keyword)
        ed.text.tag_configure("function_name", foreground=self.highlight_function_name)
        ed.text.tag_configure("function", foreground=self.highlight_function)
        ed.text.tag_configure("boolean", foreground=self.highlight_boolean)
        ed.text.tag_configure("string", foreground=self.highlight_string)
        ed.text.tag_configure("number", foreground=self.highlight_number)
        ed.text.tag_configure("operator", foreground=self.highlight_operator)
        ed.text.tag_configure('normal', foreground=self.highlight_normal)
        ed.text.tag_configure('comment', foreground=self.highlight_comment)
        self.pane.add(ed.frame)
        self.eds.append(ed)
        self.tree_frame = Frame(self.root, width=200)
        self.tree = ttk.Treeview(self.tree_frame)
        #self.tree["columns"]=("Files_and_Folders")
        self.tree = self.list_files('.', self.tree, "", '.')
        self.tree.item(os.getcwd(), open=True)
        self.tree.tag_configure('directory', background='black', foreground='magenta')
        self.tree.tag_configure('file', background='black', foreground='lime')
        ttk.Style().configure("Treeview", fieldbackground="#000000")
        self.treeScroll = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.treeScroll.configure(command=self.tree.xview)
        self.treeScroll.pack(side=TOP, fill=X)
        self.tree.configure(xscrollcommand=self.treeScroll.set)
        self.tree.bind("<3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(side=LEFT, fill=BOTH)
        self.tree_frame.pack(side=LEFT, fill=BOTH)
        self.pane.configure(background='black')
        self.pane.pack(fill='both', expand=1)
        self.n.add(self.pane, text='untitled')
        self.n.bind("<Double-1>", self.tab_rename)
        self.n.pack(side=LEFT, fill='both', expand=True)
        self.tab_names.append('untitled')

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_click)
        filemenu.add_command(label="Open Folder", command=self.open_folder_click)
        filemenu.add_command(label="Save", command=self.save_click)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_click)
        self.menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About")
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        self.menubar.add_command(label="Close Tab", command=self.close_tab)

        self.root.configure(background='black')
        self.root.title("Merengue")
        self.root.bind('<Control-s>', self.save_type)
        self.root.bind('<Control-f>', self.find_type)
        self.root.bind('<Escape>', self.end_find)
        #self.root.bind("<Configure>", self.configure)
        self.root['bg'] = 'black'
        self.root.geometry('{}x{}'.format(600, 400))
        self.root.config(menu=self.menubar)
        #self.root.attributes("-zoomed", True)

    #def configure(self, event):
    #    print(event.width)
    #    self.n.place(x = 200, y = 0)

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
            self.highlight_normal = self.lines[9].split('=')[1]
            self.highlight_comment = self.lines[10].split('=')[1]
            self.folder = self.lines[11].split('=')[1]
        if not self.folder:
            self.folder = askdirectory()
            self.lines[11] = self.lines[11][:self.lines[11].find('=')+1]+self.folder
        self.write_config()
        print(self.folder)
        os.chdir(self.folder)

    def make_directory_menu(self, w):
        self.directory_menu = Menu(self.root, tearoff=0)
        self.directory_menu.add_command(label="Delete", command=self.delete_file)
        self.directory_menu.add_command(label="Rename", command=self.tree_rename)

    def write_config(self):
        print('writing')
        with open(self.merengue_path+'config.ini', 'w') as f_out:
            for line in self.lines:
                print(line)
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
        #lines = []
        #with open('config.ini', 'r') as f_in:
        #    lines = f_in.read().split('\n')
        #    self.folder = lines[0].split('=')[1]
        #    if not self.folder:
        #        self.folder = askdirectory()
        #        lines[0] = 'folder='+self.folder
        #with open('config.ini', 'w') as f_out:
        #    for line in lines:
        #        f_out.write(line + '\n')
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
        self.highlight_normal = ''
        self.start(1, 9999)
        self.make_directory_menu(self.root)
        self.jump_counter = 0
        self. find_counter = 0
        mainloop()

if __name__ == '__main__':
    App()
