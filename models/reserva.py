from app import db
from datetime import datetime, time


class Estado_reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)



class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_reserva.id'), nullable=False, default=1)
    comprobante_pago = db.Column(db.String(255))
    
    usuario = db.relationship("Usuarios", backref="solicitudes")
    estado = db.relationship("Estado_reserva", backref="solicitudes")
    facturas = db.relationship('Facturas', backref='reserva', cascade="all, delete-orphan")

class Facturas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_solicitud = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha_emision = db.Column(db.Date, default=datetime)
    comprobante_pago = db.Column(db.String(255))

    solicitud = db.relationship("Reserva", backref="factura")
    usuario = db.relationship("Usuarios", backref="facturas")


