
from Tkinter import *
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
from tkFileDialog import askdirectory
import tkFont as font
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
from pygments.lexers.python import PythonLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.html import XmlLexer
from pygments.lexers.templates import HtmlPhpLexer
from pygments.lexers.perl import Perl6Lexer
from pygments.lexers.ruby import RubyLexer
from pygments.lexers.configs import IniLexer
from pygments.lexers.configs import ApacheConfLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.diff import DiffLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.sql import MySqlLexer
from pygments.styles import get_style_by_name

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
        self.lexer = self.get_lexer(filename)
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
        self.control = False
        self.text.bind('<Key>', self.syntax_coloring_after_type)
        self.text.bind('<KeyRelease>', self.key_release)
        self.text.bind('<Tab>', self.tab)
        try:
            self.text.bind('<ISO_Left_Tab>', self.reverse_tab)
        except:
            self.text.bind('<Shift-KeyPress-Tab>', self.reverse_tab)
        self.text.bind('<Control_L>', self.control_down)
        self.text.bind('<Return>', self.enter)
        self.text.bind('<Escape>', self.remove_highlight)
        self.text.bind('<Control-q>', self.highlight_variable)
        self.text.bind('<Control-z>', self.undo)
        self.text.bind('<Control-r>', self.syntax_coloring)
        self.text.bind('<space>', self.syntax_coloring_after_type)
        self.create_tags()

    def control_up(self, event):
        self.control = False

    def control_down(self, event):
        self.control = True

    def get_lexer(self, filename):
        extens = filename[filename.rfind('.') + 1:]
        print(extens)
        if extens == "py" or extens == "pyw" or extens == "sc" or extens == "sage" or extens == "tac":
            lexer = PythonLexer()
        elif extens == "txt" or extens == "README" or extens == "text":
            lexer = TextLexer()
        elif extens == "htm" or extens == "html" or extens == "css" or extens == "js" or extens == "md":
            lexer = HtmlLexer()
        elif extens == "xml" or extens == "xsl" or extens == "rss" or extens == "xslt" or extens == "xsd" or extens == "wsdl" or extens == "wsf":
            lexer = XmlLexer()
        elif extens == "php" or extens == "php5":
            lexer = HtmlPhpLexer()
        elif extens == "pl" or extens == "pm" or extens == "nqp" or extens == "p6" or extens == "6pl" or extens == "p6l" or extens == "pl6" or extens == "pm" or extens == "p6m" or extens == "pm6" or extens == "t":
            lexer = Perl6Lexer()
        elif extens == "rb" or extens == "rbw" or extens == "rake" or extens == "rbx" or extens == "duby" or extens == "gemspec":
            lexer = RubyLexer()
        elif extens == "ini" or extens == "init":
            lexer = IniLexer()
        elif extens == "conf" or extens == "cnf" or extens == "config":
            lexer = ApacheConfLexer()
        elif extens == "sh" or extens == "cmd" or extens == "bashrc" or extens == "bash_profile":
            lexer = BashLexer()
        elif extens == "diff" or extens == "patch":
            lexer = DiffLexer()
        elif extens == "cs":
            lexer = CSharpLexer()
        elif extens == "sql":
            lexer = MySqlLexer()
        else:
            lexer = None
        return lexer

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
                if l[len(l) - 1] in line and counter >= start_line and found_end == False:
                    end_line = counter
                    found_end = True
                counter = counter + 1
            for i in range(start_line - start_index, end_line + 1 - start_index):
                l_c[i] = '    ' + l_c[i]
            l_fin = '\n'.join(l_c)
            l_fin = l_fin[:-1]
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
                if l[len(l) - 1] in line and counter >= start_line and found_end == False:
                    end_line = counter
                    found_end = True
                counter = counter + 1
            for i in range(start_line - start_index, end_line + 1 - start_index):
                if l_c[i].startswith('    '):
                    l_c[i] = l_c[i].replace('    ', '', 1)
            l_fin = '\n'.join(l_c)
            l_fin = l_fin[:-1]
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
            return(index[:index.find('.')])


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

    def syntax_coloring(self, event):
        self.colorize()

    def key_release(self, event):
        if event.keycode == 82:
            self.control_up(event)

    def syntax_coloring_after_type(self, event):
        if not self.control:
            self.recolorize()

    def create_tags(self):
        style = get_style_by_name('default')

        self.tag_names = []

        for ttype, ndef in style:
            self.tag_names.append(str(ttype))

        self.text.tag_configure('Token.Keyword', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Constant', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Declaration', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Namespace', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Pseudo', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Reserved', foreground=self.parent.token_keyword)
        self.text.tag_configure('Token.Keyword.Type', foreground=self.parent.token_keyword)

        self.text.tag_configure('Token.Name', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Attribute', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Builtin', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Builtin.Pseudo', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Class', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Constant', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Decorator', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Entity', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Exception', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Function', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Label', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Namespace', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Other', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Tag', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Variable', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Variable.Class', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Variable.Global', foreground=self.parent.token_name)
        self.text.tag_configure('Token.Name.Variable.Instance', foreground=self.parent.token_name)

        self.text.tag_configure('Token.Literal', foreground=self.parent.token_literal)
        self.text.tag_configure('Token.Literal.Date', foreground=self.parent.token_literal)

        self.text.tag_configure('Token.Literal.String', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Backtick', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Char', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Doc', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Double', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Escape', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Heredoc', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Interpol', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Other', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Regex', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Single', foreground=self.parent.token_string)
        self.text.tag_configure('Token.Literal.String.Symbol', foreground=self.parent.token_string)

        self.text.tag_configure('Token.Literal.Number', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Bin', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Float', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Hex', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Integer', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Integer.Long', foreground=self.parent.token_number)
        self.text.tag_configure('Token.Literal.Number.Oct', foreground=self.parent.token_number)

        self.text.tag_configure('Token.Operator', foreground=self.parent.token_operators)
        self.text.tag_configure('Token.Operator.Word', foreground=self.parent.token_operators)

        self.text.tag_configure('Token.Punctuation', foreground=self.parent.token_punctuation)

        self.text.tag_configure('Token.Comment', foreground=self.parent.token_comments)
        self.text.tag_configure('Token.Comment.Hashbang', foreground=self.parent.token_comments)
        self.text.tag_configure('Token.Comment.Multiline', foreground=self.parent.token_comments)
        self.text.tag_configure('Token.Comment.Preproc', foreground=self.parent.token_comments)
        self.text.tag_configure('Token.Comment.Single', foreground=self.parent.token_comments)
        self.text.tag_configure('Token.Comment.Special', foreground=self.parent.token_comments)

        self.text.tag_configure('Token.Generic', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Deleted', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Emph', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Error', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Heading', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Inserted', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Output', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Prompt', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Strong', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Subheading', foreground=self.parent.token_generic)
        self.text.tag_configure('Token.Generic.Traceback', foreground=self.parent.token_generic)

    def recolorize(self):
        if self.lexer != None:

            insert_index = self.text.index(INSERT)
            row = int(insert_index[:insert_index.find('.')]) - 1
            start = '{}.0'.format(row)
            end = '{}.0'.format(row + 2)

            column = 0
            start_line = 1
            start_index = column
            end_line = 1
            end_index = column

            code = self.text.get(start, end)
            tokensource = self.lexer.get_tokens(code)

            for ttype, value in tokensource:
                if "\n" in value:
                    end_line += value.count("\n")
                    end_index = len(value.rsplit("\n",1)[1])
                else:
                    end_index += len(value)

                if value not in (" ", "\n"):
                    index0 = "%s.%s" % (start_line + row - 1, start_index - 1)
                    index1 = "%s.%s" % (start_line + row - 1, start_index)
                    index2 = "%s.%s" % (end_line + row - 1, end_index)

                    for tagname in self.text.tag_names(index0):

                        self.text.tag_remove(tagname, index1, index2)

                    self.text.tag_add(str(ttype), index1, index2)

                start_line = end_line
                start_index = end_index

    def colorize(self):
        if self.lexer != None:

            self.text.tag_ranges('Token.Literal.String.Doc')

            for tag in self.tag_names:
                indices = self.text.tag_ranges(tag)
                for i in range(0, len(indices), 2):
                    self.text.tag_remove(tag, indices[i], indices[i + 1])


            code = self.text.get("1.0", "end-1c")
            tokensource = self.lexer.get_tokens(code)
            start_line=1
            start_index = 0
            end_line=1
            end_index = 0

            for ttype, value in tokensource:
                if "\n" in value:
                    end_line += value.count("\n")
                    end_index = len(value.rsplit("\n",1)[1])
                else:
                    end_index += len(value)

                if value not in (" ", "\n"):
                    index0 = "%s.%s" % (start_line, start_index - 1)
                    index1 = "%s.%s" % (start_line, start_index)
                    index2 = "%s.%s" % (end_line, end_index)

                    self.text.tag_add(str(ttype), index1, index2)

                start_line = end_line
                start_index = end_index

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
