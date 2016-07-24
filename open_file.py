from Tkinter import *
import Tkinter as tk

def displayText():

    global entryWidget
     
    print(entryWidget.get())
    sys.exit()

def end():
    print('!!DO NOT OPEN!!')
    sys.exit()

root = Tk()

root.title("Open File")
root["padx"] = 40
root["pady"] = 20   

textFrame = Frame(root)

entryLabel = Label(textFrame)
entryLabel["text"] = "File to open:"
entryLabel.pack(side=LEFT)

entryWidget = Entry(textFrame)
entryWidget["width"] = 50
entryWidget.pack(side=LEFT)

textFrame.pack()

button = Button(root, text="Open", command=displayText)
button.pack()

button2 = Button(root, text="Cancel", command=end)
button2.pack()


root.mainloop()












