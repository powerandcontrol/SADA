# app.py
from flask import Flask, render_template, request
from config import Config
from models import db, Eixo, Disciplina, Requisito  # Modifique para importar db também
from database import insertDisciplinas, insertRequisitos

app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
db.init_app(app)

# Inicializa as tabelas e carrega os dados do Excel no banco de dados
with app.app_context():
    db.create_all()  # Cria as tabelas apenas se não existirem
    insertDisciplinas()  # Carrega os dados apenas se as tabelas estiverem vazias
    insertRequisitos()  # Carrega os dados dos requisitos
    
if __name__ == '_main_':
    app.run(debug=True)
    