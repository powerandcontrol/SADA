# app.py
from flask import Flask, render_template, request
from config import Config
from utils import *

#
from models import db, Eixo, Disciplina, Requisito, QuadroHorarios
from database import insertDisciplinas, insertRequisitos


app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH,
            static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
db.init_app(app)

"""# Inicializa as tabelas e carrega os dados do Excel no banco de dados
with app.app_context():
    db.create_all()  # Cria as tabelas apenas se não existirem
    # insertDisciplinas()  # Carrega os dados apenas se as tabelas estiverem vazias
    # insertRequisitos()  # Carrega os dados dos requisitos
"""


@app.route('/add', methods=['GET', 'POST'])
def add():
    disciplina = QuadroHorarios(
        codigo_disciplina=f"TIN0206",
    )
    db.session.add(disciplina)
    db.session.commit()
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado'

        file = request.files['file']
        tipo_historico = request.form.get(
            'tipo_historico')  # Captura a escolha do usuário

        # Processa o arquivo PDF enviado
        if file.filename != '':
            texto_pdf = extrair_texto_pdf(file)

            # Verifica qual função usar com base no tipo de histórico selecionado
            if tipo_historico == 'cr_aprovados':
                cursadas_historico = buscar_materias_cursadas(texto_pdf, 'cr_aprovados')
            elif tipo_historico == 'integralizacao':
                cursadas_historico = buscar_materias_cursadas(texto_pdf, 'integralizacao')

            relatorio = gerar_relatorio(cursadas_historico)

            # Redireciona para a página de resultados
            return render_template('resultado.html', relatorio=relatorio)

    return render_template('index.html')

@app.route('/test_index', methods=['GET', 'POST'])
def test_index():
    if request.method:

        file = 'Historico_Teste_CRAprovados.pdf'
        if file:
            texto_pdf = extrair_texto_pdf(file)
            cursadas_historico = buscar_materias_cursadas(texto_pdf, 'cr_aprovados')
            relatorio = gerar_relatorio(cursadas_historico)
            return render_template('resultado.html', relatorio=relatorio)

    return render_template('index.html')

@app.route('/test_add', methods=['GET', 'POST'])

def test_add():
    qd = QuadroHorarios(codigo_disciplina = "TIN0206")
    db.session.add(qd)
    db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
