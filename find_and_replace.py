try:
    from Tkinter import *
    import Tkinter as tk
except:
    from tkinter import *
    import tkinter as tk

def find():

    global entryWidget

    print('!!FIND_ONLY!! !!FIND!!' + entryWidget.get())
    #sys.exit()

def replace():

    global entryWidget
    global entryWidget2

    print('!!FIND!!' + entryWidget.get() + '!!REPLACE!!' + entryWidget2.get())
    #sys.exit()

def end():
    print('!!END!!')
    sys.exit()

root = Tk()

root.title("Find and Replace")
root["padx"] = 40
root["pady"] = 20

textFrame = Frame(root)

entryLabel = Label(textFrame)
entryLabel["text"] = "Find:"
entryLabel.pack()

entryWidget = Entry(textFrame)
entryWidget["width"] = 50
entryWidget.pack()

entryLabel2 = Label(textFrame)
entryLabel2["text"] = "Replace:"
entryLabel2.pack()

entryWidget2 = Entry(textFrame)
entryWidget2["width"] = 50
entryWidget2.pack()

textFrame.pack()

button = Button(root, text="Find Next", command=find)
button.pack()

button2 = Button(root, text="Replace", command=replace)
button2.pack()

button3 = Button(root, text="Done", command=end)
button3.pack()

root.mainloop()
