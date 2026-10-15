"""Testes da API (T05/T17). Não acessam o Firebase: as funções de dados são substituídas."""

from fastapi.testclient import TestClient

from api import index
from api.busca import filtrar_por_nome, normalizar

DISCIPLINAS = [
    {"id": "calculo-i", "nome": "Cálculo I"},
    {"id": "banco-de-dados", "nome": "Banco de Dados"},
    {"id": "estruturas-de-dados", "nome": "Estruturas de Dados"},
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
    return TestClient(index.app)


def test_health():
    assert TestClient(index.app).get("/api/health").json() == {"status": "ok"}


def test_endpoint_busca(monkeypatch):
    r = _cliente(monkeypatch).get("/api/disciplinas", params={"nome": "estrut"})
    assert r.status_code == 200
    assert r.json()["total"] == 1


def test_endpoint_detalhe_404(monkeypatch):
    assert _cliente(monkeypatch).get("/api/disciplinas/nao-existe").status_code == 404
