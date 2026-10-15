"""API do iLuno (FastAPI) — publicada como função Python na Vercel.

T17 — inicialização da API e rota de saúde.
T05 — busca de disciplina por nome.
Também expõe o detalhe da disciplina e os tópicos de avaliação, usados pela tela do T07.

Execução local:
    uvicorn api.index:app --reload --port 8000
"""

import os
import sys

# Garante que "api" seja importável tanto localmente quanto na Vercel.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query  # noqa: E402

from api.busca import filtrar_por_nome
from api import firebase

app = FastAPI(title="iLuno API", version="0.1.0")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/disciplinas")
def buscar_disciplinas(
    nome: str = Query("", max_length=80, description="Trecho do nome da disciplina"),
    limite: int = Query(20, ge=1, le=50),
):
    """T05 — busca disciplinas cujo nome contém o termo (ignora acentos e maiúsculas)."""
    disciplinas = firebase.listar_disciplinas()
    resultado = filtrar_por_nome(disciplinas, nome)
    return {"total": len(resultado), "disciplinas": resultado[:limite]}


@app.get("/api/disciplinas/{disciplina_id}")
def detalhar_disciplina(disciplina_id: str):
    disciplina = firebase.obter_disciplina(disciplina_id)
    if disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina


@app.get("/api/topicos")
def listar_topicos():
    return {"topicos": firebase.listar_topicos()}
