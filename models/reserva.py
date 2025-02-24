from app import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados_reserva.id'), nullable=False, default="Pendiente")  # Pendiente, Aprobada, Rechazada


