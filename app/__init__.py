from flask import Flask, send_from_directory
import os
from config.settings import DB_CONFIG

def create_app():
    """Factory function para criar e configurar a aplicação Flask"""
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # Registrar rotas
    from app.routes import register_routes
    register_routes(app)
    
    # Rota especial para garantir carregamento do favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, '../static/image'),
                                   'logo_carreta.ico', mimetype='image/vnd.microsoft.icon')
    
    return app