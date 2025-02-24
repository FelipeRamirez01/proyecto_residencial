from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.reserva import Reserva
from datetime import datetime, time

reserva_bp = Blueprint("reserva", __name__)

@reserva_bp.route("/reservar_salon", methods=["GET", "POST"])
@login_required
def reservar_salon():
    if request.method == "POST":
        fecha = request.form["fecha"]
        hora_inicio = request.form["hora_inicio"]
        hora_fin = request.form["hora_fin"]

        # Convertir las cadenas en objetos de fecha y hora
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_obj = datetime.strptime(hora_fin, "%H:%M").time()

        # Verificar disponibilidad
        reserva_existente = Reserva.query.filter(
            Reserva.fecha == fecha_obj,
            Reserva.hora_inicio < hora_fin_obj,
            Reserva.hora_fin > hora_inicio_obj
        ).first()

        if reserva_existente:
            flash("El salón ya está reservado en ese horario.", "error")
        else:
            nueva_reserva = Reserva(
                usuario_id=current_user.id,
                fecha=fecha_obj,
                hora_inicio=hora_inicio_obj,
                hora_fin=hora_fin_obj,
                estado="Pendiente"
            )
            db.session.add(nueva_reserva)
            db.session.commit()
            flash("Reserva realizada con éxito. Esperando aprobación.", "success")

        return redirect(url_for("reserva.reservar_salon"))

    reservas = Reserva.query.order_by(Reserva.fecha.desc()).all()
    return render_template("reservar_salon.html", reservas=reservas)
