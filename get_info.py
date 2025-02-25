import os
import subprocess
import socket
import json
import http.client


def get_anydesk_id():
    try:
        config_path = os.path.expanduser("C://ProgramData//AnyDesk//system.conf")
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                for line in file:
                    if line.startswith("ad.anynet.id="):
                        return line.split("=")[1].strip()
        return "Not Found"
    except Exception:
        return "Not Found"


def get_rustdesk_id():
    try:
        output = subprocess.run([r"C://Program Files//RustDesk//rustdesk.exe", "--get-id"],
                                capture_output=True, text=True)
        return output.stdout.strip()
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
