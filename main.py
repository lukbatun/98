import pathlib
from tkinter import *
from tkinter import ttk
import os
from datetime import datetime
import psutil

root = Tk()
root.title("98 utility")
root.geometry("400x300")
root.resizable(False, False)
root.iconbitmap("ico.ico")

canvas = Canvas(root, width=400, height=300, bg="lightgray")
canvas.pack()

selected_disk = None
current_lang = "en"
current_path = ""
canvas_main = None

Languages = ["English", "Russian", "Nedorusskiy"]
Languages_dict = {
    "English": "en",
    "Russian": "ru",
    "Nedorusskiy": "nedo"
}

Localization = {
    "en": {
        "select_disk": "Select a disk:",
        "created_by": "created by lukbatun.",
        "btn_select": "Select Disk",
        "btn_exit": "Exit",
        "btn_explorer": "Explorer",
        "btn_utility": "Utilities",
        "btn_recovery": "Recovery",
        "btn_scanning": "Scan",
        "btn_tasklist": "Tasks",
        "quick_access": "Important Places",
        "col_name": "Name",
        "col_size": "Size",
        "col_type": "Type",
        "col_date": "Modified",
        "btn_up": "Up",
        "folder": "Folder",
        "file": "File",
        "loc_desktop": "Desktop",
        "loc_docs": "Documents",
        "loc_down": "Downloads",
        "loc_music": "Music",
        "loc_pics": "Pictures",
        "loc_videos": "Videos",
        "loc_root": "Root",
        "loc_windows": "Windows"
    },
    "ru": {
        "select_disk": "Выберите диск:",
        "created_by": "создано lukbatun.",
        "btn_select": "Выбрать диск",
        "btn_exit": "Выход",
        "btn_explorer": "Проводник",
        "btn_utility": "Утилиты",
        "btn_recovery": "Восстановление",
        "btn_scanning": "Сканирование",
        "btn_tasklist": "Задачи",
        "quick_access": "Важные места",
        "col_name": "Имя",
        "col_size": "Размер",
        "col_type": "Тип",
        "col_date": "Дата изменения",
        "btn_up": "Наверх",
        "folder": "Папка",
        "file": "Файл",
        "loc_desktop": "Рабочий стол",
        "loc_docs": "Документы",
        "loc_down": "Загрузки",
        "loc_music": "Музыка",
        "loc_pics": "Изображения",
        "loc_videos": "Видео",
        "loc_root": "Корень диска",
        "loc_windows": "Windows"
    },
    "nedo": {
        "select_disk": "Vibirite disk:",
        "created_by": "sozdano lukbatun.",
        "btn_select": "Vibrat disk",
        "btn_exit": "Vihod",
        "btn_explorer": "Prowodnik",
        "btn_utility": "Utiliti",
        "btn_recovery": "Vosstanovlenie",
        "btn_scanning": "Skanirovanie",
        "btn_tasklist": "Zadachi",
        "quick_access": "Vazhnie mesta",
        "col_name": "Imya",
        "col_size": "Razmer",
        "col_type": "Tip",
        "col_date": "Data izmeneniya",
        "btn_up": "Naverh",
        "folder": "Papka",
        "file": "Fail",
        "loc_desktop": "Rabochiy stol",
        "loc_docs": "Dokumenti",
        "loc_down": "Zagruzki",
        "loc_music": "Muzika",
        "loc_pics": "Kartinki",
        "loc_videos": "Kino",
        "loc_root": "Koren",
        "loc_windows": "Vindovs"
    }
}

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def change_language(event):
    global current_lang
    selected = combobox.get()
    current_lang = Languages_dict.get(selected, "en")
    disk_selection()

def disk_selection():
    global combobox
    canvas.delete('all')
    root.geometry("400x300")
    canvas.config(width=400, height=300)

    try:
        drives = os.listdrives()
    except AttributeError:
        import string
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    count = len(drives)
    
    canvas.create_text(200, 40, text=Localization[current_lang]["select_disk"], font=("Arial", 16))
    canvas.create_text(200, 260, text=Localization[current_lang]["created_by"], font=("Arial", 16))
    
    combobox = ttk.Combobox(root, values=Languages, font=("Arial", 11), width=10, state="readonly")
    for lang_name, lang_code in Languages_dict.items():
        if lang_code == current_lang:
            combobox.set(lang_name)
            break
            
    combobox.bind("<<ComboboxSelected>>", change_language)
    canvas.create_window(55, 15, window=combobox)
    
    for i in range(count):
        btn = Button(root, text=drives[i], command=lambda d=drives[i]: select_disk(d), font=("Arial", 11), width=12)
        canvas.create_window(200, 90 + 45 * i, window=btn)

def select_disk(disk):
    global selected_disk, current_path
    selected_disk = disk
    current_path = disk
    main_menu()

def main_menu():
    global canvas_main
    canvas.delete('all')
    root.geometry("1000x600")
    canvas.config(width=1000, height=600)
    
    btn1 = Button(root, text=Localization[current_lang]["btn_select"], command=disk_selection, font=("Arial", 11), width=12)
    canvas.create_window(70, 30, window=btn1)
    
    btn2 = Button(root, text=Localization[current_lang]["btn_exit"], command=root.quit, font=("Arial", 11), width=12)
    canvas.create_window(200, 30, window=btn2)

    btn4 = Button(root, text=Localization[current_lang]["btn_utility"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    canvas.create_window(120, 170, window=btn4)

    btn5 = Button(root, text=Localization[current_lang]["btn_explorer"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    canvas.create_window(120, 240, window=btn5)

    btn6 = Button(root, text=Localization[current_lang]["btn_recovery"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    canvas.create_window(120, 310, window=btn6)

    btn7 = Button(root, text=Localization[current_lang]["btn_scanning"], command=utils, font=("Arial", 14, "bold"), width=15, height=2)
    canvas.create_window(120, 380, window=btn7) 

    btn8 = Button(root, text=Localization[current_lang]["btn_tasklist"], command=tasks, font=("Arial", 14, "bold"), width=15, height=2)
    canvas.create_window(120, 450, window=btn8)
    
    canvas.create_text(550, 30, text="98 utility", font=("Arial", 24))
    
    canvas_main = Canvas(root, width=700, height=500, bg="white")
    canvas.create_window(280, 70, window=canvas_main, anchor="nw")

def utils():
    print("utils")

def tasks():
    print("taskmgr")
    canvas.delete("all")
    for proc in psutil.process_iter(['pid', 'name', 'username',]):
        try:
            # Получаем информацию о процессе в виде словаря
            pinfo = proc.info
            print(pinfo)
            pids = []
            pnames = []
            user = []

            print(f"PID: {pinfo['pid']}, Имя: {pinfo['name']}, Пользователь: {pinfo['username']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    import subprocess

    result = subprocess.run(['tasklist'], capture_output=True, text=True, encoding='cp866')
    print(result.stdout)



disk_selection()
root.mainloop()