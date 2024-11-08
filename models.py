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

# Modelo para Informações Médicas dos Usuários
class Informacoes_Medicas(db.Model):
    __tablename__ = 'informacoes_medicas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo_sanguineo = db.Column(db.String(3))  # Exemplo: 'A+', 'O-', etc.
    comorbidades = db.Column(db.Text)
    alergias = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    historico_familiar = db.Column(db.Text)
    observacoes = db.Column(db.Text)

# Modelo para Informações dos Pets dos Usuários
class Informacoes_Pet(db.Model):
    __tablename__ = 'informacoes_pet'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    especie = db.Column(db.String(255), nullable=False)  # Exemplo: 'Cachorro', 'Gato', etc.
    raca = db.Column(db.String(255))
    idade = db.Column(db.Integer)
    peso = db.Column(db.Numeric(5, 2))  # Peso em kg com 2 casas decimais
    alergias = db.Column(db.Text)
    condicoes_medicas = db.Column(db.Text)
    observacoes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('idade >= 0', name='check_idade_pet'),
        CheckConstraint('peso >= 0', name='check_peso_pet'),
    )

class usuario(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date)
    genero = db.Column(db.Enum('Masculino', 'Feminino', 'Outro', name="genero"))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))