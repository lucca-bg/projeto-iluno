"""Carga inicial do Firestore (T04 e T06).

Cria os tópicos de avaliação e algumas disciplinas de teste, para que a busca (F02)
e a avaliação (F03) funcionem na demonstração da Onda 1 — o cadastro completo de
disciplinas (F08) é da Onda 2.

Uso (na raiz do repositório, com o venv ativo):
    python scripts/carga_inicial.py caminho/para/serviceAccountKey.json

Pode ser executado mais de uma vez: os documentos são sobrescritos, não duplicados.
"""

import sys

import firebase_admin
from firebase_admin import credentials, firestore

# T06 — tópicos fixos. Os IDs precisam bater com os de firestore.rules.
TOPICOS = [
    {
        "id": "dificuldade",
        "titulo": "Dificuldade",
        "descricao": "Quão difícil foi acompanhar o conteúdo (1 = muito fácil, 5 = muito difícil)",
        "ordem": 1,
    },
    {
        "id": "carga_extraclasse",
        "titulo": "Carga extraclasse",
        "descricao": "Tempo exigido fora da aula (1 = quase nenhum, 5 = muito tempo)",
        "ordem": 2,
    },
    {
        "id": "aplicacao_pratica",
        "titulo": "Aplicação prática",
        "descricao": "Quanto o conteúdo envolve atividades práticas (1 = só teoria, 5 = muito prática)",
        "ordem": 3,
    },
    {
        "id": "relevancia",
        "titulo": "Relevância para o curso",
        "descricao": "Quanto a disciplina contribuiu para a formação (1 = pouco, 5 = muito)",
        "ordem": 4,
    },
]

# T04 — modelo de disciplina + dados de teste.
DISCIPLINAS = [
    {
        "id": "algoritmos-e-programacao",
        "nome": "Algoritmos e Programação",
        "codigo": "TESTE-001",
        "curso": "Ciência da Computação",
        "cargaHoraria": 60,
        "modalidade": "Presencial",
        "ementa": "Lógica de programação, estruturas de controle, vetores e funções.",
    },
    {
        "id": "estruturas-de-dados",
        "nome": "Estruturas de Dados",
        "codigo": "TESTE-002",
        "curso": "Ciência da Computação",
        "cargaHoraria": 60,
        "modalidade": "Presencial",
        "ementa": "Listas, pilhas, filas, árvores e análise de complexidade.",
    },
    {
        "id": "banco-de-dados",
        "nome": "Banco de Dados",
        "codigo": "TESTE-003",
        "curso": "Ciência da Computação",
        "cargaHoraria": 60,
        "modalidade": "Híbrida",
        "ementa": "Modelagem relacional, SQL e normalização.",
    },
    {
        "id": "calculo-i",
        "nome": "Cálculo I",
        "codigo": "TESTE-004",
        "curso": "Engenharia de Software",
        "cargaHoraria": 60,
        "modalidade": "Presencial",
        "ementa": "Limites, derivadas e aplicações.",
    },
    {
        "id": "sistemas-distribuidos",
        "nome": "Sistemas Distribuídos",
        "codigo": "TESTE-005",
        "curso": "Ciência da Computação",
        "cargaHoraria": 60,
        "modalidade": "Presencial",
        "ementa": "Comunicação entre processos, sockets, consistência e tolerância a falhas.",
    },
]


def main(caminho_credencial: str) -> None:
    firebase_admin.initialize_app(credentials.Certificate(caminho_credencial))
    db = firestore.client()

    for t in TOPICOS:
        dados = {k: v for k, v in t.items() if k != "id"}
        db.collection("topicos_avaliacao").document(t["id"]).set(dados)
    print(f"{len(TOPICOS)} tópicos gravados")

    for d in DISCIPLINAS:
        dados = {k: v for k, v in d.items() if k != "id"}
        db.collection("disciplinas").document(d["id"]).set(dados)
    print(f"{len(DISCIPLINAS)} disciplinas gravadas")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python scripts/carga_inicial.py caminho/para/serviceAccountKey.json")
    main(sys.argv[1])
