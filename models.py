from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

from sqlalchemy import CheckConstraint  # Certifique-se de importar CheckConstraint

class Clinica(db.Model):
    __tablename__ = 'clinica'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    endereco = db.Column(db.String(255))
    latitude = db.Column(db.Numeric(10, 8))  
    longitude = db.Column(db.Numeric(11, 8))  
    tipo = db.Column(db.Enum('veterinário', 'médico'), nullable=False)
    avaliacao = db.Column(db.Numeric(3, 2))  
    horario = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('avaliacao >= 0 AND avaliacao <= 5', name='check_avaliacao'),
    )
    
class Servicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)

class Clinica_Servico(db.Model):
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinica.id'), primary_key=True)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), primary_key=True)

class usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
