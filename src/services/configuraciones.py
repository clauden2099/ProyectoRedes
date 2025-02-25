from src.models.configuraciones import Configuraciones
from src import db
from datetime import datetime

def obtener_configuraciones():
    return [ticket.to_dict() for ticket in Configuraciones.query.all()]

#Agregar plan a la BD
def agrega(data):
    if "fecha" in data:
        data["fecha"] = datetime.fromisoformat(data["fecha"]).date()
    nuevaConfiguracion = Configuraciones(**data)
    db.session.add(nuevaConfiguracion)
    db.session.commit()
    return nuevaConfiguracion.to_dict()

#Actualizar plan BD
def actualizar(id, data):
    configuracion = Configuraciones.query.get(id)
    if configuracion:
        data.pop('id', None)  # Evita actualizar el campo id
        for key, value in data.items():
            if key == 'fecha' and isinstance(value,str):
                #Convierte la cadena a objeto date
                try:
                    value = datetime.fromisoformat(value).date()
                except ValueError:
                    continue
            setattr(configuracion, key, value)
        db.session.commit()
        return configuracion.to_dict()  # Retorna el objeto actualizado como diccionario
    return None

#Eliminar Plan BD
def eliminar(id):
    Configuracion = Configuraciones.query.get(id)
    if Configuracion:
        db.session.delete(Configuracion)
        db.session.commit()
        return Configuracion.to_dict()
    return None

