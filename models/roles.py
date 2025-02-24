from app import db

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    #usuarios = db.relationship('Usuarios', backref='roles', lazy=True)