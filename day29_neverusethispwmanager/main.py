"""
May revisit to mess with encryption and improving overall functionality
as a learning exercise. Here's a good implementation I saw in the comments 
for day 29: https://github.com/tom111989/password-manager/blob/171e4f14d67338db11569c114077880feaa74dfb/main.py
"""
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import pandas
import random
import string
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

EXCLUDED_CHARACTERS = {"0", "o", "O", "l", "1", "I", "\"", "'"}
PASSWORD_CHARACTERS = list(
    set(string.ascii_letters).union(
        set(string.digits), 
        set(string.punctuation).difference(EXCLUDED_CHARACTERS)
    )
)

fernet_key = ""

def get_fernet_key():
    global fernet_key
    new_pw = False

    try:
        with open("./.salt", "rb") as f_salt:
            salt = f_salt.read()
        with open("./.pw_check","r") as f_check:
            check = f_check.read()
    except FileNotFoundError:
        while not new_pw:
            new_pw_1 = simpledialog.askstring(title="Password Input",
                                              prompt="No password configured.\n"
                                              + "Please input your password.",
                                              show="*")
            new_pw_2 = simpledialog.askstring(title="Password Input",
                                              prompt="Repeat for confirmation.",
                                              show="*")
            if new_pw_1 != new_pw_2:
                messagebox.showerror("Error", "Password mismatch.")
            else:
                messagebox.showinfo("Success!", "Master Password Set.")
                new_pw = True

        with open("./.salt", "wb") as f_salt:
            salt = os.urandom(16)
            f_salt.write(salt)
        with open("./.pw_check", "wb") as f_check:
            check = b"decoded"
            f_check.write(check)

        pw_correct = False
        while not pw_correct:
            if new_pw:
                user_pw = new_pw_1
            else:
                user_pw = simpledialog.askstring(
                    title="Password Input",
                    prompt="Please input your password.",
                    show="*")

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=390000)
            key = base64.urlsafe_b64encode(kdf.derive(user_pw.encode()))
            fernet_key = Fernet(key)
            pw_correct = fernet_key.decrypt(check) == b"decode" or new_pw
        with open("./.pw_check", "wb") as f_check:
            f_check.write(fernet_key.encrypt(b"decode"))


def encrypt_file():
    with open("./pw.db", "rb") as file:
        decrypted_data = file.read()

    encrypted_data = fernet_key.encrypt(decrypted_data)

    with open("./pw.db", "wb") as file:
        file.write(encrypted_data)


def decrypt_file():
    with open("./pw.db", "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet_key.decrypt(encrypted_data)

    with open("./pw.db", "wb") as file:
        file.write(decrypted_data)

def generate_pw():
    random_pw = "".join(random.choices(PASSWORD_CHARACTERS, k=16))
    entry_pw.insert(0, random_pw)


def save_pw():
    #if fernet_key == "":
    #    get_fernet_key()

    if (len(entry_website.get()) == 0 or
        len(entry_un.get()) == 0 or
        len(entry_pw.get()) == 0):
        messagebox.showerror("Error", "Missing required information")
    else:
        #decrypt_file()
        new_pw = {"website": entry_website.get(),
                  "username": entry_un.get(),
                  "password": entry_pw.get()}
        pw_df = pandas.DataFrame(new_pw, index=[0])
        pw_df.to_csv("./pw.db", mode="a", index=False, header=False)
        #encrypt_file() 

        entry_website.delete(0, END)
        entry_un.delete(0, END)
        entry_pw.delete(0, END)

def show_pw():
    pass

window = Tk()
window.title("Don't Use This Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website: ")
label_website.grid(column=0, row=1, sticky=E)

entry_website = Entry(width=47)
entry_website.grid(column=1, row=1, columnspan=2)
entry_website.focus()

label_un = Label(text="Email/Username: ")
label_un.grid(column=0, row=2, sticky=E)

entry_un = Entry(width=47)
entry_un.grid(column=1, row=2, columnspan=2)

label_pw = Label(text="Password: ")
label_pw.grid(column=0, row=3, sticky=E)

entry_pw = Entry(width=28, show="*")
entry_pw.grid(column=1, row=3)

button_generate = Button(text="Generate Password", width=15, command=generate_pw)
button_generate.grid(column=2, row=3)

button_save = Button(text="Save", width=44, command=save_pw)
button_save.grid(column=1, row=4, columnspan=2)

button_show_pass = Button(text="Show Passwords", width=44, command=show_pw)
button_show_pass.grid(column=1, row=5, columnspan=2)

window.mainloop()
