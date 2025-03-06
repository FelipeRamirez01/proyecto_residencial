from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models.reserva import Reserva
from app import db


admin_reservas_bp = Blueprint('admin_reservas', __name__)

UPLOAD_FOLDER = 'static/comprobantes'  # Carpeta donde se guardan los comprobantes

@admin_reservas_bp.route('/reservas')
@login_required
def listar_reservas_admin():
    if current_user.id_rol != 2:  # Solo el administrador puede acceder
        flash("No tienes permisos para acceder a esta sección.", "danger")
        return redirect(url_for('main.home'))
    
    reservas = Reserva.query.all()
    return render_template('reservas/listar_reservas.html', reservas=reservas)

@admin_reservas_bp.route('/reserva/aprobar/<int:id>', methods=['POST'])
@login_required
def aprobar_reserva(id):
    if current_user.id_rol != 2:
        flash("No tienes permisos para realizar esta acción.", "danger")
        return redirect(url_for('admin_reservas.listar_reservas_admin'))
    
    reserva = Reserva.query.get_or_404(id)
    reserva.id_estado = 2
    db.session.commit()
    flash("Reserva aprobada correctamente.", "success")
    return redirect(url_for('admin_reservas.listar_reservas_admin'))

@admin_reservas_bp.route('/comprobante/<filename>')
@login_required
def ver_comprobante(filename):
    comprobante_path = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(comprobante_path, filename)
