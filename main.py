import os
from tkinter import *

import modules.app_state as app

app.root = Tk()
app.root.title("98 utility")
app.root.geometry("400x300")
app.root.resizable(False, False)
icon_path = os.path.join(app.APP_DIR, "ico.ico")
if os.path.exists(icon_path):
    try:
        app.root.iconbitmap(icon_path)
    except Exception:
        pass

custom_font_name = app.ensure_project_font()
if custom_font_name:
    app.root.option_add("*Font", f"{custom_font_name} 10")

app.canvas = Canvas(app.root, width=400, height=300, bg="lightgray")
app.canvas.pack()

import modules.disk_select as disk_select

disk_select.disk_selection()
app.root.mainloop()