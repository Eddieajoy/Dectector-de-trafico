from flask import Flask
from src.api.routes import routes

def create_app():
    app = Flask(__name__, 
                template_folder='src/templates',
                static_folder='src/static')
    app.register_blueprint(routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 