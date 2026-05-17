from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Debes iniciar sesión para acceder.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)

    with app.app_context():
        db.create_all()
        _crear_admin_por_defecto()

    return app

def _crear_admin_por_defecto():
    from app.models import Usuario
    if not Usuario.query.filter_by(correo='admin@votaciones.gt').first():
        admin = Usuario(
            nombre='Administrador',
            correo='admin@votaciones.gt',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
