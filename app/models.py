from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(20), default="atendente")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Pacote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.String(150), nullable=False)
    periodo = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    vagas_min = db.Column(db.Integer, nullable=False)
    vagas_max = db.Column(db.Integer, nullable=False)
    vagas_disponiveis = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(150), nullable=False)
    cliente_email = db.Column(db.String(150))
    cliente_telefone = db.Column(db.String(50))
    pacote_id = db.Column(db.Integer, db.ForeignKey("pacote.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    data_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="ativa")
