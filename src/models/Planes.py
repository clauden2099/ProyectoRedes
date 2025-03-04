from src import db  # Importa la instancia de la base de datos desde el módulo src
from datetime import date  # Importa la clase date para manejar fechas

# Define el modelo Planes para gestionar planes de mantenimiento, configuración, etc.
class Planes(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de cada plan
    dispositivo = db.Column(db.String(100), nullable=False)  # Nombre o tipo de dispositivo asociado al plan
    descripcion = db.Column(db.Text, nullable=False)  # Descripción detallada del plan
    fecha = db.Column(db.Date, nullable=False)  # Fecha en la que se crea o aplica el plan
    responsable = db.Column(db.String(100), nullable=False)  # Persona responsable de ejecutar o supervisar el plan
    tipo_plan = db.Column(db.String(20), nullable=False)  # Tipo de plan (por ejemplo, "mantenimiento", "actualización", etc.)
    archivo_nombre = db.Column(db.String(255))  # Nombre del archivo adjunto, si existe (opcional)
    archivo_contenido = db.Column(db.LargeBinary)  # Contenido del archivo adjunto en formato binario (opcional)

    # Método para convertir la instancia del modelo a un diccionario, útil para respuestas JSON
    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),  # Convierte la fecha a formato ISO para compatibilidad JSON
            "responsable": self.responsable,
            "tipo_plan": self.tipo_plan,
            "archivo_nombre": self.archivo_nombre,  # No se incluye el contenido binario por razones de eficiencia
        }
