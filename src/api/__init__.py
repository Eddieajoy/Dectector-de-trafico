from flask import Flask
from src.api.routes import routes
import os

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='../../data')
    
    # Crear directorios necesarios
    os.makedirs('data/models', exist_ok=True)
    os.makedirs('data/videos', exist_ok=True)
    os.makedirs('data/output', exist_ok=True)
    
    # Registrar rutas
    app.register_blueprint(routes)
    
    return app 