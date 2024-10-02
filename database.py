# database.py
import pandas as pd
from models import db, Obrigatoria, Optativa, Requisito

def carregar_dados_excel():
    if Obrigatoria.query.count() == 0 and Optativa.query.count() == 0:
        obrigatorias_df = pd.read_excel('docs/2023.1/obrigatorias.xlsx')
        for _, row in obrigatorias_df.iterrows():
            nova_disciplina = Obrigatoria(
                codigo_disciplina=row['codigo_disciplina'],
                nome_disciplina=row['nome_disciplina'],
                ementa=row['ementa'],
                carga_horaria=row['carga_horaria'],
                periodo_ideal=row['periodo_ideal']
            )
            db.session.add(nova_disciplina)

        optativas_df = pd.read_excel('docs/2023.1/optativas.xlsx')
        for _, row in optativas_df.iterrows():
            nova_optativa = Optativa(
                codigo_disciplina=row['codigo_disciplina'],
                nome_disciplina=row['nome_disciplina'],
                ementa=row['ementa'],
                carga_horaria=row['carga_horaria'],
                periodo_ideal=row['periodo_ideal']
            )
            db.session.add(nova_optativa)

        db.session.commit()

def carregar_dados_requisitos():
    if Requisito.query.count() == 0:
        requisitos_df = pd.read_excel('docs/2023.1/requisitos.xlsx')
        for _, row in requisitos_df.iterrows():
            try:
                novo_requisito = Requisito(
                    id_disciplina=int(row['id_disciplina']),
                    id_requisito_disciplina=int(row['id_requisito'])
                )
                db.session.add(novo_requisito)
            except ValueError as e:
                print(f'Erro ao inserir requisito: {e}')
        db.session.commit()
