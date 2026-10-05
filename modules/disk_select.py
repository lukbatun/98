import os
import string
from tkinter import *
from tkinter import ttk

import modules.app_state as app
import modules.menu as menu

combobox = None


def change_language(event):
    app.current_lang = app.Languages_dict.get(combobox.get(), "en")
    disk_selection()


def disk_selection():
    global combobox
    app.canvas.delete('all')
    app.root.geometry("400x300")
    app.canvas.config(width=400, height=300)

    try:
        drives = os.listdrives()
    except AttributeError:
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    count = len(drives)

    app.canvas.create_text(200, 40, text=app.Localization[app.current_lang]["select_disk"], font=("Arial", 16))
    app.canvas.create_text(200, 260, text=app.Localization[app.current_lang]["created_by"], font=("Arial", 16))

    combobox = ttk.Combobox(app.root, values=app.Languages, font=("Arial", 11), width=10, state="readonly")
    for lang_name, lang_code in app.Languages_dict.items():
        if lang_code == app.current_lang:
            combobox.set(lang_name)
            break

    combobox.bind("<<ComboboxSelected>>", change_language)
    app.canvas.create_window(55, 15, window=combobox)

    for i in range(count):
        btn = Button(app.root, text=drives[i], command=lambda d=drives[i]: select_disk(d), font=("Arial", 11), width=12)
        app.canvas.create_window(200, 90 + 45 * i, window=btn)


def select_disk(disk):
    app.selected_disk = disk
    app.current_path = disk
    menu.main_menu()