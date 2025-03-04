from src.models.configuraciones import Configuraciones
from src import db
from datetime import datetime

# Obtener todas las configuraciones almacenadas en la base de datos
def obtener_configuraciones():
    return [config.to_dict() for config in Configuraciones.query.all()]

# Agregar una nueva configuración a la base de datos
def agrega(data):
    if "fecha" in data:
        try:
            data["fecha"] = datetime.fromisoformat(data["fecha"]).date()  # Convertir fecha de string a objeto date
        except ValueError:
            return {"error": "Formato de fecha inválido"}, 400  # Manejo de error en caso de formato incorrecto

    nuevaConfiguracion = Configuraciones(**data)
    db.session.add(nuevaConfiguracion)
    db.session.commit()
    return nuevaConfiguracion.to_dict()

# Actualizar una configuración existente en la base de datos
def actualizar(id, data):
    configuracion = Configuraciones.query.get(id)
    if configuracion:
        data.pop('id', None)  # Evita actualizar el campo ID

        for key, value in data.items():
            if key == 'fecha' and isinstance(value, str):
                # Convertir fecha en formato ISO a objeto date
                try:
                    value = datetime.fromisoformat(value).date()
                except ValueError:
                    continue  # Si hay error en la fecha, se ignora la actualización de este campo

            setattr(configuracion, key, value)  # Asigna el nuevo valor al atributo correspondiente
        
        db.session.commit()
        return configuracion.to_dict()  # Retorna el objeto actualizado como diccionario
    
    return None  # Retorna None si el ID no existe

# Eliminar una configuración de la base de datos
def eliminar(id):
    configuracion = Configuraciones.query.get(id)
    if configuracion:
        db.session.delete(configuracion)
        db.session.commit()
        return configuracion.to_dict()  # Retorna la configuración eliminada como confirmación
    
    return None  # Retorna None si el ID no existe
