# models.py
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

import enum

db = SQLAlchemy()

# Definindo os Eixos a partir do Enum
class Eixo(enum.Enum):
    fundamentos_matematica = "Fundamentos da Matemática"
    gestao_empreendedorismo = "Gestão de Sistemas e Tecnologias da Informação, e Empreendedorismo e Inovação"
    programacao_algoritmos = "Programação e Algoritmos"
    engenharia_software = "Engenharia de Software"
    engenharia_dados = "Engenharia de Dados e Informação"
    infraestrutura = "Infraestrutura em Sistemas de Informação"
    sistemas_informacao = "Sistemas de Informação"
    desenvolvimento_pessoal = "Desenvolvimento Pessoal e Profissional"
    formacao_complementar = "Formação Complementar"
    atividades_extensao = "Atividades de Extensão"
    atividades_complementares = "Atividades Complementares"
    trabalho_conclusao = "Trabalho de Conclusão de Curso"

# Definindo a tabela Disciplina
class Disciplina(db.Model):
    __tablename__ = 'disciplina'

    codigo_disciplina = db.Column(db.String(7), primary_key=True)  # Identificador único da disciplina (TIN0206)
    nome_disciplina = db.Column(db.String(255), nullable=False)  # Nome completo da disciplina
    periodo_ideal = db.Column(db.Integer)  # Período ideal, exemplo: 1, 2, 3
    carga_horaria = db.Column(db.Integer)  # Carga horária em horas
    ementa = db.Column(db.String(600))  # Ementa da matéria, se disponível
    obrigatoria = db.Column(db.Boolean, default=True) # Se a matéria é obrigatória ou optativa
    eixo = db.Column(db.Enum(Eixo), nullable=False)

# Definindo a tabela Requisito
class Requisito(db.Model):
    __tablename__ = 'requisito'

    codigo_disciplina = db.Column(db.String(7), db.ForeignKey('disciplina.codigo_disciplina'), primary_key=True)  # Identificador da disciplina que possui requisitos
    codigo_requisito = db.Column(db.String(7), db.ForeignKey('disciplina.codigo_disciplina'), primary_key=True)  # Identificador do requisito (disciplina que é um requisito)

    disciplina = relationship("Disciplina", foreign_keys=[codigo_disciplina])  # Relacionamento com Disciplina
    requisito_disciplina = relationship("Disciplina", foreign_keys=[codigo_requisito])  # Relacionamento com Disciplina

class QuadroHorarios(db.Model):
    __tablename__ = 'quadro-horarios-2024'

    id_disciplina = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo_disciplina = db.Column(db.String(7), db.ForeignKey('disciplina.codigo_disciplina'))  # Identificador da disciplina que possui requisitos
    professor = db.Column(db.String(255))
    dias = db.Column(db.String(255))
    horario = db.Column(db.String(255))
    sala = db.Column(db.String(255))

    disciplina = relationship("Disciplina", foreign_keys=[codigo_disciplina])  # Relacionamento com Disciplina
