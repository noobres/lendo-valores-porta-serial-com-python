from tkinter import *

ROOT = Tk()

def ask_for_userinput():
    user_input = raw_input("Give me your command! Just type \"exit\" to close: ")
    if user_input == "exit":
        ROOT.quit()
    else:
        label = Label(ROOT, text=user_input)
        label.pack()
        ROOT.after(0, ask_for_userinput)

LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
ROOT.after(0, ask_for_userinput)
ROOT.mainloop()