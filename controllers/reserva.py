from flask import Blueprint, Response, render_template, request, redirect, url_for, flash, send_file, current_app, send_from_directory, send_file
from flask_login import login_required, current_user
from app import db, login_manager
from models.reserva import Reserva
from models.reserva import Facturas
from models.usuario import Usuarios
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
        horario = request.form['horario']
        descripcion = request.form['descripcion']


        # Convertir valores a datetime
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

        # Validar que los campos no estén vacíos
        if not fecha or not horario or not descripcion:
            flash('Error: Todos los campos son obligatorios.', 'danger')
            return render_template('reservas/agendar_salon.html')

        # Validar que la descripción no supere los 300 caracteres
        if len(descripcion) > 300:
            flash('Error: La descripción no puede superar los 300 caracteres.', 'danger')
            return render_template('reservas/agendar_salon.html')

        # Validar que la fecha y el horario no estén ocupados (evitar duplicados)
        reserva_existente = Reserva.query.filter_by(fecha=fecha, horario=horario).first()
        if reserva_existente:
            flash('Error: La fecha y el horario ya están reservados. Por favor elige otra fecha u horario.', 'danger')
            return render_template('reservas/agendar_salon.html')


       # Crear la nueva reserva
        nueva_reserva = Reserva(
            usuario_id=current_user.id,
            fecha=fecha,
            horario=horario,
            descripcion=descripcion,
            estado=1
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        # Generar factura por el uso del salón (ejemplo: $50.000)
        monto_salon = 50000
        nueva_factura = Facturas(
            id_solicitud=nueva_reserva.id,
            id_usuario=current_user.id,
            monto=monto_salon,
            fecha_emision=datetime.now()
        )
        db.session.add(nueva_factura)
        db.session.commit()

        flash("Solicitud enviada. Estado: Pendiente. Factura generada.", "success")
        return redirect(url_for('reserva.mis_agendas'))

    return render_template('reservas/agendar_salon.html')


@reserva_bp.route('/descargar_factura/<int:id>', methods=['GET'])
@login_required
def descargar_factura(id):
    factura = Facturas.query.get_or_404(id)
    
    # Generar la factura en PDF
    filepath = generar_factura_pdf(factura)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash("Error al generar la factura.", "danger")
        return redirect(url_for('reserva.mis_agendas'))


def generar_factura_pdf(factura):
    filename = f"factura_{factura.id}.pdf"
    #filepath = os.path.join("static\facturas", filename)
    filepath = f"static\facturas\{filename}"

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Agregar encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Factura de Pago - Conjunto Residencial")

    # Agregar información del usuario
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Usuario: {factura.usuario.nombre}")
    c.drawString(50, height - 120, f"Casa: {factura.usuario.casa.numero}")
    c.drawString(50, height - 140, f"Valor a Pagar: ${factura.monto:.2f}")

    # Generar el código de barras (Convertido correctamente)
    barcode_value = str(factura.id)
    barcode = code128.Code128(barcode_value, barHeight=40, barWidth=1.2)

    # Dibujar el código de barras directamente en el PDF
    barcode.drawOn(c, 200, height - 250)

    # Guardar el PDF
    c.showPage()
    c.save()

    return filepath

def generar_factura_pdf(factura):
    filename = f"factura_{factura.id}.pdf"
    #filepath = os.path.join("static\facturas", filename)
    filepath = f"static\facturas\{filename}"

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Agregar encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Factura de Pago - Conjunto Residencial")

    # Agregar información del usuario
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Usuario: {factura.usuario.nombre}")
    c.drawString(50, height - 120, f"Casa: {factura.usuario.casa.numero}")
    c.drawString(50, height - 140, f"Valor a Pagar: ${factura.monto:.2f}")

    # Generar el código de barras (Convertido correctamente)
    barcode_value = str(factura.id)
    barcode = code128.Code128(barcode_value, barHeight=40, barWidth=1.2)

    # Dibujar el código de barras directamente en el PDF
    barcode.drawOn(c, 200, height - 250)

    # Guardar el PDF
    c.showPage()
    c.save()

    return filepath

@reserva_bp.route('/editar_reserva/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reserva(id):
    """Modificar la fecha y hora de una reserva."""
    agenda = Reserva.query.get_or_404(id)

    if request.method == 'POST':
        nueva_fecha = request.form['fecha']
        nuevo_horario = request.form['horario']
        nueva_descripcion = request.form['descripcion']

        # Verificar si ya existe una reserva en la misma fecha y horario (excepto la actual)
        reserva_existente = Reserva.query.filter(
            Reserva.fecha == nueva_fecha,
            Reserva.horario == nuevo_horario,
            Reserva.id != agenda.id  # Excluir la reserva actual
        ).first()

        if reserva_existente:
            flash('Error: La fecha y el horario ya están reservados. Por favor elige otra fecha u horario.', 'danger')
            return render_template('reservas/editar_agenda.html', agenda=agenda)

        # Actualizar los valores de la reserva
        agenda.fecha = nueva_fecha
        agenda.horario = nuevo_horario
        agenda.descripcion = nueva_descripcion
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


