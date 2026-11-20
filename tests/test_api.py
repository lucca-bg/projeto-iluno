"""Testes da API (T05/T17). Não acessam o Firebase: as funções de dados são substituídas."""

from fastapi.testclient import TestClient

from api import index
from api.busca import filtrar_por_nome, normalizar
from api.medias import calcular_medias

DISCIPLINAS = [
    {"id": "calculo-i", "nome": "Cálculo I"},
    {"id": "banco-de-dados", "nome": "Banco de Dados"},
    {"id": "estruturas-de-dados", "nome": "Estruturas de Dados"},
]

TOPICOS = ["dificuldade", "carga_extraclasse", "aplicacao_pratica", "relevancia"]
AVALIACOES = [
    {"notas": {"dificuldade": 5, "carga_extraclasse": 4, "aplicacao_pratica": 2, "relevancia": 3}},
    {"notas": {"dificuldade": 4, "carga_extraclasse": 4, "aplicacao_pratica": 3, "relevancia": 5}},
    {"notas": {"dificuldade": 4, "carga_extraclasse": 3, "aplicacao_pratica": 3, "relevancia": 5}},
]


def test_normalizar_remove_acentos_e_maiusculas():
    assert normalizar("  Cálculo   I ") == "calculo i"


def test_filtrar_ignora_acentos():
    assert [d["id"] for d in filtrar_por_nome(DISCIPLINAS, "calculo")] == ["calculo-i"]


def test_filtrar_prioriza_quem_comeca_com_o_termo():
    ids = [d["id"] for d in filtrar_por_nome(DISCIPLINAS, "dados")]
    assert ids == ["banco-de-dados", "estruturas-de-dados"]
    ids = [d["id"] for d in filtrar_por_nome(DISCIPLINAS, "ban")]
    assert ids == ["banco-de-dados"]


def test_filtrar_termo_vazio_devolve_todas():
    assert len(filtrar_por_nome(DISCIPLINAS, "")) == 3


def _cliente(monkeypatch):
    monkeypatch.setattr(index.firebase, "listar_disciplinas", lambda: DISCIPLINAS)
    monkeypatch.setattr(
        index.firebase,
        "obter_disciplina",
        lambda i: next((d for d in DISCIPLINAS if d["id"] == i), None),
    )
    monkeypatch.setattr(
        index.firebase, "listar_topicos", lambda: [{"id": t} for t in TOPICOS]
    )
    monkeypatch.setattr(
        index.firebase, "listar_avaliacoes", lambda i: AVALIACOES if i == "calculo-i" else []
    )
    return TestClient(index.app)


def test_health():
    assert TestClient(index.app).get("/api/health").json() == {"status": "ok"}


def test_endpoint_busca(monkeypatch):
    r = _cliente(monkeypatch).get("/api/disciplinas", params={"nome": "estrut"})
    assert r.status_code == 200
    assert r.json()["total"] == 1


def test_endpoint_detalhe_404(monkeypatch):
    assert _cliente(monkeypatch).get("/api/disciplinas/nao-existe").status_code == 404


def test_calcular_medias():
    r = calcular_medias(AVALIACOES, TOPICOS)
    assert r["total"] == 3
    assert r["medias"] == {
        "dificuldade": 4.33,
        "carga_extraclasse": 3.67,
        "aplicacao_pratica": 2.67,
        "relevancia": 4.33,
    }


def test_calcular_medias_sem_avaliacoes():
    assert calcular_medias([], ["dificuldade"]) == {"total": 0, "medias": {"dificuldade": None}}


def test_calcular_medias_ignora_notas_invalidas():
    avaliacoes = [{"notas": {"dificuldade": 2}}, {"notas": {"dificuldade": 9}}, {"notas": {}}]
    assert calcular_medias(avaliacoes, ["dificuldade"])["medias"] == {"dificuldade": 2.0}


def test_endpoint_medias(monkeypatch):
    r = _cliente(monkeypatch).get("/api/disciplinas/calculo-i/medias")
    assert r.status_code == 200
    assert r.json()["total"] == 3
    assert r.json()["medias"]["dificuldade"] == 4.33


def test_endpoint_medias_404(monkeypatch):
    assert _cliente(monkeypatch).get("/api/disciplinas/nao-existe/medias").status_code == 404
