from flask import Blueprint, request, jsonify
from app import db, login_manager

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/reservas', methods=['POST'])
def reservar_salon():
    data = request.json
    cur = db.connection.cursor()
    cur.execute("INSERT INTO reservas_salon (id_usuario, fecha, hora_inicio, hora_fin, id_estado) VALUES (%s, %s, %s, %s, 1)",
                (data['id_usuario'], data['fecha'], data['hora_inicio'], data['hora_fin']))
    db.connection.commit()
    cur.close()
    return jsonify({"message": "Reserva creada"}), 201

@reservations_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM reservas_salon")
    reservas = cur.fetchall()
    cur.close()
    return jsonify(reservas)
