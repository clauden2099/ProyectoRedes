import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import json
import socket
import sys
from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
import paramiko

# Obtener la IP local
def obtener_ip_local():
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return ip_local

# Almacenar datos en memoria
data_store = {
    "faults": [],
    "devices": {},
    "inventory": [],
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

def ping_device(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response != 0:
        data_store["faults"].append(ip)
        messagebox.showwarning("Fallo detectado", f"El dispositivo {ip} no responde.")

def add_prevention_plan():
    plan = plan_text.get("1.0", tk.END).strip()
    if plan:
        data_store["plans"].append(plan)
        plan_text.delete("1.0", tk.END)
        messagebox.showinfo("Plan agregado", "Plan guardado en memoria.")

def show_devices():
    devices_text.delete("1.0", tk.END)
    for ip, info in data_store["devices"].items():
        devices_text.insert(tk.END, f"IP: {ip}\nMAC: {info['MAC']}\nHostname: {info['Hostname']}\nVendor: {info['Vendor']}\n\n")

def show_faults():
    faults_text.delete("1.0", tk.END)
    for fault in data_store["faults"]:
        faults_text.insert(tk.END, f"{fault}\n")

def add_to_inventory():
    device_ip = inv_ip_entry.get().strip()
    device_name = inv_name_entry.get().strip()
    device_location = inv_location_entry.get().strip()
    
    if device_ip and device_name and device_location:
        data_store["inventory"].append({
            "IP": device_ip,
            "Name": device_name,
            "Location": device_location
        })
        messagebox.showinfo("Inventario actualizado", "Dispositivo agregado al inventario.")
    else:
        messagebox.showwarning("Campos incompletos", "Por favor, llena todos los campos.")

def show_inventory():
    inventory_text.delete("1.0", tk.END)
    for device in data_store["inventory"]:
        inventory_text.insert(tk.END, f"IP: {device['IP']}\nNombre: {device['Name']}\nUbicación: {device['Location']}\n\n")

def configure_device():
    device_ip = config_ip_entry.get().strip()
    
    if device_ip in data_store["devices"]:
        config_window = tk.Toplevel(root)
        config_window.title(f"Configuración de {device_ip}")
        
        # Cambio de nombre de host
        hostname_label = tk.Label(config_window, text="Nombre del host:")
        hostname_label.pack()
        hostname_entry = tk.Entry(config_window)
        hostname_entry.pack()
        hostname_entry.insert(0, data_store["devices"][device_ip]["Hostname"])

        # Cambio de dirección IP
        ip_label = tk.Label(config_window, text="Dirección IP:")
        ip_label.pack()
        ip_entry = tk.Entry(config_window)
        ip_entry.pack()
        ip_entry.insert(0, device_ip)

        # Cambio de Puerta de Enlace
        gateway_label = tk.Label(config_window, text="Puerta de Enlace:")
        gateway_label.pack()
        gateway_entry = tk.Entry(config_window)
        gateway_entry.pack()

        # Configuración de DNS
        dns_label = tk.Label(config_window, text="Servidores DNS:")
        dns_label.pack()
        dns_entry = tk.Entry(config_window)
        dns_entry.pack()

        # Botón para aplicar cambios
        apply_btn = tk.Button(config_window, text="Aplicar Cambios", command=lambda: apply_config_changes(device_ip, hostname_entry.get(), ip_entry.get(), gateway_entry.get(), dns_entry.get()))
        apply_btn.pack()
    else:
        messagebox.showwarning("Dispositivo no encontrado", "La dirección IP no está en la lista de dispositivos encontrados.")


def apply_config_changes(ip, hostname, new_ip, gateway, dns):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conecta al dispositivo usando SSH
        ssh.connect(ip, username='tu_usuario', password='tu_contraseña')
        
        # Cambia el nombre del host (esto es un ejemplo, los comandos reales pueden variar)
        if hostname:
            ssh.exec_command(f'hostnamectl set-hostname {hostname}')
        
        # Cambia la dirección IP (ejemplo de comando, ajustar según el dispositivo)
        if new_ip:
            ssh.exec_command(f'nmcli con modify "Conexión cableada 1" ipv4.addresses {new_ip}/24')
            ssh.exec_command('nmcli con down "Conexión cableada 1"')
            ssh.exec_command('nmcli con up "Conexión cableada 1"')
        
        # Cambia la puerta de enlace (ejemplo de comando)
        if gateway:
            ssh.exec_command(f'nmcli con modify "Conexión cableada 1" ipv4.gateway {gateway}')
        
        # Cambia los DNS (ejemplo de comando)
        if dns:
            ssh.exec_command(f'nmcli con modify "Conexión cableada 1" ipv4.dns {dns}')

        ssh.close()
        messagebox.showinfo("Cambios aplicados", "Los cambios de configuración se han aplicado correctamente.")
    except Exception as e:
        messagebox.showerror("Error de configuración", f"No se pudieron aplicar los cambios: {str(e)}")


# Configurar interfaz gráfica
root = tk.Tk()
root.title("Administrador de Red")

# Escaneo de la red
scan_btn = tk.Button(root, text="Escanear Red", command=scan_network)
scan_btn.pack()

# Mostrar dispositivos
devices_text = scrolledtext.ScrolledText(root, width=50, height=10)
devices_text.pack()
show_devices_btn = tk.Button(root, text="Mostrar Dispositivos", command=show_devices)
show_devices_btn.pack()

# Mostrar fallas
faults_text = scrolledtext.ScrolledText(root, width=50, height=5)
faults_text.pack()
show_faults_btn = tk.Button(root, text="Mostrar Fallos", command=show_faults)
show_faults_btn.pack()

# Agregar plan de prevención
plan_text = scrolledtext.ScrolledText(root, width=50, height=5)
plan_text.pack()
add_plan_btn = tk.Button(root, text="Agregar Plan de Prevención", command=add_prevention_plan)
add_plan_btn.pack()

# Inventario
inv_ip_label = tk.Label(root, text="IP del dispositivo:")
inv_ip_label.pack()
inv_ip_entry = tk.Entry(root)
inv_ip_entry.pack()

inv_name_label = tk.Label(root, text="Nombre del dispositivo:")
inv_name_label.pack()
inv_name_entry = tk.Entry(root)
inv_name_entry.pack()

inv_location_label = tk.Label(root, text="Ubicación del dispositivo:")
inv_location_label.pack()
inv_location_entry = tk.Entry(root)
inv_location_entry.pack()

add_inventory_btn = tk.Button(root, text="Agregar al Inventario", command=add_to_inventory)
add_inventory_btn.pack()

inventory_text = scrolledtext.ScrolledText(root, width=50, height=10)
inventory_text.pack()
show_inventory_btn = tk.Button(root, text="Mostrar Inventario", command=show_inventory)
show_inventory_btn.pack()

# Interfaz de configuración de dispositivos
config_ip_label = tk.Label(root, text="IP del dispositivo a configurar:")
config_ip_label.pack()
config_ip_entry = tk.Entry(root)
config_ip_entry.pack()

config_device_btn = tk.Button(root, text="Configurar Dispositivo", command=configure_device)
config_device_btn.pack()

root.mainloop()
