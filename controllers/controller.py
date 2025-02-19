from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import Ingrediente, Producto, VentasTotales
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuarios
from models.roles import Roles
from app import db, login_manager
from datetime import timedelta


main = Blueprint('main', __name__)

ventas_dia=0


 ## Login

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            nombre = request.form['username']
            contraseña = request.form['password']
            id_rol = int(request.form['role_id'])
            email="prueba@gmail.com"
            telefono=32451235  # Nuevo campo para seleccionar el rol
            
            # Verificar si el rol existe
            role = Roles.query.get(id_rol)
            if not role:
                flash('Rol no válido', 'danger')
                return redirect(url_for('main.register'))
                
            # Verificar si el usuario ya existe
            existing_user = Usuarios.query.filter_by(nombre=nombre).first()
            if existing_user:
                flash('El nombre de usuario ya está en uso', 'warning')
                return redirect(url_for('main.register'))    
            
            hashed_password = generate_password_hash(contraseña)
            new_user = Usuarios(nombre=nombre,email=email, contraseña=hashed_password, telefono=telefono, id_rol=id_rol )
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()  # Deshacer la transacción si ocurre un error
            flash(f'Error en el registro: {str(e)}', 'danger')
        
    return render_template('register.html', roles=Roles.query.all())

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuarios.query.filter_by(nombre=username).first()

        if user and check_password_hash(user.contraseña, password):
            login_user(user)
            if user.id_rol == 1:
                session['username'] = username
                session['role'] = 'Residente'
                session.permanent = True
            elif user.id_rol == 2:
                session['username'] = username
                session['role'] = 'Administrador'
                session.permanent = True
            else:
                session['username'] = username
                session['role'] = 'employee'
                session.permanent = True
                  
            return redirect(url_for('main.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username, rol=current_user.roles.nombre)

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

##Listar Productos

@main.route('/')
def inicio():
    productos = Producto.query.all()
    return render_template('vista_inicial.html', productos=productos)
    

@main.route('/productos')
@login_required
@role_required('admin','employee', 'user')
def index():
  
    productos = Producto.query.all()
    mas_rentable = max(productos, key=lambda producto: producto.calcular_rentabilidad()).nombre
    acumulado_ventas = VentasTotales.query.first().acumulado if VentasTotales.query.first() else 0.0
    return render_template('index.html', productos=productos, mas_rentable=mas_rentable, ventas_dia=acumulado_ventas, rol=current_user.roles.nombre)
    
##Mostrar Ingredientes
@main.route('/ingredientes')
@login_required
@role_required('admin','employee')
def ingredientes():
        
    ingredientes = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingredientes, rol=current_user.roles.nombre)

##Agregar un Producto
@main.route('/producto/agregar', methods=['GET', 'POST'])
@role_required('admin','employee')
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_publico = request.form.get('precio')
        tipo = request.form.get('tipo')
        ingredientes_ids = request.form.getlist('ingredientes')  # Obtener IDs de los ingredientes seleccionados

        if not ingredientes_ids:
            flash('Seleccione Un Ingrediente', 'danger')
            return redirect(url_for('main.agregar_producto'))

        productos = Producto.query.all()
        if len(productos) == 4:
            flash('No Se Pueden Agregar Mas Productos (Max 4 Productos)', 'danger')
            return redirect(url_for('main.agregar_producto'))


        if len(ingredientes_ids) > 3:
            flash('Solo selecciona 3 ingredientes', 'danger')
            return redirect(url_for('main.agregar_producto'))

        # Crear el nuevo producto
        nuevo_producto = Producto(nombre=nombre, precio_publico=float(precio_publico), tipo=tipo)
        db.session.add(nuevo_producto)
        db.session.commit()

        # Relacionar ingredientes seleccionados con el producto
        for ingrediente_id in ingredientes_ids:
            ingrediente = Ingrediente.query.get(int(ingrediente_id))
            if ingrediente:
                nuevo_producto.ingredientes.append(ingrediente)
        
        db.session.commit()
        flash('Producto agregado con éxito', 'success')
        return redirect(url_for('main.index'))

    ingredientes = Ingrediente.query.all()  # Obtener todos los ingredientes
    return render_template('agregar_producto.html', ingredientes=ingredientes, rol=current_user.roles.nombre)

##Vender un producto
@main.route('/producto/vender', methods=['GET', 'POST'])
@login_required
@role_required('admin','employee','user')
def vender_producto():
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        producto = Producto.query.get(producto_id)
        if producto:
            # Lógica para verificar si hay suficiente inventario
            for ingrediente in producto.ingredientes:
                cantidad_necesaria = 1 if ingrediente.es_vegetariano else 0.2
                if ingrediente.inventario < cantidad_necesaria:
                    flash(f'¡Oh no! Nos hemos quedado sin {ingrediente.nombre}', 'danger')
                    return redirect(url_for('main.vender_producto'))
                
                # Descontar la cantidad necesaria del inventario
                ingrediente.inventario -= cantidad_necesaria

            VentasTotales.incrementar_venta(producto.precio_publico)    
            db.session.commit()
            flash('¡Vendido!', 'success')
        else:
            flash('El producto no existe.', 'danger')
        return redirect(url_for('main.vender_producto'))

    productos = Producto.query.all()
    return render_template('vender_producto.html', productos=productos, rol=current_user.roles.nombre)

##Agregar un ingrediente
@main.route('/ingrediente/agregar', methods=['GET', 'POST'])
@login_required
@role_required('admin','employee')
def agregar_ingrediente():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        calorias = request.form.get('calorias')
        inventario = request.form.get('inventario')
        es_vegetariano = request.form.get('es_vegetariano') == '1'
        tipo = request.form.get('tipo')
        
        nuevo_ingrediente = Ingrediente(nombre=nombre, precio=float(precio),calorias=int(calorias),inventario=int(inventario),es_vegetariano=es_vegetariano, tipo=tipo)
            
        # Guardar el nuevo ingrediente en la base de datos
        db.session.add(nuevo_ingrediente)
        db.session.commit()
        flash('Ingrediente agregado con éxito.', 'success')
        return redirect(url_for('main.agregar_ingrediente'))

    return render_template('agregar_ingrediente.html', rol=current_user.roles.nombre)

##Abastecer un producto
@main.route('/ingredientes/abastecer/<int:ingrediente_id>', methods=['GET','POST'])
@role_required('admin','employee')
def abastecer_ingrediente(ingrediente_id):
    if request.method == 'POST':
        #ingrediente_id = request.form.get('ingrediente_id')
        ingrediente = Ingrediente.query.get(ingrediente_id)

        if not ingrediente:
            flash('Seleccione Un Ingrediente', 'danger')
            return redirect(url_for('main.ingredientes'))
       
        ingrediente.abastecer()
        db.session.commit()
        flash(f'El inventario de {ingrediente.nombre} ha sido abastecido con éxito. {ingrediente.inventario}', 'success')
      

    ingre = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingre)


