from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuarios
from models.roles import Roles
from models.casas import Casas
from app import db, login_manager
from datetime import timedelta
from controllers import usuarios


main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            contraseña = request.form['password']
            id_rol = int(request.form['id_rol'])
            id_casa = int(request.form['id_casa'])
            telefono= request.form['telefono']
            
            # Verificar si el rol existe
            role = Roles.query.get(id_rol)
            if not role:
                flash('Rol no válido', 'danger')
                return redirect(url_for('main.register'))
                
            # Verificar si el usuario ya existe
            existing_user = Usuarios.query.filter_by(email=email).first()
            if existing_user:
                flash('El nombre de usuario ya está en uso', 'warning')
                return redirect(url_for('main.register'))    
            
            hashed_password = generate_password_hash(contraseña)
            new_user = Usuarios(nombre=nombre,email=email, contraseña=hashed_password, telefono=telefono, id_rol=id_rol, id_casa=id_casa )
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('usuarios.listar_usuarios'))
        except Exception as e:
            db.session.rollback()  # Deshacer la transacción si ocurre un error
            flash(f'Error en el registro: {str(e)}', 'danger')
        
    return render_template('register.html', roles=Roles.query.all(), casas = Casas.query.all())

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuarios.query.filter_by(email=username).first()

        if user and check_password_hash(user.contraseña, password):
            login_user(user)
            if user.id_rol == 2:
                session['username'] = username
                session['role'] = 'Administrador'
                session.permanent = True
                return redirect(url_for('main.home_admin')) ##administrador - configurar vista
            else:
                session['username'] = username
                session['role'] = 'Residente'
                session.permanent = True
                return redirect(url_for('main.home_usuario')) ##residente - configurar vista
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

from functools import wraps

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('main.login'))

            #if current_user.is_authenticated or current_user.roles.nombre not in roles:
            if session.get('role') not in roles:
                flash('Acceso denegado.', 'danger')
                return redirect(url_for('main.no_autorizado'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main.route('/Administrador')
@login_required
@role_required('admin')
def admin_dashboard():
    return 'Panel de Administrador'

@main.route('/no_autorizado')
def no_autorizado():
    return render_template('no_autorizado.html'), 403  # Código de estado HTTP 403 (Prohibido)


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/admin')
@role_required('Administrador')
@login_required
def home_admin():
    return render_template('home_admin.html')

@main.route('/usuario')
@role_required('Residente')
@login_required
def home_usuario():
    return render_template('home_usuario.html')

@main.route('/reservas')
@login_required
def reservas():
    return render_template('reservas.html')

@main.route('/pqrs')
@login_required
def pqrs():
    return render_template('pqrs.html')

@main.route('/facturacion')
@login_required
def facturacion():
    return render_template('facturacion.html')

@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html')