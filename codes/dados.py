import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Configurações da base de dados
DATABASE_URL = "sqlite:///historico_escolar.db"  # Use SQLite para simplicidade
Base = declarative_base()

# Definindo a tabela Disciplina
class Obrigatoria(Base):
    __tablename__ = 'Obrigatoria'

    id_disciplina = Column(Integer, primary_key=True)  # Identificador único da disciplina
    codigo_disciplina = Column(String(20), nullable=False)  # Código da disciplina, exemplo: 'GPN'
    nome_disciplina = Column(String(255), nullable=False)  # Nome completo da disciplina
    ementa = Column(String(255))  # Link para a ementa da disciplina, se aplicável
    carga_horaria = Column(Integer)  # Carga horária em horas
    periodo_ideal = Column(String(10))  # Período ideal, exemplo: '1º', '2º', '3º'

# Definindo a tabela Requisito
class Requisito(Base):
    __tablename__ = 'Requisito'

    id_disciplina = Column(Integer, ForeignKey('Obrigatoria.id_disciplina'),
                           primary_key=True)  # Identificador da disciplina que possui requisitos
    id_requisito = Column(Integer, ForeignKey('Obrigatoria.id_disciplina'),
                          primary_key=True)  # Identificador do requisito (disciplina que é um requisito)

    disciplina = relationship("Obrigatoria", foreign_keys=[id_disciplina])  # Relacionamento com Obrigatoria
    requisito_disciplina = relationship("Obrigatoria", foreign_keys=[id_requisito])  # Relacionamento com Obrigatoria


# Definindo a tabela Optativa
class Optativa(Base):
    __tablename__ = 'Optativa'

    id_optativa = Column(Integer, primary_key=True)  # Identificador único da optativa
    codigo_disciplina = Column(String(20), nullable=True)  # Código da disciplina, pode ser NULL
    nome_disciplina = Column(String(255), nullable=False)  # Nome completo da disciplina
    ementa = Column(String(255), nullable=True)  # Link para a ementa da disciplina, pode ser NULL
    carga_horaria = Column(Integer)  # Carga horária em horas
    periodo_ideal = Column(String(10))  # Período ideal, exemplo: '1º', '2º', '3º'

# Criando a engine e as tabelas (inclui a nova tabela Optativas)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Criando uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo dados do arquivo Excel para Disciplina
def insert_data_from_excel(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        obrigatoria = Obrigatoria(
            codigo_disciplina=row['codigo_disciplina'],
            nome_disciplina=row['nome_disciplina'],
            ementa=row['ementa'],
            carga_horaria=row['carga_horaria'],
            periodo_ideal=row['periodo_ideal']
        )
        session.add(obrigatoria)

    session.commit()

# Inserindo dados do arquivo Excel para Optativas
def insert_optativas_from_excel(file_path):
    # Lê os dados do arquivo Excel
    df = pd.read_excel(file_path)

    # Adiciona as optativas ao banco de dados
    for _, row in df.iterrows():
        optativa = Optativa(
            codigo_disciplina=row['codigo_disciplina'],  # Pode ser NaN (nulo) sem problemas
            nome_disciplina=row['nome_disciplina'],
            ementa=row['ementa'],  # Pode ser NaN (nulo) sem problemas
            carga_horaria=row['carga_horaria'],
            periodo_ideal=row['periodo_ideal']
        )
        session.add(optativa)

    session.commit()


# Relatório para Disciplina
def relatorio():
    obrigatorias = session.query(Obrigatoria).all()
    print("----------------------------------------------------------")
    print(f"{'Nome da Disciplina':<30} | {'Código':<10} | {'Ementa':<30} | {'Carga Horária':<15} | {'Período Ideal':<15} | {'Requisitos'}")
    print("----------------------------------------------------------")

    for obrigatoria in obrigatorias:
        requisitos = session.query(Requisito).filter(Requisito.id_disciplina == obrigatoria.id_disciplina).all()
        obrigatoria_info = (
            f"{obrigatoria.nome_disciplina:<30} | "
            f"{obrigatoria.codigo_disciplina:<10} | "
            f"{obrigatoria.ementa:<30} | "
            f"{obrigatoria.carga_horaria:<15} | "
            f"{obrigatoria.periodo_ideal:<15}"
        )
        if requisitos:
            requisitos_nomes = []
            for r in requisitos:
                disciplina_requisito = session.query(Obrigatoria).filter(Obrigatoria.id_disciplina == r.id_requisito).first()
                if disciplina_requisito:
                    requisitos_nomes.append(disciplina_requisito.nome_disciplina)
                else:
                    requisitos_nomes.append('Desconhecido')
            requisitos_info = ', '.join(requisitos_nomes)
            print(f"{obrigatoria_info} | {requisitos_info}")
        else:
            print(f"{obrigatoria_info} | Nenhum requisito")

    print("----------------------------------------------------------")


# Relatório para Optativas
def relatorio_optativas():
    optativas = session.query(Optativa).all()  # Busca todas as optativas
    print(
        "Nome da Optativa               | Código     | Ementa                         | Carga Horária   | Período Ideal")
    print("----------------------------------------------------------")
    for optativa in optativas:
        # Usa 'N/A' se o valor for None
        codigo = optativa.codigo_disciplina if optativa.codigo_disciplina is not None else 'N/A'
        ementa = optativa.ementa if optativa.ementa is not None else 'N/A'

        print(
            f"{optativa.nome_disciplina:<30} | "
            f"{codigo:<10} | "
            f"{ementa:<30} | "
            f"{optativa.carga_horaria:<15} | "
            f"{optativa.periodo_ideal:<15}"
        )

# Rodando as funções
insert_data_from_excel('docs/2023.1/obrigatórias.xlsx')  # Insere os dados do Excel
insert_optativas_from_excel('docs/2023.1/optativas.xlsx')  # Insere os dados do Excel
relatorio()  # Imprime as disciplinas
relatorio_optativas()  # Imprime as optativas
