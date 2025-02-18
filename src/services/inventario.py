from src.models.inventario import Inventario
from src import db

def obtener_inventario():
    return [item.to_dict() for item in Inventario.query.all()]

def agregar_dispositivo(data):
    nuevo = Inventario(**data)
    db.session.add(nuevo)
    db.session.commit()
    return nuevo.to_dict()

def actualizar_dispositivo(id, data):
    dispositivo = Inventario.query.get(id)
    if dispositivo:
        data.pop('id', None)  # Evita actualizar el campo id
        for key, value in data.items():
            setattr(dispositivo, key, value)
        db.session.commit()
        return dispositivo.to_dict()  # Retorna el objeto actualizado como diccionario
    return None


def eliminar_dispositivo(id):
    dispositivo = Inventario.query.get(id)
    if dispositivo:
        db.session.delete(dispositivo)
        db.session.commit()
        return dispositivo.to_dict()
    return None


