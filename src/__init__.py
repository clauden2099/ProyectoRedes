from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Importar y registrar las rutas
    from src.routes.main import main_bp
    from src.routes.inventario_controller import inventario_bp
    from src.routes.redes_controller import listaRedes_bp
    from src.routes.escanearDispositivos_controller import escanearDispositivos_bp
    from src.routes.ticket_controller import ticket_bp
    from src.routes.planes_controller import plan_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(listaRedes_bp)
    app.register_blueprint(escanearDispositivos_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(plan_bp)

    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
    
    return app
