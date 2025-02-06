import socket as verRed
import tkinter as tk


def ver_red_local():
    hostname = verRed.gethostname()
    ip_local = verRed.gethostbyname(hostname)
    return ip_local

#Ip Local
ip_local = ver_red_local()
print("Tu dirección ip local es: " + ip_local)


root = tk.Tk()
root.title("página principal")

# Escaneo de la red
scan_btn = tk.Button(root, text="Escanear Red")
scan_btn.pack()

root.mainloop()
