import os

class Config:
    SECRET_KEY = "tu_clave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///inventario.db"  # Usamos SQLite por simplicidad
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración para la subida de archivos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png', 'docx', 'txt'}
