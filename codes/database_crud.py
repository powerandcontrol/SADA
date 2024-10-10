import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa o Flask e o SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historico_escolar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para a tabela de disciplinas obrigatórias
class Obrigatoria(db.Model):
    __tablename__ = 'Obrigatoria'
    id_disciplina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_disciplina = db.Column(db.String(20), nullable=False, unique=True)
    nome_disciplina = db.Column(db.String(255), nullable=False)
    ementa = db.Column(db.String(255))
    carga_horaria = db.Column(db.Integer)
    periodo_ideal = db.Column(db.String(10))

# Modelo para a tabela de disciplinas optativas
class Optativa(db.Model):
    __tablename__ = 'Optativa'
    id_optativa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_disciplina = db.Column(db.String(20), nullable=True, unique=True)
    nome_disciplina = db.Column(db.String(255), nullable=False)
    ementa = db.Column(db.String(255), nullable=True)
    carga_horaria = db.Column(db.Integer)
    periodo_ideal = db.Column(db.String(10))

# Modelo para a tabela de requisitos
class Requisito(db.Model):
    __tablename__ = 'Requisito'
    id_requisito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_disciplina = db.Column(db.Integer, db.ForeignKey('Obrigatoria.id_disciplina'), nullable=False)
    id_requisito_disciplina = db.Column(db.Integer, db.ForeignKey('Obrigatoria.id_disciplina'), nullable=False)

def listar_disciplinas_obrigatorias():
    """Lista todas as disciplinas obrigatórias."""
    disciplinas = Obrigatoria.query.all()
    return disciplinas

def encontrar_disciplina_obrigatoria(id_disciplina):
    """Encontra uma disciplina obrigatória pelo ID."""
    disciplina = Obrigatoria.query.get(id_disciplina)
    return disciplina

def buscar_disciplinas_por_nome(nome):
    """Busca disciplinas obrigatórias pelo nome."""
    disciplinas = Obrigatoria.query.filter(Obrigatoria.nome_disciplina.ilike(f'%{nome}%')).all()
    return disciplinas

def contar_disciplinas_obrigatorias():
    """Conta o número total de disciplinas obrigatórias."""
    total = Obrigatoria.query.count()
    return total

def buscar_disciplinas_por_carga_horaria(carga_horaria):
    """Busca disciplinas obrigatórias com carga horária específica."""
    disciplinas = Obrigatoria.query.filter_by(carga_horaria=carga_horaria).all()
    return disciplinas

def listar_disciplinas_optativas():
    """Lista todas as disciplinas optativas."""
    disciplinas = Optativa.query.all()
    return disciplinas

def listar_requisitos():
    """Lista todas as disciplinas optativas."""
    requisitos = Requisito.query.all()
    return requisitos

def listar_requisitos_disciplina(id_disciplina):
    """Lista os requisitos de uma disciplina obrigatória."""
    requisitos = Requisito.query.filter_by(id_disciplina=id_disciplina).all()
    return requisitos

# Função principal para executar consultas via linha de comando
def main():
    with app.app_context():
        while True:
            print("\n--- Consultas ao Banco de Dados ---")
            print("1. Listar Disciplinas Obrigatórias")
            print("2. Encontrar Disciplina Obrigatória pelo ID")
            print("3. Buscar Disciplinas Obrigatórias pelo Nome")
            print("4. Contar Disciplinas Obrigatórias")
            print("5. Buscar Disciplinas Obrigatórias por Carga Horária")
            print("6. Listar Disciplinas Optativas")
            print("7. Listar Requisitos de uma Disciplina Obrigatória")
            print("8. Listar Requisitos")
            print("0. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                disciplinas = listar_disciplinas_obrigatorias()
                for disciplina in disciplinas:
                    print(f"{disciplina.id_disciplina} - {disciplina.codigo_disciplina} - {disciplina.nome_disciplina}")

            elif opcao == '2':
                id_disciplina = int(input("Digite o ID da disciplina: "))
                disciplina = encontrar_disciplina_obrigatoria(id_disciplina)
                if disciplina:
                    print(f"{disciplina.codigo_disciplina} - {disciplina.nome_disciplina}")
                else:
                    print("Disciplina não encontrada.")

            elif opcao == '3':
                nome = input("Digite o nome da disciplina: ")
                disciplinas = buscar_disciplinas_por_nome(nome)
                for disciplina in disciplinas:
                    print(f"{disciplina.codigo_disciplina} - {disciplina.nome_disciplina}")

            elif opcao == '4':
                total = contar_disciplinas_obrigatorias()
                print(f"Total de disciplinas obrigatórias: {total}")

            elif opcao == '5':
                carga_horaria = int(input("Digite a carga horária: "))
                disciplinas = buscar_disciplinas_por_carga_horaria(carga_horaria)
                for disciplina in disciplinas:
                    print(f"{disciplina.codigo_disciplina} - {disciplina.nome_disciplina}")

            elif opcao == '6':
                disciplinas = listar_disciplinas_optativas()
                for disciplina in disciplinas:
                    print(f"{disciplina.id_optativa} - {disciplina.nome_disciplina}")

            elif opcao == '7':
                id_disciplina = int(input("Digite o ID da disciplina para listar requisitos: "))
                requisitos = listar_requisitos_disciplina(id_disciplina)
                if requisitos:
                    print("Requisitos:")
                    for requisito in requisitos:
                        disciplina_requisito = Obrigatoria.query.get(requisito.id_requisito_disciplina)
                        if disciplina_requisito:
                            print(f"{disciplina_requisito.codigo_disciplina} - {disciplina_requisito.nome_disciplina}")
                else:
                    print("Nenhum requisito encontrado para essa disciplina.")

            elif opcao == '8':
                requisitos = listar_requisitos()
                for requisito in requisitos:
                    print(f"{requisito.id_disciplina} - {requisito.id_requisito_disciplina}")

            elif opcao == '0':
                print("Saindo...")
                break

            else:
                print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    main()
