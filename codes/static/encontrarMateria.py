import requests
from bs4 import BeautifulSoup

# Defina suas credenciais
USERNAME = '16137826759'  # Substitua pelo seu nome de usuário
PASSWORD = 'Pedromoreira1'  # Substitua pela sua senha

# URL de login e URL de busca
LOGIN_URL = 'https://portais.unirio.br/aluno/login.action'
TURMA_URL = 'https://portais.unirio.br/aluno/aluno/turma.action?turma={}'

# Cria uma sessão
session = requests.Session()


def login():
    # Prepara os dados para login
    payload = {
        'username': USERNAME,
        'password': PASSWORD,
    }

    # Faz a requisição POST para logar
    response = session.post(LOGIN_URL, data=payload)

    # Verifica se o login foi bem-sucedido
    if 'Login' in response.text:
        print("Login falhou. Verifique suas credenciais.")
        return False

    print("Login bem-sucedido.")
    return True


def find_turma(start, end):
    for turma in range(start, end + 1):
        url = TURMA_URL.format(turma)
        response = session.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            disciplina = soup.find('td', colspan="2",
                                   string=lambda text: text and "Metodologia Científica e Tecnológica" in text)

            if disciplina:
                print(f"Turma encontrada: {turma}")
                return turma

    print("Turma não encontrada.")
    return None


# Executa o processo
if login():
    find_turma(192000, 193000)
