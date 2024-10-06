# app.py
from flask import Flask, render_template, request
from config import Config

from models import db, Eixo, Disciplina, Requisito  # Modifique para importar db também
from database import insertDisciplinas, insertRequisitos
import PyPDF2

import re
import unicodedata

app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
db.init_app(app)

# Inicializa as tabelas e carrega os dados do Excel no banco de dados
with app.app_context():
    db.create_all()  # Cria as tabelas apenas se não existirem
  #  insertDisciplinas()  # Carrega os dados apenas se as tabelas estiverem vazias
   # insertRequisitos()  # Carrega os dados dos requisitos

# Função para extrair o texto de um PDF diretamente do objeto FileStorage
def extrair_texto_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ''
    for page in reader.pages:
        texto += page.extract_text()  # Mantém o texto normal, sem lower()

    return texto

# Função para buscar as matérias cursadas no texto extraído (para CR - Aprovados)
def buscar_materias_cursadas(texto):
    cursadas = []

    for linha in texto.split('\n'):
        # Captura matérias APV com código
        if 'APV- Aprovado' in linha:
            match = re.search(r'\b([A-Z]{3}\d{4})\s+(.+?)\s+\d+\s+\d+,\d+\s+\d+,\d+\s+APV', linha)
            if match:
                codigo_materia = match.group(1).strip()  # Captura o código da matéria
                cursadas.append(codigo_materia)  # Armazena o código da disciplina
                print(f"Matéria APV encontrada: {codigo_materia}")  # Log


        # Captura matérias ADI com código
        if 'ADI - Aproveitamento de' in linha:
            match = re.search(r'\b([A-Z]{3}\d{4})\s+(.+?)\s+\d+\s+\d+,\d+\s+ADI\s+-\s+Aproveitamento de \d+', linha)
            if match:
                codigo_materia = match.group(1).strip()  # Captura o código da matéria
                cursadas.append(codigo_materia)  # Armazena o código da disciplina
                print(f"Matéria ADI encontrada: {codigo_materia}")  # Log

    return cursadas

def gerar_codigo_disciplina(nome_disciplina):
    if not nome_disciplina:
        return "ND"  # Retorna 'ND' se o nome da disciplina estiver vazio

    # Normaliza para remover acentos e caracteres especiais
    nome_normalizado = unicodedata.normalize('NFKD', nome_disciplina).encode('ASCII', 'ignore').decode('utf-8')

    # Remove palavras irrelevantes
    palavras_irrelevantes = {'de', 'da', 'do', 'dos', 'das', 'e', 'a', 'o', 'com', 'em'}

    # Divide o nome em palavras e remove palavras irrelevantes
    palavras = [palavra for palavra in nome_normalizado.split() if palavra.lower() not in palavras_irrelevantes]

    # Gera o código pegando as primeiras letras das palavras restantes
    codigo = ''.join([palavra[0].upper() for palavra in palavras])

    # Limita o código a um máximo de 5 caracteres (ajustável)
    return codigo[:5] if codigo else "ND"

def gerar_relatorio(cursadas_historico):
    cursadas = cursadas_historico
    curriculo_obrigatorias = Disciplina.query.filter_by(obrigatoria=True).all()
    curriculo_optativas = Disciplina.query.filter_by(obrigatoria=False).all()

    materias_faltantes = {}
    requisitos_materiais_faltantes = {}

    # Inicializa a lista de disciplinas por período
    disciplinas_por_periodo = {}

    # Verifica as matérias faltantes nas obrigatórias
    for disciplina in curriculo_obrigatorias:
        if disciplina.codigo_disciplina not in cursadas:  # Comparação com código
            periodo = disciplina.periodo_ideal
            if periodo not in disciplinas_por_periodo:
                disciplinas_por_periodo[periodo] = []  # Cria uma nova lista para o período

            # Verifica os requisitos para a disciplina faltante
            requisitos = Requisito.query.filter_by(codigo_disciplina=disciplina.codigo_disciplina).all()
            requisitos_ok = all(
                req.codigo_requisito in cursadas  # Verifica por código
                for req in requisitos
            )

            # Adiciona a disciplina e o status dos requisitos
            disciplina.requisitos_ok = requisitos_ok  # Armazenando o status na disciplina
            disciplinas_por_periodo[periodo].append(disciplina)

            # Armazena os códigos das disciplinas dos requisitos faltantes
            requisitos_materiais_faltantes[disciplina.nome_disciplina] = [
                Disciplina.query.get(req.codigo_requisito).nome_disciplina for req in requisitos
            ]

    # Ordena os períodos e as disciplinas dentro deles
    for periodo in sorted(disciplinas_por_periodo.keys()):
        materias_faltantes[periodo] = sorted(disciplinas_por_periodo[periodo], key=lambda d: d.nome_disciplina)

    total_faltantes = sum(len(faltam) for faltam in materias_faltantes.values())
    total_cursadas = len(curriculo_obrigatorias) - total_faltantes
    percentual_cursado = (total_cursadas / len(curriculo_obrigatorias)) * 100

    # Cálculo das optativas
    total_optativas = 8  # Número total de optativas necessárias
    lista_optativas_cursadas = []

    # Filtra as optativas cursadas
    for optativa in curriculo_optativas:
        if optativa.codigo_disciplina in cursadas:  # Comparação com código
            lista_optativas_cursadas.append({
                "codigo_disciplina": optativa.codigo_disciplina,
                "nome_disciplina": optativa.nome_disciplina,
                "ementa": optativa.ementa,
                "carga_horaria": optativa.carga_horaria,
            })

    optativas_cursadas = len(lista_optativas_cursadas)

    return {
        "cursadas": cursadas,
        "faltantes": materias_faltantes,
        "requisitos": requisitos_materiais_faltantes,
        "total_faltantes": total_faltantes,
        "total_cursadas": total_cursadas,
        "percentual_cursado": percentual_cursado,
        "optativas_cursadas": optativas_cursadas,
        "total_optativas": total_optativas,
        "lista_optativas_cursadas": lista_optativas_cursadas,
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado'

        file = request.files['file']
        tipo_historico = request.form.get('tipo_historico')  # Captura a escolha do usuário

        # Processa o arquivo PDF enviado
        if file.filename != '':
            texto_pdf = extrair_texto_pdf(file)

            # Verifica qual função usar com base no tipo de histórico selecionado
            if tipo_historico == 'cr_aprovados':
                cursadas_historico = buscar_materias_cursadas(texto_pdf)

            relatorio = gerar_relatorio(cursadas_historico)

            # Redireciona para a página de resultados
            return render_template('resultado.html', relatorio=relatorio)

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
