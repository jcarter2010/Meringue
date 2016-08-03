#this needs to be compltely redone, it's a stupid way of doing things and so I'm going to change this entire thing

try:
    from Tkinter import *
    import Tkinter as tk
except:
    from tkinter import *
    import tkinter as tk

def displayText():

    global entryWidget

    print(entryWidget.get())
    sys.exit()

def end():
    print('!!DO NOT RENAME!!')
    sys.exit()

root = Tk()

root.title("Rename Tab")
root["padx"] = 40
root["pady"] = 20

textFrame = Frame(root)

entryLabel = Label(textFrame)
entryLabel["text"] = "Rename file:"
entryLabel.pack(side=LEFT)

entryWidget = Entry(textFrame)
entryWidget["width"] = 50
entryWidget['text'] = sys.argv[1]
entryWidget.pack(side=LEFT)

textFrame.pack()

button = Button(root, text="Rename", command=displayText)
button.pack()


button2 = Button(root, text="Cancel", command=end)
button2.pack()

root.mainloop()
