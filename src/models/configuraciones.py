from src import db  # Importa la instancia de la base de datos desde el módulo src

# Define el modelo Configuraciones para la base de datos
class Configuraciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de la configuración
    dispositivo = db.Column(db.String(100), nullable=False)  # Nombre del dispositivo asociado
    descripcion = db.Column(db.Text, nullable=False)  # Descripción detallada de la configuración
    fecha = db.Column(db.Date, nullable=False)  # Fecha en que se registró la configuración
    responsable = db.Column(db.String(100), nullable=False)  # Persona responsable de la configuración
    archivo_nombre = db.Column(db.String(255))  # Nombre del archivo adjunto (opcional)
    archivo_contenido = db.Column(db.LargeBinary)  # Contenido del archivo en formato binario

    # Método para convertir la instancia del modelo a un diccionario, útil para respuestas JSON
    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),  # Convierte la fecha a string en formato ISO 8601
            "responsable": self.responsable,
            "archivo_nombre": self.archivo_nombre,  # Se devuelve solo el nombre del archivo, no su contenido
        }
