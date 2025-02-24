from app import db
from flask_login import UserMixin

class Usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15))
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    id_casa = db.Column(db.Integer, db.ForeignKey('casas.id'), nullable=False)

    rol = db.relationship("Roles", backref="usuarios")
    casa = db.relationship("Casas", backref="residentes")