from flask import Blueprint, request, jsonify
from app import db, login_manager

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/facturas', methods=['POST'])
def generar_factura():
    data = request.json
    cur = db.connection.cursor()
    cur.execute("INSERT INTO facturas (id_casa, fecha_emision, fecha_vencimiento, monto, id_estado) VALUES (%s, %s, %s, %s, 1)",
                (data['id_casa'], data['fecha_emision'], data['fecha_vencimiento'], data['monto']))
    db.connection.commit()
    cur.close()
    return jsonify({"message": "Factura generada"}), 201

@billing_bp.route('/pagos', methods=['POST'])
def registrar_pago():
    data = request.json
    cur = db.connection.cursor()
    cur.execute("INSERT INTO pagos (id_factura, fecha_pago, monto_pagado, metodo_pago) VALUES (%s, %s, %s, %s)",
                (data['id_factura'], data['fecha_pago'], data['monto_pagado'], data['metodo_pago']))
    db.connection.commit()
    cur.execute("UPDATE facturas SET id_estado = 2 WHERE id = %s", (data['id_factura'],))
    db.connection.commit()
    cur.close()
    return jsonify({"message": "Pago registrado"}), 201
