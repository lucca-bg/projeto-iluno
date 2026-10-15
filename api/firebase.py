"""Acesso ao Firestore pela API, usando o Firebase Admin SDK.

A credencial vem da variável de ambiente FIREBASE_SERVICE_ACCOUNT
(JSON completo da conta de serviço), configurada na Vercel e no .env.local.
"""

import json
import os
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore


@lru_cache(maxsize=1)
def _db():
    if not firebase_admin._apps:
        conteudo = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
        if not conteudo:
            raise RuntimeError("Variável FIREBASE_SERVICE_ACCOUNT não configurada")
        firebase_admin.initialize_app(credentials.Certificate(json.loads(conteudo)))
    return firestore.client()


def listar_disciplinas() -> list[dict]:
    docs = _db().collection("disciplinas").stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]


def obter_disciplina(disciplina_id: str) -> dict | None:
    doc = _db().collection("disciplinas").document(disciplina_id).get()
    return {"id": doc.id, **doc.to_dict()} if doc.exists else None


def listar_topicos() -> list[dict]:
    docs = _db().collection("topicos_avaliacao").order_by("ordem").stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]
