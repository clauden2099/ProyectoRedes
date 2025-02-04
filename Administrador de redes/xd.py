import socket

def obtener_ip_local():
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return ip_local

# Obtén la IP local
ip_local = obtener_ip_local()
print(f"Tu dirección IP local es: {ip_local}")