@main.route('/ingredientes/renovar/<int:ingrediente_id>', methods=['GET','POST'])
@role_required('admin','employee')
def renovar_ingrediente(ingrediente_id):
    if request.method == 'POST':
        #ingrediente_id = request.form.get('ingrediente_id')
        ingrediente = Ingrediente.query.get(ingrediente_id)
        
        # Verificar el tipo y abastecer según corresponda
        if ingrediente:
            ingrediente.renovar_inventario()
            db.session.commit()
            flash(f'El inventario de {ingrediente.nombre} ha sido renovado con éxito. {ingrediente.inventario}', 'success')
        else:
            flash('Error al renovar el ingrediente', 'danger')
            return redirect(url_for('main.ingredientes'))

    ingre = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingre)    


@main.route('/producto/editar/<int:producto_id>', methods=['POST'])
@role_required('admin')
def editar_producto(producto_id):
    """Ruta para editar un producto existente."""
    producto = Producto.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('main.index'))

    # Obtener los nuevos datos del formulario
    nuevo_nombre = request.form.get('nombre')
    nuevo_precio = request.form.get('precio')

    # Actualizar el producto
    producto.nombre = nuevo_nombre
    producto.precio_publico = float(nuevo_precio)
    db.session.commit()
    flash('Producto actualizado con éxito', 'success')

    return redirect(url_for('main.index'))

@main.route('/producto/eliminar/<int:producto_id>', methods=['POST'])
@role_required('admin')
def eliminar_producto(producto_id):
    """Ruta para eliminar un producto existente."""
    producto = Producto.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('main.index'))

    # Eliminar el producto
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito', 'success')

    return redirect(url_for('main.index'))


@main.route('/productos/rentabilidad', methods=['GET'])
@role_required('admin')
def rentabilidad_productos():

    # Obtener todos los productos
    productos = Producto.query.all()
    
    # Calcular la rentabilidad de cada producto
    for producto in productos:
        producto.rentabilidad = producto.calcular_rentabilidad()
    
    # Encontrar el producto más rentable
    producto_mas_rentable = max(productos, key=lambda p: p.rentabilidad) if productos else None

    return render_template('rentabilidad_productos.html', productos=productos, producto_mas_rentable=producto_mas_rentable)

@main.route('/no_autorizado')
def no_autorizado():
    return render_template('no_autorizado.html'), 403  # Código de estado HTTP 403 (Prohibido)
