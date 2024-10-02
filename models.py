# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Obrigatoria(db.Model):
    __tablename__ = 'Obrigatoria'
    id_disciplina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_disciplina = db.Column(db.String(20), nullable=False, unique=True)
    nome_disciplina = db.Column(db.String(255), nullable=False)
    ementa = db.Column(db.String(255))
    carga_horaria = db.Column(db.Integer)
    periodo_ideal = db.Column(db.String(10))

class Optativa(db.Model):
    __tablename__ = 'Optativa'
    id_optativa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_disciplina = db.Column(db.String(20), nullable=True, unique=True)
    nome_disciplina = db.Column(db.String(255), nullable=False)
    ementa = db.Column(db.String(255), nullable=True)
    carga_horaria = db.Column(db.Integer)
    periodo_ideal = db.Column(db.String(10))

class Requisito(db.Model):
    __tablename__ = 'Requisito'
    id_requisito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_disciplina = db.Column(db.Integer, db.ForeignKey('Obrigatoria.id_disciplina'), nullable=False)
    id_requisito_disciplina = db.Column(db.Integer, db.ForeignKey('Obrigatoria.id_disciplina'), nullable=False)
