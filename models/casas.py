from app import db

class Casas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    #usuarios = db.relationship('Usuarios', backref='casas', lazy=True)