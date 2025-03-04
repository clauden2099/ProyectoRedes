from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
import os

# Instancia de SQLAlchemy para gestionar la base de datos
db = SQLAlchemy()

# Función para crear la aplicación Flask
def create_app():
    app = Flask(__name__)  # Crea la instancia de la aplicación Flask
    app.config.from_object(Config)  # Carga la configuración desde la clase Config en src.config

    db.init_app(app)  # Inicializa la base de datos con la aplicación Flask

    # Crear carpeta de uploads si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Importar y registrar los blueprints (rutas organizadas en controladores)
    from src.routes.main import main_bp
    from src.routes.inventario_controller import inventario_bp
    from src.routes.redes_controller import listaRedes_bp
    from src.routes.escanearDispositivos_controller import escanearDispositivos_bp
    from src.routes.ticket_controller import ticket_bp
    from src.routes.planes_controller import plan_bp
    from src.routes.configuraciones_controller import configuracion_bp
    from src.routes.usuario_controller import usuario_bp

    # Registrar cada blueprint en la aplicación
    app.register_blueprint(main_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(listaRedes_bp)
    app.register_blueprint(escanearDispositivos_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(configuracion_bp)
    app.register_blueprint(usuario_bp)

    # Dentro del contexto de la aplicación, crear las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()

    return app  # Retorna la aplicación Flask inicializada
