# database.py
from models import db, Eixo, Disciplina, Requisito
import pandas as pd
import re

df = pd.read_excel("docs/2023.1/reforma-bsi-quadro-materias.xlsx")

def retornaEixo(eixo):
    if "Atividades de extensão" in eixo:
        return Eixo.atividades_extensao
    elif "Desenvolvimento Pessoal e Profissional" in eixo:
        return Eixo.desenvolvimento_pessoal
    elif "Engenharia de Software" in eixo:
        return Eixo.engenharia_software
    elif "Programação e Algoritmos" in eixo:
        return Eixo.programacao_algoritmos
    elif "Engenharia de Dados e Informação" in eixo:
        return Eixo.engenharia_dados
    elif "Formação Complementar" in eixo:
        return Eixo.formacao_complementar
    elif "Gestão de SI e TI" in eixo:
        return Eixo.gestao_empreendedorismo
    elif "Infraestrutura em SI" in eixo:
        return Eixo.infraestrutura
    elif "Trabalho de conclusão de curso" in eixo:
        return Eixo.trabalho_conclusao
    elif "Visão Sistêmica (Sistemas de Informação)":
        return Eixo.sistemas_informacao
    elif "Fundamentos de Matemática" in eixo:
        return Eixo.fundamentos_matematica


def retornaPeriodo(periodo):
    return int(periodo.replace("º", ""))


def retornaCargaHoraria(carga_horaria):
    carga_horaria = carga_horaria.split('/')[0]
    carga_horaria = carga_horaria.replace('h', "")
    return int(carga_horaria)


def retornaTipo(tipo):
    return True if tipo == 1 else False


def retornaEmenta(ementa):
    return re.sub(' +', ' ', ementa)


def retornaRequisitos(pre_requisitos):
    return [elem.strip() for elem in pre_requisitos.split(',')]

def insertDisciplinas():
    for index, row in df.iterrows():
        eixo = retornaEixo(row['Eixo'])
        codigo = row['Código SIE']
        nome = row['Disciplina']
        periodo = retornaPeriodo(row['Período'])
        carga_horaria = retornaCargaHoraria(row['CH Total'])
        tipo = retornaTipo(row['Tipo'])
        ementa = retornaEmenta(row['Ementa'])

        nova_disciplina = Disciplina(eixo=eixo, codigo_disciplina=codigo, nome_disciplina=nome, periodo_ideal=periodo,
                                     carga_horaria=carga_horaria, ementa=ementa, obrigatoria=tipo)
        db.session.add(nova_disciplina)

    db.session.commit()


def insertRequisitos():
    for index, row in df.iterrows():
        nome = row['Disciplina']
        disciplina = Disciplina.query.filter_by(nome_disciplina=nome).first()

        if disciplina:
            if row["Pré-requisitos"] != '—':
                lista_requisitos = retornaRequisitos(row["Pré-requisitos"])
                for nome_requisito in lista_requisitos:
                    requisito = Disciplina.query.filter_by(nome_disciplina=nome_requisito).first()
                    if requisito:
                        novo_requisito = Requisito(codigo_disciplina=disciplina.codigo_disciplina,
                                                   codigo_requisito=requisito.codigo_disciplina)
                        db.session.add(novo_requisito)
                    else:
                        print(f"Não encontrei o requisito {nome_requisito} no banco de dados")
        else:
            print(f"Não encontrei a matéria {nome} no banco de dados")

    db.session.commit()