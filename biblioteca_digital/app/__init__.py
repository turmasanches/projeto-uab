from flask import Flask
from config import Config
from .database import inicializar_db

def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        inicializar_db()
        
    # Blueprints registration
    from .controllers.auth_controller import auth_bp
    from .controllers.admin_controller import admin_bp
    from .controllers.livro_controller import livros_bp
    from .controllers.emprestimo_controller import emprestimos_bp
    from .controllers.relatorio_controller import relatorios_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(livros_bp)
    app.register_blueprint(emprestimos_bp)
    app.register_blueprint(relatorios_bp)
    
    return app
