import subprocess
from tkinter import *
from tkinter import messagebox, simpledialog, ttk

import psutil

import modules.app_state as app
import modules.menu as menu


def tasks():
    app.canvas.delete('all')
    loc = app.Localization[app.current_lang]

    btn_back = Button(app.root, text=loc["btn_back"], command=menu.main_menu, font=("Arial", 11), width=10)
    app.canvas.create_window(50, 20, window=btn_back)

    notebook = ttk.Notebook(app.root, width=900, height=500)
    app.canvas.create_window(500, 310, window=notebook)

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
        name_lower = name.lower()
        exe_lower = (exe_path or "").lower()
        user_lower = (user or "").lower()

        if "temp" in exe_lower or "appdata" in exe_lower:
            return True

        if name_lower in critical_processes and exe_path:
            if "system32" not in exe_lower and "syswow64" not in exe_lower:
                return True

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

                if pid in app.overridden_criticality:
                    crit_status = loc["crit_removed"] if not app.overridden_criticality[pid] else loc["crit_yes"]
                else:
                    is_critical = (
                        name.lower() in critical_processes or
                        "system" in user.lower()
                    )
                    crit_status = loc["crit_yes"] if is_critical else loc["crit_no"]

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
        cmd = simpledialog.askstring(loc["run_title"], loc["run_prompt"], parent=app.root)
        if cmd:
            try:
                subprocess.Popen(cmd, shell=True)
                app.root.after(1000, lambda: load_processes(search_entry.get()))
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
            app.overridden_criticality[pid] = True
        else:
            app.overridden_criticality[pid] = False

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