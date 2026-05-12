import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, filedialog
import subprocess
import os
import json
import paramiko
import time
import subprocess
import scp 

CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    root_temp = tk.Tk()
    root_temp.withdraw()
    pwd = simpledialog.askstring("Configure", "Enter the password")
    user = simpledialog.askstring("Configure", "Enter username")
    data = {
        "pwd": pwd,
        "user": user
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
    root_temp.destroy()
    
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)
pwd = config["pwd"]
user = config["user"]
def upup():
    root = tk.Tk()
    root.withdraw() 
    host = simpledialog.askstring("APK update", "Host IP adress:")
    if not host:
        messagebox.showerror("ERRER", "Input cannot be empty")
        return
    root.destroy()
    toor = tk.Tk()
    toor.title("APK Upgrade")
    toor.geometry("640x300")
    terminal = scrolledtext.ScrolledText(toor, width=75, height=20)
    terminal.pack(pady=10)
    global ssh
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=pwd)
    
    except Exception as e:
        messagebox.showerror("ERROR", str(e))
    
    command = f'echo "{pwd}" | sudo -S -p "" apk update'
    print ("command to be executed:" + command)
    
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()
        terminal.insert(tk.END, f"\n$ {command}\n")
        terminal.insert(tk.END, result)
        if error:
            terminal.insert(tk.END, error)
        terminal.see(tk.END)
        terminal.insert(tk.END, "Updated\n")
    except Exception as e:
        terminal.insert(tk.END, f"ERROR: {e}\n")
        print ("command to be executed:" + command)
    
    command = f'echo "{pwd}" | sudo -S -p "" apk upgrade'
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()
        terminal.insert(tk.END, f"\n$ {command}\n")
        terminal.insert(tk.END, result)
        if error:
            terminal.insert(tk.END, error)
        terminal.see(tk.END)
        terminal.insert(tk.END, "Upgraded\n")
    except Exception as e:
        terminal.insert(tk.END, f"ERROR: {e}\n")
    time.sleep(5)
    toor.destroy()

def console():
    root = tk.Tk()
    root.withdraw() 
    host = simpledialog.askstring("SSH console", "Host IP adress:")
    if not host:
        messagebox.showerror("ERRER", "Input cannot be empty")
        return
    root.destroy()
    ssh_command = f"ssh {user}@{host}"
    try:
        subprocess.Popen(
            f'start cmd /k "{ssh_command}"',
            shell=True
        )
    except Exception as e:
        messagebox.showerror("ERRER", str(e))
def exit():
    root.destroy()
def localinst():
    question = tk.Tk()
    question.withdraw()
    terminal = scrolledtext.ScrolledText(question, width=75, height=20)
    terminal.pack(pady=10)
    ipaddr = simpledialog.askstring("enter ip address", "Enter the IP of your pmOS device")
    question.destroy()
    apk = tk.Tk()
    file = filedialog.askopenfilename(title="Open .apk file")
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipaddr, username=user, password=pwd)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(file, f"/home/{user}/{file}")
    messagebox.showinfo("File uploaded", "Step 1 completed")
    command = f"echo {pwd} | sudo -S -p '' apk add /home/{user}/{file}"
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    error = stderr.read().decode()
    terminal.insert(tk.END, result)
    if error:
        terminal.insert(tk.END, error)
    terminal.see(tk.END)
    terminal.insert(tk.END, "Maybe installed?\n")
    messagebox.showinfo("Done", "Maybe installed, if you had the dependencies.")
    apk.destroy()
def apk():
    window = tk.Tk()
    window.title("APK utils")
    window.geometry("300x200")
    window.resizable(False, False)
    title = tk.Label(window, text="APK Utils", font=("Times New Roman", 10))
    title.pack(pady=5)
    upup_btn = tk.Button(window, text="Update&Upgrade", width=20, height=2, command=upup)
    upup_btn.pack(padx=10,pady=20)
    localinst_btn = tk.Button(window, text="Install .apk file locally", width=20, height=2, command=localinst)
    localinst_btn.pack(padx=10,pady=20)
    window.mainloop()
root = tk.Tk()
root.title("pmOS manager")
root.geometry("600x400")
root.resizable(False, False)

title = tk.Label(root, text=f"Welcome {user}", font=("Arial", 18))
title.pack(pady=10)

console_btn = tk.Button(root, text="Console", width=20, height=2, command=console)
console_btn.pack(side="left", padx=10)

exit_btn = tk.Button(root, text="Exit", width=20, height=2, command=exit)
exit_btn.pack(side="left", padx=10)

apkutils_btn = tk.Button(root, text="APK utils", width=20, height=2, command=apk)
apkutils_btn.pack(side="left", padx=10)

root.mainloop()
