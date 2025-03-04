from src import db  # Importa la instancia de la base de datos desde el módulo src
from datetime import date  # Importa la clase date para manejar fechas

# Define el modelo Ticket para gestionar reportes o incidencias en los dispositivos
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de cada ticket
    dispositivo = db.Column(db.String(100), nullable=False)  # Nombre o tipo de dispositivo afectado
    descripcion = db.Column(db.Text, nullable=False)  # Descripción detallada del problema o solicitud
    fecha = db.Column(db.Date, nullable=False)  # Fecha en la que se registra el ticket
    responsable = db.Column(db.String(100), nullable=False)  # Persona asignada para resolver el ticket
    prioridad = db.Column(db.String(20), nullable=False)  # Nivel de prioridad (por ejemplo, "Alta", "Media", "Baja")
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")  # Estado del ticket ("Pendiente" o "Resuelto")

    # Método para convertir la instancia del modelo a un diccionario, útil para respuestas JSON
    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),  # Convierte la fecha a formato ISO para compatibilidad JSON
            "responsable": self.responsable,
            "prioridad": self.prioridad,
            "estado": self.estado
        }
