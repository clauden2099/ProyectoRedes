import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import json
import socket
import sys
sys.path.append('/ruta/a/scapy')
from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup

# Obtener la IP local
def obtener_ip_local():
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return ip_local

# Almacenar datos en memoria
data_store = {
    "faults": [],
    "devices": {},
    "plans": []
}

def scan_network():
    ip_local = obtener_ip_local()
    # Cambia la máscara de subred según tu configuración de red
    network = ip_local + "/24"
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]

    devices = {}
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        try:
            # Obtener el nombre del host
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Desconocido"

        # Obtener el fabricante de la dirección MAC
        try:
            vendor = MacLookup().lookup(mac)
        except Exception:
            vendor = "Desconocido"

        devices[ip] = {
            "MAC": mac,
            "Hostname": hostname,
            "Vendor": vendor
        }
    
    data_store["devices"] = devices
    messagebox.showinfo("Escaneo completado", f"{len(devices)} dispositivos encontrados.")

def show_devices():
    devices_text.delete("1.0", tk.END)
    for ip, info in data_store["devices"].items():
        devices_text.insert(tk.END, f"IP: {ip}\nMAC: {info['MAC']}\nHostname: {info['Hostname']}\nVendor: {info['Vendor']}\n\n")

# Configurar interfaz gráfica
root = tk.Tk()
root.title("Administrador de Red")

scan_btn = tk.Button(root, text="Escanear Red", command=scan_network)
scan_btn.pack()

devices_text = scrolledtext.ScrolledText(root, width=50, height=15)
devices_text.pack()
show_devices_btn = tk.Button(root, text="Mostrar Dispositivos", command=show_devices)
show_devices_btn.pack()

root.mainloop()
