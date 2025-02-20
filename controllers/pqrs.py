from flask import Blueprint, request, jsonify
from app import db, login_manager

pqrs_bp = Blueprint('pqrs', __name__)

@pqrs_bp.route('/pqrs', methods=['POST'])
def crear_pqrs():
    data = request.json
    cur = db.connection.cursor()
    cur.execute("INSERT INTO pqrs (id_usuario, tipo, descripcion, id_estado) VALUES (%s, %s, %s, 1)",
                (data['id_usuario'], data['tipo'], data['descripcion']))
    db.connection.commit()
    cur.close()
    return jsonify({"message": "PQRS creada"}), 201

@pqrs_bp.route('/pqrs', methods=['GET'])
def listar_pqrs():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM pqrs")
    pqrs = cur.fetchall()
    cur.close()
    return jsonify(pqrs)
