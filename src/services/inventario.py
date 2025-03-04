from src.models.inventario import Inventario
from src import db

# Función para obtener todos los dispositivos del inventario
def obtener_inventario():
    # Convierte cada objeto Inventario en un diccionario y lo devuelve como una lista
    return [item.to_dict() for item in Inventario.query.all()]

# Función para agregar un nuevo dispositivo al inventario
def agregar_dispositivo(data):
    # Crea una nueva instancia de Inventario con los datos recibidos
    nuevo = Inventario(**data)
    db.session.add(nuevo)  # Agrega el nuevo dispositivo a la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return nuevo.to_dict()  # Retorna el dispositivo agregado como diccionario

# Función para actualizar un dispositivo en el inventario
def actualizar_dispositivo(id, data):
    # Busca el dispositivo en la base de datos por su ID
    dispositivo = Inventario.query.get(id)
    if dispositivo:
        data.pop('id', None)  # Evita actualizar el campo ID
        for key, value in data.items():
            setattr(dispositivo, key, value)  # Actualiza los atributos del dispositivo
        
        db.session.commit()  # Guarda los cambios en la base de datos
        return dispositivo.to_dict()  # Retorna el dispositivo actualizado como diccionario
    return None  # Si el dispositivo no se encuentra, retorna None

# Función para eliminar un dispositivo del inventario
def eliminar_dispositivo(id):
    # Busca el dispositivo en la base de datos por su ID
    dispositivo = Inventario.query.get(id)
    if dispositivo:
        db.session.delete(dispositivo)  # Elimina el dispositivo de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return dispositivo.to_dict()  # Retorna el dispositivo eliminado como diccionario
    return None  # Si el dispositivo no se encuentra, retorna None
