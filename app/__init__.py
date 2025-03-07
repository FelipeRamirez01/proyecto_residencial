from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

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
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    from controllers.reserva import reserva_bp
    app.register_blueprint(reserva_bp, url_prefix='/reserva')

    from controllers.admin_reservas import admin_reservas_bp
    app.register_blueprint(admin_reservas_bp, url_prefix='/admin')


    #UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'comprobantes')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/comprobantes')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    #with app.app_context():
     #   db.create_all()

    return app
