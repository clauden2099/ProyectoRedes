import os

class Config:
    SECRET_KEY = "tu_clave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///inventario.db"  # Usamos SQLite por simplicidad
    SQLALCHEMY_TRACK_MODIFICATIONS = False
