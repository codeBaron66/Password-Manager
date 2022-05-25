# add scroll
# seperate code into Files 
# package up app 

from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import *
from random import *
import string
from tkinter.constants import ACTIVE, HORIZONTAL
from typing import NewType
from typing_extensions import IntVar

# key = Fernet.generate_key()

# with open('mykey.key', 'wb') as mykey:
#     mykey.write(key)

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()

# print(key)

f = Fernet(key)



window = tk.Tk()
window.title("Password Generator")
window.geometry("450x300")
window.option_add("*Font", "Arial 18")
ps_length = tk.IntVar()
specChars = tk.IntVar()

def gen_pass():
    length = ps_length.get()
    special = specChars.get()
    characters = string.digits + string.ascii_letters + string.digits
    charPunc = string.ascii_letters + string.digits + string.punctuation + string.digits
    if special == 0:
        password = "".join(choice(characters) for x in range (length))
    else:
        password = "".join(choice(charPunc) for x in range (length))
    global newPass
    newPass = password
    label.config(text=newPass, width=32)
    copyBtn.config(state=NORMAL)
    saveBtn.config(state=NORMAL)

def save_pass():
    newWindow = Toplevel(window)
    newWindow.title("Save Password")
    newWindow.geometry("400x140")
    newWindow.option_add("*Font", "Arial 18")
    text = tk.Label(newWindow, padx=10, pady=10, text="Name:")
    text.grid(row=1, column=0)
    entry = Entry(newWindow, width= 20)
    entry.focus_set()
    entry.grid(row=1, column=1)
    global kill
    def kill():
        log = entry.get()
        passs = (f"\n" + log + ": " + newPass)
        res = bytes(passs, "utf-8")
        textFile = open("passwords.csv", "ab")
        textFile.write(res)
        textFile.close()




        with open('passwords.csv', 'rb') as original_file:
            original = original_file.read()
        encrypted = f.encrypt(original)

        with open ('enc_passwords.csv', 'ab') as encrypted_file:
            encrypted_file.write(res)
        
        # with open ('enc_passwords.csv', 'ab') as encrypted_file:
        #     encrypted_file.write(encrypted)



        newWindow.destroy()
    okBtn = tk.Button(newWindow, text="Save", padx=30, pady=10, command=kill)
    okBtn.grid(row=2, columnspan=3, pady=20)

def copy():
    window.clipboard_clear()
    window.clipboard_append(newPass)
    window.update()

def savedPass():
    newWindow = Toplevel(window)
    newWindow.title("Saved Passwords")
    newWindow.option_add("*Font", "Arial 18")
    newWindow.geometry("700x400")
    text = tk.Text(newWindow, height=10, padx=30, pady=30)
    textFile = open("saved.txt", 'r')
    content = textFile.read()
    text.insert("1.0", content)
    textFile.close()
    text.configure(state=DISABLED)
    scrollbar = tk.Scrollbar(newWindow, orient='vertical', command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    text.pack(side='left', fill='both', expand=True)
    def kill():
        newWindow.destroy()
    closeBtn = tk.Button(newWindow, text="Close", padx=30, pady=10, command=kill)
    closeBtn.pack()

m = Menu(window, tearoff = 0)
m.add_command(label ="Copy", command=copy)
def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

label = tk.Label(window, bg="white", width=32, text="")
label.bind("<Button-3>", do_popup)
label.grid(row=1, columnspan=3, pady=18, padx=15, ipady=5)

chkBtn4 = tk.Checkbutton(window, text="@!£&#(-+}]...", variable=specChars, onvalue=1, offvalue=0)
chkBtn4.grid(row=2, column=2)

slider = tk.Scale(window, from_=5, to=25, orient=HORIZONTAL, variable=ps_length)
slider.grid(row=2, column=0, columnspan=2)

genBtn = tk.Button(window, text="Generate", command=gen_pass)
genBtn.grid(row=3, columnspan=3, pady=30, sticky="ew", padx=10, ipady=5)

copyBtn = tk.Button(window, text="Copy ", state=DISABLED, command=copy)
copyBtn.grid(row=4, column=0, sticky='ew')

saveBtn = tk.Button(window, text="Save ", state=DISABLED, command=save_pass)
saveBtn.grid(row=4, column=1, sticky='ew')

savedBtn = tk.Button(window, text="Saved", command=savedPass)
savedBtn.grid(row=4, column=2, sticky='ew')

window.mainloop()