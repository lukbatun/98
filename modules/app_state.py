import ctypes
import json
import os
import shutil
from tkinter import messagebox

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(APP_DIR, "local.ttf")

root = None
canvas = None
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


def register_windows_font(font_path):
    try:
        if not os.path.exists(font_path):
            return False

        fonts_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        os.makedirs(fonts_dir, exist_ok=True)

        dest_path = os.path.join(fonts_dir, os.path.basename(font_path))
        if not os.path.exists(dest_path):
            shutil.copy2(font_path, dest_path)

        if ctypes.windll.gdi32.AddFontResourceW(dest_path):
            return True
    except Exception:
        pass
    return False


def ensure_project_font(font_path=FONT_PATH):
    try:
        import tkinter.font as tkfont
        available = {name.lower() for name in tkfont.families()}
    except Exception:
        available = set()

    family_candidates = [
        "local",
        os.path.splitext(os.path.basename(font_path))[0].lower() if font_path else "",
        "tahoma",
        "segoe ui",
        "arial"
    ]

    for candidate in family_candidates:
        if candidate and candidate.lower() in available:
            return candidate

    if not os.path.exists(font_path):
        return None

    if messagebox.askyesno(
        "Проблема со шрифтом",
        "Системный шрифт работает некорректно.\n"
        "Установить встроенный шрифт из проекта в Windows и использовать его сразу?"
    ):
        if register_windows_font(font_path):
            try:
                import tkinter.font as tkfont
                available = {name.lower() for name in tkfont.families()}
                for candidate in family_candidates:
                    if candidate and candidate.lower() in available:
                        messagebox.showinfo("Шрифт установлен", "Встроенный шрифт успешно установлен и активирован.")
                        return candidate
            except Exception:
                pass

        messagebox.showerror(
            "Шрифт не установлен",
            "Автоматическая установка не удалась.\n"
            "Проверьте файл local.ttf в папке проекта."
        )

    return None


def load_localization():
    localization_path = os.path.join(APP_DIR, "Localization.json")
    try:
        with open(localization_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, dict) and data:
            return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass

    with open(localization_path, "w", encoding="utf-8") as file:
        json.dump(DEFAULT_LOCALIZATION, file, ensure_ascii=False, indent=2)
    return DEFAULT_LOCALIZATION


Localization = load_localization()


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"