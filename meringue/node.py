from Tkinter import *

class node:
    def __init__(self, name, parent, indent, path, tag, textFrame, application):
        self.name = name
        self.parent = parent
        self.indent = indent
        self.path = path
        self.children = []
        self.tag = tag
        self.name_label = Label(textFrame, text=name)
        if tag == 'folder':
            icon_image = PhotoImage(file='./resources/folder_image.gif')
        else:
            icon_image = PhotoImage(file='./resources/file_image.gif')
        self.image_label = Label(textFrame, image=icon_image)
        self.image_label.photo = icon_image
        self.display_children = False
        if tag == 'folder':
            self.name_label.bind("<Double-Button-1>", self.double_click_folder)
            self.image_label.bind("<Double-Button-1>", self.double_click_folder)
        if tag == 'file':
            self.name_label.bind("<Double-Button-1>", self.double_click_file)
            self.image_label.bind("<Double-Button-1>", self.double_click_file)
        self.application = application

    def double_click_folder(self, event):
        self.display_children = not self.display_children
        self.application.refresh_tree()

    def double_click_file(self, event):
        print('open file')
