from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
import os
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../views')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/conjunto_residencial'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Clave secreta para manejar sesiones y seguridad
    app.config['SECRET_KEY'] = os.urandom(24)  # Genera una clave aleatoria
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Ruta para login obligatorio


    from controllers.controller import main
    app.register_blueprint(main)

    from controllers.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp)


    from controllers.reserva import reserva_bp
    ##app.register_blueprint(reserva_bp)


    #with app.app_context():
     #   db.create_all()

    return app
