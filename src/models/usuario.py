# Definir modelo de usuario
from src import db  # Importa la instancia de la base de datos desde el módulo src

# Modelo Usuario para gestionar los datos de los usuarios en la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único del usuario
    nombre = db.Column(db.String(150), nullable=False)  # Nombre del usuario (máximo 150 caracteres)
    password = db.Column(db.String(150), nullable=False)  # Contraseña almacenada (debe encriptarse antes de guardar)

    # Método para convertir la instancia del modelo a un diccionario, útil para respuestas JSON
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "password": self.password  
        }
