import sys
import os
import requests
import time
import hashlib
import subprocess
import tkinter.messagebox as msgbox
from tkinter import Tk
from threading import Thread

# Конфигурация обновлений
update_server = "https://nskpc.ru/web/update/"
version = "1.0.0.0"  # Текущая версия


class Updater:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()

    def check_update(self):
        try:
            response = requests.get(f"{update_server}/version.txt", timeout=10)
            if response.status_code == 200:
                latest_version = response.text.strip()
                return latest_version > version
        except Exception as e:
            print(f"Ошибка проверки обновлений: {e}")
        return False

    def download_update(self):
        try:
            # Создаем папку для обновлений
            os.makedirs("update_temp", exist_ok=True)

            # Получение манифеста
            manifest = requests.get(f"{update_server}/manifest.json").json()

            # Скачивание файлов
            for file in manifest['files']:
                self._download_file(file['url'], file['sha256'])

            return True
        except Exception as e:
            print("Ошибка обновления", str(e))
            return False


    def _download_file(self, url, checksum):
        file_name = 'SupportNSKPC.exe'
        local_path = os.path.join("update_temp", file_name)

        # Скачивание
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Проверка хеша
        file_hash = hashlib.sha256(open(local_path, 'rb').read()).hexdigest().upper()
        if file_hash != checksum:
            os.remove(local_path)
            print(file_hash)
            raise Exception("Checksum mismatch")

    def apply_update(self):
        try:
            current_exe = os.path.basename(sys.argv[0])
            update_exe = os.path.join("update_temp", current_exe)

            # Проверяем, существует ли новый файл
            if not os.path.exists(update_exe):
                msgbox.showerror("Ошибка", f"Файл {update_exe} не найден!")
                return

            bat_script = f"""
            @echo off
            chcp 65001 > nul
    
            taskkill /IM "{current_exe}" /F > nul 2>&1
            timeout /t 2 /nobreak > nul
    
            xcopy /y "update_temp\\{current_exe}" "{os.getcwd()}" > nul
            if errorlevel 1 (
                pause
                exit /b 1
            )
    
            rmdir /s /q "update_temp"
    
            start "" "{current_exe}"
    
            del "%~f0"
            """

            with open("updater.bat", "w", encoding="utf-8") as f:
                f.write(bat_script.strip())

            # Запускаем bat-файл
            subprocess.Popen(["cmd", "/c", "start", "updater.bat"], shell=True)
            time.sleep(2)

            # Закрываем текущее приложение
            close_application()

        except Exception as e:
            msgbox.showerror("Ошибка", f"Не удалось применить обновление: {str(e)}")



def close_application():
    try:
        # Закрываем главное окно (если используется Tkinter)
        if 'tk' in sys.modules:
            import tkinter as tk
            root = tk.Tk()
            root.destroy()

        # Принудительное завершение процесса
        time.sleep(1)  # Даем время на закрытие
        os._exit(0)  # Немедленное завершение
    except Exception as e:
        print(f"Ошибка при закрытии: {e}")
        os._exit(1)


def start_update_check():

    def check():
        updater = Updater()
        if updater.check_update():
            if msgbox.askyesno("Обновление NSKPC", "Доступна новая версия! Установить сейчас?", icon='question'):
                if updater.download_update():
                    updater.apply_update()

    Thread(target=check, daemon=True).start()
