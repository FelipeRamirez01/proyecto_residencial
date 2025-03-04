from flask import Blueprint, Response, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
import pdfkit 
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
from app import db, login_manager
from models.reserva import Reserva
from models.reserva import Facturas
from datetime import datetime, time

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
            Reserva.id_estado != 3  # No considerar solicitudes "Resueltas" (canceladas)
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

#@reserva_bp.route('/ver_solicitudes')
#@login_required
#def ver_solicitudes():
    solicitudes = Reserva.query.filter_by(id_usuario=current_user.id).all()
    return render_template('ver_solicitudes.html', solicitudes=solicitudes)


@reserva_bp.route('/descargar_factura/<int:id>')
@login_required
def descargar_factura(id):
    factura = Facturas.query.get_or_404(id)

    options = {
    "enable-local-file-access": "",  # Permite acceder a archivos locales
    "disable-smart-shrinking": ""    # Evita errores de escalado
    }

    html = render_template('reservas/factura_pdf.html', factura=factura)
    pdf = pdfkit.from_string(html, "factura.pdf", options=options)

    response = Response(pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename=factura_{factura.id}.pdf'
    return response

@reserva_bp.route('/generar_factura/<int:id>', methods=['POST'])
@login_required
def generar_factura(id):
    """Volver a generar la factura."""
    agenda = Reserva.query.get_or_404(id)

    nueva_factura = Facturas(
        id_solicitud=agenda.id,
        id_usuario=current_user.id,
        monto=50000,  # Monto del alquiler del salón
        fecha_emision=datetime.now()
    )
    db.session.add(nueva_factura)
    db.session.commit()

    flash("Factura generada nuevamente.", "success")
    return redirect(url_for('reserva.mis_agendas'))




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
        return redirect(url_for('mis_agendas'))

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
    """Subir el comprobante de pago y cambiar el estado de la reserva."""
    factura = Reserva.query.filter_by(id=id).first()


    if 'comprobante' not in request.files:
        flash("No seleccionaste un archivo.", "danger")
        return redirect(url_for('mis_agendas'))

    file = request.files['comprobante']

    if file.filename == '':
        flash("Nombre de archivo inválido.", "danger")
        return redirect(url_for('mis_agendas'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Guardar la ruta en la base de datos y cambiar estado
        factura.comprobante_pago = filename
        #solicitud = Reserva.query.get_or_404(id)
        factura.id_estado = 2  # Estado: "Espera de Aprobación"
        db.session.commit()

        flash("Comprobante subido. Solicitud en espera de aprobación.", "success")
    else:
        flash("Formato de archivo no permitido.", "danger")

    return redirect(url_for('reserva.mis_agendas'))

@reserva_bp.route('/comprobante/<filename>')
def ver_comprobante(filename):
    comprobantes_dir = os.path.join(current_app.root_path, 'static', 'comprobantes')
    return send_from_directory(comprobantes_dir, filename)
