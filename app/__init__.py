from flask import Flask
from config.settings import DB_CONFIG

def create_app():
    """Factory function para criar e configurar a aplicação Flask"""
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # Registrar rotas
    from app.routes import register_routes
    register_routes(app)
    
    return app