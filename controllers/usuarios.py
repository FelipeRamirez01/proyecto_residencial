from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app import db
from models.usuario import Usuarios
from models.casas import Casas
from models.roles import Roles

usuarios_bp = Blueprint("usuarios", __name__)

# Mostrar lista de usuarios
@usuarios_bp.route("/usuarios")
@login_required
def listar_usuarios():
    usuarios = Usuarios.query.all()
    roles = Roles.query.all()
    

    return render_template("usuarios.html", usuarios=usuarios)

# Editar usuario
@usuarios_bp.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    roles = Roles.query.all()
    casas = Casas.query.all()

    if request.method == "POST":
        usuario.nombre = request.form["nombre"]
        usuario.email = request.form["email"]
        usuario.telefono = request.form["telefono"]
        usuario.id_rol = request.form["id_rol"]
        usuario.id_casa = request.form["id_casa"]

        nueva_contraseña = request.form['contraseña']
        if nueva_contraseña:
            usuario.contraseña = generate_password_hash(nueva_contraseña)

        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("editar_usuario.html", usuario=usuario, roles=roles, casas=casas)

# Eliminar usuario
@usuarios_bp.route("/eliminar_usuario/<int:id>", methods=["POST"])
@login_required
def eliminar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("usuarios.listar_usuarios"))
