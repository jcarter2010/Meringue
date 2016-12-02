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

class EditorClass(object):

    UPDATE_PERIOD = 100 #ms
    editors = []
    updateId = None
    #keyword_python =
    def __init__(self, master, filename, parent):
        self.multiline = False
        self.past_keys = [None, None, None]
        self.parent = parent
        self.keywords_bash = ['if','then','else','elif','fi','case','esac','for','select','while','until','do','done','in','function','time','coproc']
        self.keywords_java = ['abstract','continue','for','new','switch','assert','default','goto','package','synchronized','boolean','do','if','private','this','break','double','implements','protected','throw','byte','else','import','public','throws','case','enum','instanceof','return','transient','catch','extends','int','short','try','char','final','interface','static','void','class','finally','long','strictfp','volatile','const','float','native','super','while','String','Integer','Double','Boolean']
        self.__class__.editors.append(self)
        self.fname = filename
        self.lineNumbers = ''
        self.words = []
        # A frame to hold the three components of the widget.
        self.frame = Frame(master, bd=2, relief=SUNKEN)
        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)
        self.hScrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hScrollbar.pack(fill='x', side=BOTTOM)
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
                foreground = 'blue',
                wrap = NONE
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)
        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.yview)
        self.hScrollbar.config(command=self.xview)
        if self.__class__.updateId is None:
            self.updateAllLineNumbers()
        self.text.bind('<KeyRelease>', self.syntax_coloring_after_type)
        #self.text.bind('<4>', self.update_display)
        #self.text.bind('<5>', self.update_display)
        self.text.bind('<Tab>', self.tab)
        try:
            self.text.bind('<ISO_Left_Tab>', self.reverse_tab)
        except:
            self.text.bind('<Shift-KeyPress-Tab>', self.reverse_tab)
        self.text.bind('<Return>', self.enter)
        self.text.bind('<Escape>', self.remove_highlight)
        self.text.bind('<Control-q>', self.highlight_variable)
        self.text.bind('<Control-z>', self.undo)
        self.text.bind('<space>', self.syntax_coloring_after_type)
        #self.text.bind('<MouseWheel>', self.syntax_coloring)
        #self.text.bind('<1>', self.syntax_coloring)

    def undo(self, event):
        self.text.edit_undo()
        self.syntax_coloring_after_type(event)

    def redo(self, event):
        self.text.edit_redo()
        self.syntax_coloring_after_type(event)

    def add_word(self, event):
        pass

    def update_display(self, event):
        start=self.text.index('@0,0')
        end=self.text.index('@0,%d' % self.text.winfo_height())

        self.parent.update_display(start, end)

    def yview(self, *args):
        self.text.yview(*args)

    def xview(self, *args):
        self.text.xview(*args)

    def enter(self, event):
        start = float(int(float(self.text.index(INSERT))))
        s = self.text.get(str(start), str(int(start))+'.1000')
        indent = re.match(r"\s*", s).group()
        self.text.insert(INSERT, '\n' + indent)
        self.syntax_coloring_after_type(event)
        return 'break'

    def tab(self, event):
        try:
            self.text.edit_separator()

            start = '1.0'
            end = END
            #start=self.text.index('@0,0')
            #end=self.text.index('@0,%d' % self.text.winfo_height())
            content = self.text.get(start, end)
            l_c = content.split('\n')
            t = self.text.selection_get()
            l = t.split('\n')
            start_line = int(str(self.find_selection()))
            end_line = 0
            start_index = int(start[:start.find('.')])
            counter = start_index
            #found_start = False
            found_end = False
            for line in l_c:
                if l[len(l) - 1] in line and counter > start_line and found_end == False:
                    end_line = counter
                    found_end = True
                counter = counter + 1
            for i in range(start_line - start_index, end_line + 1 - start_index):
                l_c[i] = '    ' + l_c[i]
            l_fin = '\n'.join(l_c)
            #l_fin = []
            #for line in l:
            #    l_fin = '    ' + l
            self.text.delete(start, end)
            self.text.insert(start, l_fin)
            self.syntax_coloring_after_type(event)
        except:
            self.text.insert(INSERT, " " * 4)
        return 'break'

    def reverse_tab(self, event):
        try:

            self.text.edit_separator()

            start = '1.0'
            end = END
            #start=self.text.index('@0,0')
            #end=self.text.index('@0,%d' % self.text.winfo_height())
            content = self.text.get(start, end)
            l_c = content.split('\n')
            t = self.text.selection_get()
            l = t.split('\n')
            start_line = int(str(self.find_selection()))
            end_line = 0
            start_index = int(start[:start.find('.')])
            counter = start_index
            found_end = False
            for line in l_c:
                if l[len(l) - 1] in line and counter > start_line and found_end == False:
                    end_line = counter
                    found_end = True
                counter = counter + 1
            for i in range(start_line - start_index, end_line + 1 - start_index):
                if l_c[i].startswith('    '):
                    l_c[i] = l_c[i].replace('    ', '', 1)
            l_fin = '\n'.join(l_c)
            self.text.delete(start, end)
            self.text.insert(start, l_fin)
            self.syntax_coloring_after_type(event)
        except:
            self.text.insert(INSERT, " " * 4)
        return 'break'

    def find_selection(self):
        pattern = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        tag = "highlight"
        start = tk.SEL_FIRST
        end = tk.SEL_LAST
        self.text.mark_set("matchStart", start)
        self.text.mark_set("matchEnd", start)
        self.text.mark_set("searchLimit", end)
        count = tk.IntVar()
        while True:
            index = self.text.search(pattern, "matchEnd", "searchLimit", count=count, regexp=False)
            if index == "": break
            if count.get() == 0: break
            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            #print(index)
            #print(count.get())
            return(index[:index.find('.')])
        #    self.text.tag_add(tag, "matchStart", "matchEnd")
        #print(start)


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

    def return_function_names(self, parent):
        function_names = []
        start = '1.0'
        end = END
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
                #self.text.tag_add(tag, "matchStart", "matchEnd")
                function_names.append(self.text.get("matchStart", "matchEnd"))
        parent.function_list = function_names

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
        self.text.tag_remove('comment', start, end)
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
        #self.highlight_functions_and_variables(start, end, event)
        self.highlight_True_False(start, end, event)
        self.highlight_operators(start, end, event)
        self.highlight_strings(start, end, event)
        self.highlight_comments(start, end, event)
        self.highlight_multiline_comments(start, end, event)

    def syntax_coloring_after_type(self, event):
        self.past_keys.pop(0)
        self.past_keys.append(event.char)
        self.sc(event)
        '''
        #start=self.text.index('@0,0')
        #end=self.text.index('@0,%d' % self.text.winfo_height())
        start = self.text.index("insert linestart")
        end = self.text.index("insert lineend")

        self.remove_all_tags(start, end, event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        self.highlight_numbers(start, end, event)
        self.highlight_keywords(start, end, event)
        self.highlight_function_names(start, end, event)
        #self.highlight_functions_and_variables(start, end, event)
        self.highlight_True_False(start, end, event)
        self.highlight_operators(start, end, event)
        self.highlight_strings(start, end, event)
        self.highlight_comments(start, end, event)
        self.highlight_multiline_comments(start, end, event)
        '''

    def sc(self, event):
        text = self.text.get(1.0, END)
        lines = text.split('\n')
        start = self.text.index("insert linestart")
        end = self.text.index("insert lineend")
        line = self.text.get(start, end)
        row_txt = self.text.index(start)
        row = int(row_txt[:row_txt.find('.')])
        start = self.text.index("{}.0 lineend".format(row - 1))
        end = self.text.index("{}.0 linestart".format(row + 1))

        if self.multiline:
            if (self.past_keys[0] == "'" and self.past_keys[1] == "'" and self.past_keys[2] == "'"):
                column = -1
                r = row
                for i in range(row, 0, -1):
                    l = lines[i]
                    if i == row:
                        l = l[:-3]
                    c = l.rfind("'''")
                    if c != -1:
                        r = i
                        break
                idx = '{}.{}'.format(r, c)
                self.remove_all_tags(idx, end, event)
                self.highlight_numbers(idx, end, event)
                self.highlight_keywords(idx, end, event)
                self.highlight_numbers(idx, end, event)
                self.highlight_keywords(idx, end, event)
                self.highlight_function_names(idx, end, event)
                self.highlight_True_False(idx, end, event)
                self.highlight_operators(idx, end, event)
                self.highlight_strings(idx, end, event)
                self.highlight_comments(idx, end, event)
                self.highlight_multiline_comments(idx, end, event)
                self.multiline = False
            if (self.past_keys[0] == '"' and self.past_keys[1] == '"' and self.past_keys[2] == '"'):
                column = -1
                r = row
                for i in range(row, 0, -1):
                    l = lines[i]
                    if i == row:
                        l = l[:-3]
                    c = l.rfind('"""')
                    if c != -1:
                        r = i
                        break
                idx = '{}.{}'.format(r, c)
                self.remove_all_tags(idx, end, event)
                self.highlight_numbers(idx, end, event)
                self.highlight_keywords(idx, end, event)
                self.highlight_numbers(idx, end, event)
                self.highlight_keywords(idx, end, event)
                self.highlight_function_names(idx, end, event)
                self.highlight_True_False(idx, end, event)
                self.highlight_operators(idx, end, event)
                self.highlight_strings(idx, end, event)
                self.highlight_comments(idx, end, event)
                self.highlight_multiline_comments(idx, end, event)
                self.multiline = False
        else:
            if (self.past_keys[0] == "'" and self.past_keys[1] == "'" and self.past_keys[2] == "'") or \
                (self.past_keys[0] == '"' and self.past_keys[1] == '"' and self.past_keys[2] == '"'):
                self.multiline = True
            else:
                self.remove_all_tags(start, end, event)
                self.highlight_numbers(start, end, event)
                self.highlight_keywords(start, end, event)
                self.highlight_numbers(start, end, event)
                self.highlight_keywords(start, end, event)
                self.highlight_function_names(start, end, event)
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
        first_index = None
        first = True
        while True:
            index = self.text.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break
            if first:
                first_index = index
                first = False
            self.text.mark_set("matchStart", index)
            self.counttext.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_add(tag, "matchStart", "matchEnd")
            if counter == 0:
            	self.text.see(index)
            counter = counter + 1
        if first_index != None:
            self.syntax_coloring(None)
            self.text.see(first_index)

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
                self.syntax_coloring(None)
                self.text.see(index)
            counter = counter + 1

    def highlight_keywords(self, start, end, event):
        if self.fname.endswith('.py') or self.fname.endswith('.sh') or self.fname.endswith('.java'):
            tag = 'keyword'
            regexp=True
            keywords = []
            if self.fname.endswith('.py'):
                keywords = keyword.kwlist
            if self.fname.endswith('.sh'):
                keywords = self.keywords_bash
            if self.fname.endswith('.java'):
                keywords = self.keywords_java
            for pattern in keywords:
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
        if self.fname.endswith('.java') or self.fname.endswith('.sh'):
            tag = 'function_name'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\\S+\\(', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                index = arr[0] + '.' + str(int(arr[1]))
                count_temp = str(int(count.get()) - 1)
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_functions_and_variables(self, start, end, event):
        if self.fname.endswith('.py') or self.fname.endswith('.java'):
            tag = 'function'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\\..*', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                index = arr[0] + '.' + str(int(arr[1]) + 1)
                count_temp = str(int(count.get()) - 2)
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count_temp))
                self.text.tag_add(tag, "matchStart", "matchEnd")
        if self.fname.endswith('.sh'):
            tag = 'function'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\\$\\S+', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                index = arr[0] + '.' + str(int(arr[1]))
                count_temp = str(int(count.get()))
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
        if self.fname.endswith('.py') or self.fname.endswith('.java') or self.fname.endswith('.sh'):
            tag = 'operator'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('[\\(\\)\\+\\\\\-\\*\\/\\.\\]\\[\\=\\!\\{\\}\\<\\>\\;\\:]', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_comments(self, start, end, event):
        if self.fname.endswith('.py') or self.fname.endswith('.sh'):
            tag = 'comment'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('([ ]|^|[\'\"])#.*\n', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")
        if self.fname.endswith('.java'):
            tag = 'comment'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('[^\'\"]\\/\\/.*\n', "matchEnd", "searchLimit", count=count, regexp=regexp)
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
                index = self.text.search('\"\"\"(.|\n)*\"\"\"', "matchEnd", "searchLimit", count=count, regexp=regexp)
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
        if self.fname.endswith('.java'):
            tag = 'comment'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search("\\/\\*\\*(.|\n)*\\*\\*\\/", "matchEnd", "searchLimit", count=count, regexp=regexp)
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
                index = self.text.search("\\/\\*(.|\n)*\\*\\/", "matchEnd", "searchLimit", count=count, regexp=regexp)
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
        if self.fname.endswith('.java') or self.fname.endswith('.sh'):
            tag = 'boolean'
            regexp=True
            start = self.text.index(start)
            end = self.text.index(end)
            self.text.mark_set("matchStart", start)
            self.text.mark_set("matchEnd", start)
            self.text.mark_set("searchLimit", end)
            count = tk.IntVar()
            while True:
                index = self.text.search('\ytrue\y', "matchEnd", "searchLimit", count=count, regexp=regexp)
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
                index = self.text.search('\yfalse\y', "matchEnd", "searchLimit", count=count, regexp=regexp)
                if index == "": break
                arr = index.split('.')
                count_temp = str(int(count.get()) - 5)
                if count.get() == 0: break
                self.text.mark_set("matchStart", index)
                self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.text.tag_add(tag, "matchStart", "matchEnd")

    def highlight_strings(self, start, end, event):
        if self.fname.endswith('.py') or self.fname.endswith('.sh'):
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
        if self.fname.endswith('.java'):
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

    def remove_highlight(self, event):
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
