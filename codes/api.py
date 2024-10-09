from fastapi import FastAPI, Path, HTTPException
from typing import Optional

app = FastAPI()

disciplinas = {
    0:{
        "codigo_disciplina": "TIN0222",
        "nome_disciplina": "Algoritmos e Programação",
        "ementa": "",
        "professor": "Jobson",
        "carga_horaria": 60,
        "periodo": 1,
    },
    1:{
        "codigo_disciplina": "TIN0235",
        "nome_disciplina": "Arquitetura de Computadores",
        "ementa": "",
        "professor": "Jefferson",
        "carga_horaria": 60,
        "periodo": 1,
    },
    2:{
        "codigo_disciplina": "TMT0043",
        "nome_disciplina": "Fundamentos de Cálculo",
        "ementa": "",
        "professor": "Amâncio",
        "carga_horaria": 60,
        "periodo": 1,
    },
    3:{
        "codigo_disciplina": "TIN0206",
        "nome_disciplina": "Fundamentos de Sistemas de Informação",
        "ementa": "",
        "professor": "Rodrigo",
        "carga_horaria": 60,
        "periodo": 1,
    },
    4:{
        "codigo_disciplina": "TIN0208",
        "nome_disciplina": "Interação Humano-Computador",
        "ementa": "",
        "professor": "Simone",
        "carga_horaria": 60,
        "periodo": 1,
    },
    5:{
        "codigo_disciplina": "TIN0207",
        "nome_disciplina": "Informação e Sociedade",
        "ementa": "",
        "professor": "Sean",
        "carga_horaria": 60,
        "periodo": 1,
    },
    6:{
        "codigo_disciplina": "TIN0207",
        "nome_disciplina": "Informação e Sociedade",
        "ementa": "",
        "professor": "Pimentel",
        "carga_horaria": 60,
        "periodo": 1,
    },
    7:{
        "codigo_disciplina": "TMT0044",
        "nome_disciplina": "Álgebra Linear",
        "ementa": "",
        "professor": "Jutuca",
        "carga_horaria": 60,
        "periodo": 2,
    },
}

@app.get("/")
def index():
    return {"codigo_disciplina": "TMQ0007"}

@app.get("/disciplinas/{id}")
def get_disciplina(id: int = Path(description="Entre com o ID da disciplina")):
    if id < len(disciplinas):
        return disciplinas[id]
    else:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")


@app.get("/get-disciplina-by-codigo")
def get_disciplina(*, codigo: str, professor: Optional[str] = None):
    lista_disciplinas = []

    for id in disciplinas:
        if disciplinas[id]['codigo_disciplina'] == codigo:
            if professor == None:
                lista_disciplinas.append(disciplinas[id])
            else:
                if professor == disciplinas[id]['professor']:
                    lista_disciplinas.append(disciplinas[id])

    if len(lista_disciplinas) > 0:
        return lista_disciplinas
    else:
        return {"Data": f"Não encontramos a disciplina do código {codigo}"}
        

@app.get("/list-disciplinas-by-periodo")
def list_disciplinas(periodo: int):
    
    lista_disciplinas = []

    for id in disciplinas:
        if disciplinas[id]["periodo"] == periodo:
            lista_disciplinas.append(disciplinas[id])

    if len(lista_disciplinas) > 0:
        return lista_disciplinas
    else:
        return {"Data": f"Não encontramos nenhuma disciplina do {periodo}° período"}


@app.get("/disciplinas")
def list_disciplinas():
    return disciplinas