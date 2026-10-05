from tkinter import *

import modules.app_state as app
import modules.disk_select as disk_select
import modules.tasks as tasks


def main_menu():
    app.canvas.delete('all')
    app.root.geometry("1000x600")
    app.canvas.config(width=1000, height=600)

    btn1 = Button(app.root, text=app.Localization[app.current_lang]["btn_select"], command=disk_select.disk_selection, font=("Arial", 11), width=12)
    app.canvas.create_window(70, 30, window=btn1)

    btn2 = Button(app.root, text=app.Localization[app.current_lang]["btn_exit"], command=app.root.quit, font=("Arial", 11), width=12)
    app.canvas.create_window(200, 30, window=btn2)

    btn4 = Button(app.root, text=app.Localization[app.current_lang]["btn_utility"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    app.canvas.create_window(120, 170, window=btn4)

    btn5 = Button(app.root, text=app.Localization[app.current_lang]["btn_explorer"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    app.canvas.create_window(120, 240, window=btn5)

    btn6 = Button(app.root, text=app.Localization[app.current_lang]["btn_recovery"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    app.canvas.create_window(120, 310, window=btn6)

    btn7 = Button(app.root, text=app.Localization[app.current_lang]["btn_scanning"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    app.canvas.create_window(120, 380, window=btn7)

    btn8 = Button(app.root, text=app.Localization[app.current_lang]["btn_tasklist"], command=tasks.tasks, font=("Arial", 14, "bold"), width=15, height=2)
    app.canvas.create_window(120, 450, window=btn8)

    app.canvas.create_text(550, 30, text="98 utility", font=("Arial", 24))

    app.canvas_main = Canvas(app.root, width=700, height=500, bg="white")
    app.canvas.create_window(280, 70, window=app.canvas_main, anchor="nw")


def utils():
    print("utils")