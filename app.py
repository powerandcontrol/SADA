# app.py
from flask import Flask, render_template, request
from config import Config
from models import db, Obrigatoria, Optativa, Requisito
from database import carregar_dados_excel, carregar_dados_requisitos
import PyPDF2

app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
db.init_app(app)

# Inicializa as tabelas e carrega os dados do Excel no banco de dados
with app.app_context():
    db.create_all()  # Cria as tabelas apenas se não existirem
    carregar_dados_excel()  # Carrega os dados apenas se as tabelas estiverem vazias
    carregar_dados_requisitos()  # Carrega os dados dos requisitos
# Função para extrair o texto de um PDF diretamente do objeto FileStorage
def extrair_texto_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ''
    for page in reader.pages:
        texto += page.extract_text()
    return texto.lower()

# Função para buscar as matérias cursadas no texto extraído
def buscar_materias_cursadas(texto):
    cursadas_apv = []
    cursadas_adi = []

    for linha in texto.split('\n'):
        # Captura matérias APV
        if 'apv- aprovado' in linha:
            match = re.search(r'\b[a-z]{3}\d{4}\s+(.+?)\s+\d+\s+\d+,\d+\s+\d+,\d+\s+apv', linha)
            if match:
                nome_materia = match.group(1).strip()  # Captura o nome da matéria
                cursadas_apv.append(nome_materia.lower())  # Armazena em minúsculas

        # Captura matérias ADI
        if 'adi - aproveitamento de' in linha:
            match = re.search(r'\b[a-z]{3}\d{4}\s+(.+?)\s+\d+\s+\d+,\d+\s+adi\s+-\s+aproveitamento de \d+', linha)
            if match:
                nome_materia = match.group(1).strip()  # Captura o nome da matéria
                cursadas_adi.append(nome_materia.lower())  # Armazena em minúsculas

    return cursadas_apv, cursadas_adi


import re
import unicodedata

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

def gerar_relatorio(cursadas_apv, cursadas_adi):
    cursadas = set(cursadas_apv + cursadas_adi)
    curriculo_obrigatorias = Obrigatoria.query.all()
    curriculo_optativas = Optativa.query.all()

    materias_faltantes = {}
    requisitos_materiais_faltantes = {}
    total_materias = len(curriculo_obrigatorias)

    # Verifica as matérias faltantes nas obrigatórias
    for disciplina in curriculo_obrigatorias:
        if disciplina.nome_disciplina.lower() not in cursadas:
            periodo = disciplina.periodo_ideal
            if periodo not in materias_faltantes:
                materias_faltantes[periodo] = []
            # Verifica os requisitos para a disciplina faltante
            requisitos = Requisito.query.filter_by(id_disciplina=disciplina.id_disciplina).all()
            requisitos_ok = all(
                Obrigatoria.query.get(req.id_requisito_disciplina).nome_disciplina.lower() in cursadas
                for req in requisitos
            )

            # Adiciona a disciplina e o status dos requisitos
            disciplina.requisitos_ok = requisitos_ok  # Armazenando o status na disciplina
            materias_faltantes[periodo].append(disciplina)

            requisitos_materiais_faltantes[disciplina.nome_disciplina] = [
                Obrigatoria.query.get(req.id_requisito_disciplina).codigo_disciplina for req in requisitos
            ]
            print(
                f'Requisitos para {disciplina.nome_disciplina}: {requisitos_materiais_faltantes[disciplina.nome_disciplina]}')

    total_faltantes = sum(len(faltam) for faltam in materias_faltantes.values())
    total_cursadas = total_materias - total_faltantes
    percentual_cursado = (total_cursadas / total_materias) * 100

    # Cálculo das optativas
    total_optativas = 8  # Número total de optativas necessárias
    lista_optativas_cursadas = []

    # Filtra as optativas cursadas
    for optativa in curriculo_optativas:
        if optativa.nome_disciplina.lower() in cursadas:
            # Se a optativa não tem código, gera um com base no nome
            codigo_disciplina = optativa.codigo_disciplina if optativa.codigo_disciplina else gerar_codigo_disciplina(
                optativa.nome_disciplina)
            lista_optativas_cursadas.append({
                "codigo_disciplina": codigo_disciplina,
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
        "lista_optativas_cursadas": lista_optativas_cursadas  # Adiciona a lista de optativas cursadas
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado'

        file = request.files['file']

        # Processa o arquivo PDF enviado
        if file.filename != '':
            texto_pdf = extrair_texto_pdf(file)
            cursadas_apv, cursadas_adi = buscar_materias_cursadas(texto_pdf)

            relatorio = gerar_relatorio(cursadas_apv, cursadas_adi)

            # Redireciona para a página de resultados
            return render_template('resultado.html', relatorio=relatorio)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
