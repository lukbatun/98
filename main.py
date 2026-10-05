import pathlib
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import os
from datetime import datetime
import psutil
import subprocess

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

overridden_criticality = {}

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
        "loc_windows": "Windows",
        "tab_processes": " Processes ",
        "tab_services": " Services ",
        "lbl_search_proc": "Search process: ",
        "lbl_search_serv": "Search service: ",
        "btn_kill": "Kill Process",
        "btn_run": "Run Task",
        "btn_toggle_crit": "Toggle Critical",
        "col_proc_name": "Process",
        "col_pid": "PID",
        "col_user": "User",
        "col_critical": "Critical",
        "col_serv_name": "Service Name",
        "col_serv_display": "Display Name",
        "col_serv_status": "Status",
        "crit_yes": "Yes",
        "crit_no": "No",
        "crit_removed": "Removed",
        "btn_back": "< Back",
        "run_title": "Run New Task",
        "run_prompt": "Enter program name or path:",
        "run_error": "Failed to start process:"
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
        "loc_windows": "Windows",
        "tab_processes": " Процессы ",
        "tab_services": " Службы ",
        "lbl_search_proc": "Поиск процесса: ",
        "lbl_search_serv": "Поиск службы: ",
        "btn_kill": "Завершить процесс",
        "btn_run": "Запустить процесс",
        "btn_toggle_crit": "Снять критичность",
        "col_proc_name": "Процесс",
        "col_pid": "PID",
        "col_user": "Пользователь",
        "col_critical": "Критичен",
        "col_serv_name": "Имя службы",
        "col_serv_display": "Отображаемое имя",
        "col_serv_status": "Статус",
        "crit_yes": "Да",
        "crit_no": "Нет",
        "crit_removed": "Снято",
        "btn_back": "< Назад",
        "run_title": "Запуск задачи",
        "run_prompt": "Введите имя программы или путь к файлу:",
        "run_error": "Не удалось запустить процесс:"
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
        "loc_windows": "Vindovs",
        "tab_processes": " Protsessi ",
        "tab_services": " Sluzhbi ",
        "lbl_search_proc": "Poisk protsessa: ",
        "lbl_search_serv": "Poisk sluzhbi: ",
        "btn_kill": "Zavershit",
        "btn_run": "Zapustit protsess",
        "btn_toggle_crit": "Snyat kritichnost",
        "col_proc_name": "Protsess",
        "col_pid": "PID",
        "col_user": "Polzovatel",
        "col_critical": "Kritichen",
        "col_serv_name": "Imya sluzhbi",
        "col_serv_display": "Imya",
        "col_serv_status": "Status",
        "crit_yes": "Da",
        "crit_no": "Net",
        "crit_removed": "Snyato",
        "btn_back": "< Nazad",
        "run_title": "Zapusk zadachi",
        "run_prompt": "Vvedite imya programmi ili put:",
        "run_error": "Ne udalos zapustit protsess:"
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
    canvas.delete('all')
    loc = Localization[current_lang]
    
    btn_back = Button(root, text=loc["btn_back"], command=main_menu, font=("Arial", 11), width=10)
    canvas.create_window(50, 20, window=btn_back)

    notebook = ttk.Notebook(root, width=900, height=500)
    canvas.create_window(500, 310, window=notebook)

    tab_tasks = Frame(notebook)
    tab_services = Frame(notebook)

    notebook.add(tab_tasks, text=loc["tab_processes"])
    notebook.add(tab_services, text=loc["tab_services"])

    top_frame = Frame(tab_tasks)
    top_frame.pack(fill=X, padx=5, pady=5)

    Label(top_frame, text=loc["lbl_search_proc"], font=("Arial", 10)).pack(side=LEFT)
    search_entry = Entry(top_frame, font=("Arial", 10), width=20)
    search_entry.pack(side=LEFT, padx=5)

    tree_frame = Frame(tab_tasks)
    tree_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    columns = ("name", "pid", "user", "critical")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    
    # Подсветка подозрительных процессов красным цветом
    tree.tag_configure("suspicious", background="#ff9999", foreground="black")
    
    tree.heading("name", text=loc["col_proc_name"], command=lambda: sort_column(tree, "name", False))
    tree.heading("pid", text=loc["col_pid"], command=lambda: sort_column(tree, "pid", False))
    tree.heading("user", text=loc["col_user"], command=lambda: sort_column(tree, "user", False))
    tree.heading("critical", text=loc["col_critical"], command=lambda: sort_column(tree, "critical", False))
    
    tree.column("name", width=230, minwidth=100)
    tree.column("pid", width=70, minwidth=50, anchor="center")
    tree.column("user", width=180, minwidth=100)
    tree.column("critical", width=100, minwidth=60, anchor="center")

    scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    critical_processes = [
        "system", "system idle process", "smss.exe", "csrss.exe", 
        "wininit.exe", "services.exe", "lsass.exe", "svchost.exe"
    ]

    def is_suspicious(name, exe_path, user):
        """Функция проверки процесса на подозрительность"""
        name_lower = name.lower()
        exe_lower = (exe_path or "").lower()
        user_lower = (user or "").lower()

        # 1. Запуск из временных папок (Temp / AppData)
        if "temp" in exe_lower or "appdata" in exe_lower:
            return True

        # 2. Подделка системных процессов (запущены не из System32/SysWOW64)
        if name_lower in critical_processes and exe_path:
            if "system32" not in exe_lower and "syswow64" not in exe_lower:
                return True

        # 3. Системные процессы, запущенные от обычного пользователя
        if name_lower in ["lsass.exe", "csrss.exe", "smss.exe", "services.exe", "wininit.exe"]:
            if "system" not in user_lower and "local service" not in user_lower and "network service" not in user_lower:
                return True

        return False

    def load_processes(filter_text=""):
        for item in tree.get_children():
            tree.delete(item)

        filter_text = filter_text.lower()

        for proc in psutil.process_iter(['pid', 'name', 'username', 'exe']):
            try:
                pinfo = proc.info
                pid = pinfo['pid']
                name = pinfo['name'] or "Unknown"
                user = pinfo['username'] or "Unknown"
                exe_path = pinfo['exe'] or ""
                
                if pid in overridden_criticality:
                    crit_status = loc["crit_removed"] if not overridden_criticality[pid] else loc["crit_yes"]
                else:
                    is_critical = (
                        name.lower() in critical_processes or 
                        "system" in user.lower()
                    )
                    crit_status = loc["crit_yes"] if is_critical else loc["crit_no"]
                
                # Применяем тег подсветки, если процесс подозрителен
                tags = ()
                if is_suspicious(name, exe_path, user):
                    tags = ("suspicious",)

                if (filter_text in name.lower() or 
                    filter_text in str(pid) or 
                    filter_text in user.lower()):
                    tree.insert("", END, values=(name, pid, user, crit_status), tags=tags)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def kill_selected_process():
        selected_item = tree.selection()
        if not selected_item:
            return
        
        item_values = tree.item(selected_item[0], "values")
        pid = int(item_values[1])

        try:
            p = psutil.Process(pid)
            p.kill()
            load_processes(search_entry.get())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def run_new_process():
        cmd = simpledialog.askstring(loc["run_title"], loc["run_prompt"], parent=root)
        if cmd:
            try:
                subprocess.Popen(cmd, shell=True)
                root.after(1000, lambda: load_processes(search_entry.get()))
            except Exception as e:
                messagebox.showerror(loc["run_title"], f"{loc['run_error']}\n{e}")

    def toggle_criticality():
        selected_item = tree.selection()
        if not selected_item:
            return
        
        item_values = tree.item(selected_item[0], "values")
        pid = int(item_values[1])

        current_status = item_values[3]
        if current_status == loc["crit_removed"]:
            overridden_criticality[pid] = True
        else:
            overridden_criticality[pid] = False

        load_processes(search_entry.get())

    btn_kill = Button(top_frame, text=loc["btn_kill"], command=kill_selected_process, bg="#ffdddd", font=("Arial", 9, "bold"))
    btn_kill.pack(side=RIGHT, padx=3)

    btn_run = Button(top_frame, text=loc["btn_run"], command=run_new_process, bg="#ddffdd", font=("Arial", 9))
    btn_run.pack(side=RIGHT, padx=3)

    btn_crit = Button(top_frame, text=loc["btn_toggle_crit"], command=toggle_criticality, bg="#fff3cd", font=("Arial", 9))
    btn_crit.pack(side=RIGHT, padx=3)

    search_entry.bind("<KeyRelease>", lambda event: load_processes(search_entry.get()))

    serv_top_frame = Frame(tab_services)
    serv_top_frame.pack(fill=X, padx=5, pady=5)

    Label(serv_top_frame, text=loc["lbl_search_serv"], font=("Arial", 10)).pack(side=LEFT)
    serv_search_entry = Entry(serv_top_frame, font=("Arial", 10), width=30)
    serv_search_entry.pack(side=LEFT, padx=5)

    serv_tree_frame = Frame(tab_services)
    serv_tree_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    serv_columns = ("name", "display_name", "status")
    serv_tree = ttk.Treeview(serv_tree_frame, columns=serv_columns, show="headings")

    serv_tree.heading("name", text=loc["col_serv_name"], command=lambda: sort_column(serv_tree, "name", False))
    serv_tree.heading("display_name", text=loc["col_serv_display"], command=lambda: sort_column(serv_tree, "display_name", False))
    serv_tree.heading("status", text=loc["col_serv_status"], command=lambda: sort_column(serv_tree, "status", False))

    serv_tree.column("name", width=200, minwidth=100)
    serv_tree.column("display_name", width=350, minwidth=150)
    serv_tree.column("status", width=120, minwidth=80, anchor="center")

    serv_scrollbar = Scrollbar(serv_tree_frame, orient=VERTICAL, command=serv_tree.yview)
    serv_tree.configure(yscrollcommand=serv_scrollbar.set)

    serv_scrollbar.pack(side=RIGHT, fill=Y)
    serv_tree.pack(side=LEFT, fill=BOTH, expand=True)

    def load_services(filter_text=""):
        for item in serv_tree.get_children():
            serv_tree.delete(item)

        filter_text = filter_text.lower()

        try:
            for s in psutil.win_service_iter():
                try:
                    s_info = s.as_dict()
                    s_name = s_info.get('name', 'Unknown')
                    s_display = s_info.get('display_name', 'Unknown')
                    s_status = s_info.get('status', 'Unknown')

                    if (filter_text in s_name.lower() or 
                        filter_text in s_display.lower() or 
                        filter_text in s_status.lower()):
                        serv_tree.insert("", END, values=(s_name, s_display, s_status))
                except Exception:
                    pass
        except AttributeError:
            pass

    serv_search_entry.bind("<KeyRelease>", lambda event: load_services(serv_search_entry.get()))

    def sort_column(tree_obj, col, reverse):
        l = [(tree_obj.set(k, col), k) for k in tree_obj.get_children('')]
        if col == "pid":
            l.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        else:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree_obj.move(k, '', index)

        tree_obj.heading(col, command=lambda: sort_column(tree_obj, col, not reverse))

    load_processes()
    load_services()

disk_selection()
root.mainloop()