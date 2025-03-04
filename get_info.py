import os
import subprocess
import socket
import json
import http.client
import platform
import psutil
from time import sleep


def get_anydesk_id():
    try:
        anydesk_portable_path = "C://NSKPC//Удаленная помощь//AnyDesk.exe"
        config_path = "C://ProgramData//AnyDesk//system.conf"
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                for line in file:
                    if line.startswith("ad.anynet.id="):
                        return line.split("=")[1].strip()

        if not os.path.exists(config_path):
            anydesk_status = False
            for proc in psutil.process_iter():
                name = proc.name()
                if name == "AnyDesk.exe":
                    anydesk_status = True
            if not anydesk_status:
                subprocess.Popen(anydesk_portable_path)
                sleep(6)


            output = subprocess.run([anydesk_portable_path, "--get-id"],
                                    capture_output=True, text=True)
            return output.stdout.strip()
        return "Not Found"
    except Exception:
        return "Not Found"


def get_rustdesk_id():
    try:
        rustdesk_path = r"C:\Program Files\RustDesk\rustdesk.exe"
        rustdesk_portable_path = r"C:\NSKPC\Удаленная помощь\rustdesk-1.2.7-x86_64.exe"
        if os.path.exists(rustdesk_path):
            path = rustdesk_path
        else:
            path = rustdesk_portable_path
        output = subprocess.run([path, "--get-id"],
                                capture_output=True, text=True)
        rust_desk_id = output.stdout.strip().split("\n")[-1]
        return rust_desk_id
    except Exception:
        return "Not Found"


def get_global_ip():
    try:
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        global_ip = str(conn.getresponse().read())
        global_ip = global_ip[2:-1]
        return global_ip
    except Exception:
        return "Not Found"


def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception:
        return "Not Found"


def get_host_name():
    try:
        return socket.gethostname()
    except Exception:
        return "Not Found"


def get_computer_info():
    try:
        computer_info_path = os.path.expanduser("C://NSKPC//computer_info.json")
        if os.path.exists(computer_info_path):
            with open(computer_info_path, "r", encoding="UTF8") as file:
                data = json.load(file)
                company_name = data["company_name"]
                full_company_name = data["full_company_name"]
                computer_name = data["computer_name"]
            return computer_name, company_name, full_company_name
        return "Not Found", "Not Found", "Not Found"
    except:
        return "Not Found", "Not Found", "Not Found"


def get_os_info():
    try:
        os_full = platform.platform()
        os_bit = "64-bit" if "PROGRAMFILES(X86)" in os.environ else "32-bit"
        os_info = f'{os_full} {os_bit}'
        return os_info
    except:
        return "Not Found"
