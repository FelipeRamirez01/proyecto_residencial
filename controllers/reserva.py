from flask import Blueprint, Response, render_template, request, redirect, url_for, flash, current_app, send_from_directory, send_file
from flask_login import login_required, current_user
from app import db, login_manager
from models.reserva import Reserva
from models.reserva import Facturas
from datetime import datetime, time
import uuid
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128

reserva_bp = Blueprint("reserva", __name__)

@reserva_bp.route('/mis_agendas')
@login_required
def mis_agendas():
    """Mostrar las reservas del usuario."""
    agendas = Reserva.query.filter_by(id_usuario=current_user.id).all()
    return render_template('reservas/mis_agendas.html', agendas=agendas)

@reserva_bp.route('/agendar_salon', methods=['GET', 'POST'])
@login_required
def agendar_salon():
    if request.method == 'POST':
        fecha = request.form['fecha']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        # Convertir valores a datetime
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_dt = datetime.strptime(hora_fin, "%H:%M").time()

        # VALIDAR DISPONIBILIDAD: Buscar reservas que coincidan en fecha y hora
        conflicto = Reserva.query.filter(
            Reserva.fecha == fecha_dt,
            Reserva.hora_inicio < hora_fin_dt,
            Reserva.hora_fin > hora_inicio_dt,
            Reserva.id_estado != 3  # No considerar solicitudes "Espera de Aprobacion"
        ).first()

        if conflicto:
            flash("El salón ya está reservado en ese horario. Por favor, elige otra fecha o franja horaria.", "danger")
            return redirect(url_for('agendar_salon'))

        # Si no hay conflicto, crear la solicitud
        nueva_solicitud = Reserva(
            id_usuario=current_user.id,
            fecha=fecha_dt,
            hora_inicio=hora_inicio_dt,
            hora_fin=hora_fin_dt,
            id_estado=1  # Estado "Pendiente"
        )
        db.session.add(nueva_solicitud)
        db.session.commit()

        # Generar factura por el uso del salón (ejemplo: $50.000)
        monto_salon = 50000
        nueva_factura = Facturas(
            id_solicitud=nueva_solicitud.id,
            id_usuario=current_user.id,
            monto=monto_salon,
            fecha_emision=datetime.now()
        )
        db.session.add(nueva_factura)
        db.session.commit()

        flash("Solicitud enviada. Estado: Pendiente. Factura generada.", "success")
        return redirect(url_for('reserva.mis_agendas'))

    return render_template('reservas/agendar_salon.html')


# Ruta donde se guardarán los PDFs
FACTURAS_DIR = "static/facturas"
os.makedirs(FACTURAS_DIR, exist_ok=True)

def generar_factura(usuario, reserva, monto):
    """Genera un PDF con la factura de la reserva del salón comunal."""
    archivo_pdf = os.path.join(FACTURAS_DIR, f"factura_{reserva.id}.pdf")
    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    
    # Agregar título y datos
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Factura - Conjunto Residencial XYZ")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Nombre: {usuario.nombre}")
    c.drawString(100, 700, f"Casa: {usuario.id_casa}")
    c.drawString(100, 680, f"Fecha de reserva: {reserva.fecha}")
    c.drawString(100, 660, f"Hora: {reserva.hora_inicio} - {reserva.hora_fin}")
    c.drawString(100, 640, f"Valor a pagar: ${monto}")

    # Agregar código de barras con el ID de la reserva
    barcode = code128.Code128(str(reserva.id), barHeight=20, barWidth=1.2)
    barcode.drawOn(c, 200, 500)

    # Guardar el PDF
    c.save()
    return archivo_pdf

@reserva_bp.route('/descargar_factura/<int:id>', methods=['POST'])
@login_required
def descargar_factura(reserva_id):
    """Permite descargar la factura de una reserva."""
    factura_path = os.path.join(FACTURAS_DIR, f"factura_{reserva_id}.pdf")
    if os.path.exists(factura_path):
        return send_file(factura_path, as_attachment=True)
    return "Factura no encontrada", 404
 

@reserva_bp.route('/editar_reserva/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reserva(id):
    """Modificar la fecha y hora de una reserva."""
    agenda = Reserva.query.get_or_404(id)

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        # Validar que la nueva fecha y hora no esté ocupada
        conflicto = Reserva.query.filter(
            Reserva.fecha == fecha,
            Reserva.hora_inicio < hora_fin,
            Reserva.hora_fin > hora_inicio,
            Reserva.id != id,
            Reserva.id_estado != 3
        ).first()

        if conflicto:
            flash("El salón ya está reservado en ese horario. Elige otro.", "danger")
            return redirect(url_for('editar_reserva', id=id))

        agenda.fecha = fecha
        agenda.hora_inicio = hora_inicio
        agenda.hora_fin = hora_fin
        db.session.commit()

        flash("Reserva actualizada correctamente.", "success")
        return redirect(url_for('reserva.mis_agendas'))

    return render_template('reservas/editar_reserva.html', agenda=agenda)


@reserva_bp.route('/eliminar_agenda/<int:id>', methods=['POST'])
@login_required
def eliminar_agenda(id):
    """Eliminar una reserva."""
    agenda = Reserva.query.get_or_404(id)

    if agenda.id_estado != 1:  # Solo se pueden eliminar reservas pendientes
        flash("No se puede eliminar una reserva ya aprobada.", "danger")
        return redirect(url_for('reserva.mis_agendas'))

    db.session.delete(agenda)
    db.session.commit()
    flash("Reserva eliminada correctamente.", "success")
    return redirect(url_for('reserva.mis_agendas'))

import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@reserva_bp.route('/subir_comprobante/<int:id>', methods=['POST'])
@login_required
def subir_comprobante(id):
    reserva = Reserva.query.filter_by(id=id).first()
    
    if 'comprobante' not in request.files:
        flash("No se seleccionó ningún archivo.", "danger")
        return redirect(url_for('reserva.mis_agendas'))

    file = request.files['comprobante']
    
    if file.filename == '':
        flash("Nombre de archivo inválido.", "danger")
        return redirect(url_for('reserva.mis_agendas'))

    if file and allowed_file(file.filename):
        file_ext = file.filename.rsplit('.', 1)[1].lower()  # Extrae la extensión
        unique_filename = f"comprobante_{id}_{uuid.uuid4().hex}.{file_ext}"  # Nombre único con UUID
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Si ya existe un comprobante previo, eliminarlo para evitar acumulación de archivos
        if reserva.comprobante_pago:
            old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], reserva.comprobante_pago)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        reserva.comprobante_pago = unique_filename
        db.session.commit()

        flash("Comprobante subido correctamente.", "success")
    else:
        flash("Formato de archivo no permitido.", "danger")
    
    return redirect(url_for('reserva.mis_agendas'))

@reserva_bp.route('/comprobante/<filename>')
def ver_comprobante(filename):
    comprobantes_dir = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(comprobantes_dir, filename)


