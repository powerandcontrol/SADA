import PyPDF2
import re
from termcolor import colored
from colorama import init
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Inicializa o colorama para compatibilidade com o Windows
init()

# Função para extrair o texto de um PDF
def extrair_texto_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto = ''
        for page in reader.pages:
            texto += page.extract_text()
        return texto.lower()  # Converte todo o texto para minúsculas

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

# Função para gerar o relatório com cores
def gerar_relatorio(cursadas_apv, cursadas_adi, curriculo):
    cursadas = set(cursadas_apv + cursadas_adi)  # Combina as listas de APV e ADI em um conjunto
    materias_faltantes = {}
    cores = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    total_materias = sum(len(materias) for periodo, materias in curriculo.items() if periodo != "disciplinas optativas e extensão")

    for periodo, materias in curriculo.items():
        if periodo != "disciplinas optativas e extensão":  # Ignora optativas
            faltam = [materia for materia in materias if materia.lower() not in cursadas]
            materias_faltantes[periodo] = faltam

    total_faltantes = sum(len(faltam) for faltam in materias_faltantes.values())
    total_cursadas = total_materias - total_faltantes
    percentual_cursado = (total_cursadas / total_materias) * 100

    print(colored("Matérias cursadas (APV e ADI):", 'green'))
    for materia in cursadas:
        print(f"- {materia}")

    print(colored("\n\nMatérias faltantes:", 'red'))
    for i, (periodo, faltam) in enumerate(materias_faltantes.items()):
        cor = cores[i % len(cores)]  # alterna as cores para cada período
        print(colored(f"{periodo}:", cor))
        for materia in faltam:
            print(f"- {materia}")

    # Cálculo e exibição do total de optativas
    total_optativas = 8  # Número total de optativas necessárias
    optativas_cursadas = sum(1 for materia in cursadas if materia in curriculo["disciplinas optativas e extensão"])

    print(f"\nTotal de matérias faltantes (obrigatórias): {total_faltantes}")
    print(f"Total de matérias cursadas (obrigatórias): {total_cursadas}")
    print(f"Total de optativas cursadas: {optativas_cursadas}/{total_optativas}")
    print(f"Percentual do curso já cursado (obrigatórias): {percentual_cursado:.2f}%")

# Função para abrir a janela e escolher o arquivo PDF
def selecionar_arquivo_pdf():
    Tk().withdraw()  # Esconde a janela principal do Tkinter
    arquivo = askopenfilename(title="Selecione o arquivo PDF do histórico escolar",
                               filetypes=[("PDF files", "*.pdf")])
    return arquivo

# Caminho para o arquivo PDF
pdf_path = selecionar_arquivo_pdf()

# Extração do texto e busca das matérias cursadas
if pdf_path:
    texto_pdf = extrair_texto_pdf(pdf_path)
    cursadas_apv, cursadas_adi = buscar_materias_cursadas(texto_pdf)

    # Listas e dicionário de matérias (currículo) em minúsculas
    curriculo = {
        "1º período": ["fundamentos de sistemas de informação", "informação e sociedade",
                       "interação humano-computador", "fundamentos de cálculo", "algoritmos e programação",
                       "arquitetura de computadores"],
        "2º período": ["álgebra linear", "cálculo diferencial e integral i", "fundamentos de gestão organizacional",
                       "gestão de processos de negócios", "introdução à lógica computacional",
                       "técnicas de programação"],
        "3º período": ["cálculo diferencial e integral ii", "estruturas de dados", "linguagens e paradigmas de programação",
                       "análise e projeto de sistemas", "modelagem da informação", "sistemas operacionais"],
        "4º período": ["projeto integrador ii", "probabilidade", "redes de computadores",
                       "engenharia de software i", "projeto e análise de algoritmos",
                       "armazenamento e gestão de dados"],
        "5º período": ["metodologia científica e tecnológica", "estatística", "governança e planejamento de ti",
                       "engenharia de software ii", "gerência de projetos", "engenharia de software ii"],
        "6º período": ["ciência de dados", "empreendedorismo e inovação"],
        "disciplinas optativas e extensão": [
            "acessibilidade", "cibercultura", "ciência de redes", "desenvolvimento de páginas web",
            "informática na educação", "novas formas de economia", "pensamento computacional",
            "pensamento sistêmico", "projeto de aplicação de sistemas de informação em um contexto específico",
            "sistemas colaborativos", "teorias e práticas de sistemas de informação",
            "tópicos em informática na educação", "tópicos em gestão de processos de negócio",
            "tópicos em gestão do conhecimento", "tópicos em inovação tecnológica",
            "tópicos em propriedade intelectual", "algoritmos para ciência de dados",
            "algoritmos para problemas combinatórios", "análise multiparadigma de algoritmos",
            "aplicações de pesquisa operacional", "aprendizagem profunda", "estruturas de dados avançadas",
            "estruturas discretas com algoritmos", "estudo de problemas de otimização combinatória",
            "fluxos em redes", "fundamentos de representação de conhecimento e raciocínio",
            "heurísticas inteligentes: técnicas e aplicações", "introdução à inteligência artificial",
            "introdução algorítmica a grafos", "modelagem e ontologias", "processamento baseado em restrições",
            "programação linear", "técnicas de programação avançada", "tópicos em algoritmos",
            "tópicos em aplicações de lógica e raciocínio automatizado", "tópicos em aprendizagem de máquina",
            "tópicos em engenharia de ontologias", "tópicos em processamento de linguagem natural",
            "desenvolvimento de servidor web", "engenharia de sistemas complexos",
            "interfaces móveis", "projeto de jogos digitais", "tópicos em arquitetura de software",
            "tópicos em aspectos humanos, econômicos e sociais de software", "tópicos em construção de software",
            "tópicos em engenharia de requisitos", "tópicos em engenharia de software experimental",
            "tópicos em gerência de configuração de software", "tópicos em gerência de projetos",
            "tópicos em manutenção de software", "tópicos em modelagem de software",
            "tópicos em processos de software", "tópicos em projeto de software",
            "tópicos em qualidade de software", "tópicos em sistemas colaborativos",
            "tópicos em verificação, validação e testes de software", "administração de banco de dados",
            "banco de dados distribuídos", "banco de dados não convencionais",
            "projeto de aplicações com dados abertos", "recuperação de informação", "séries temporais",
            "descoberta de conhecimento em dados", "processamento e mineração de texto",
            "projetos de ciência de dados para o bem-estar social", "ambiente operacional unix",
            "automação", "ferramentas de modelagem e simulação para avaliação de desempenho",
            "gerenciamento de redes e serviços", "modelos de sistemas de computação e comunicação",
            "redes móveis e computação ubíqua", "segurança de tecnologia da informação",
            "serviços de rede e multimídia", "simulação estocástica", "sistemas distribuídos",
            "culturas afro-brasileiras em sala de aula", "educação ambiental e cidadania",
            "língua brasileira de sinais","atividades complementares e de extensão-1",
            "atividades complementares e de extensão-2","atividades complementares e de extensão-3",
            "atividades complementares e de extensão-4","atividades de extensão i",
            "atividades de extensão ii","projeto de graduação i","projeto de graduação ii"
        ]

        }

    gerar_relatorio(cursadas_apv, cursadas_adi, curriculo)
