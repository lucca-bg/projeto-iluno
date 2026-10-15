"""Regras de busca de disciplinas (T05), separadas do Firebase para poderem ser testadas."""

import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas e sem acentos: 'Cálculo I' -> 'calculo i'."""
    sem_acentos = unicodedata.normalize("NFKD", texto or "")
    sem_acentos = "".join(c for c in sem_acentos if not unicodedata.combining(c))
    return " ".join(sem_acentos.lower().split())


def filtrar_por_nome(disciplinas: list[dict], termo: str) -> list[dict]:
    """Retorna as disciplinas cujo nome contém o termo, em ordem alfabética.

    Termo vazio devolve todas. Disciplinas cujo nome começa com o termo vêm primeiro.
    O Firestore não tem busca por trecho de texto; com o volume do MVP
    (algumas centenas de disciplinas) filtrar na API é suficiente.
    """
    alvo = normalizar(termo)
    encontradas = [d for d in disciplinas if alvo in normalizar(d.get("nome", ""))]
    return sorted(
        encontradas,
        key=lambda d: (
            not normalizar(d.get("nome", "")).startswith(alvo),
            normalizar(d.get("nome", "")),
        ),
    )
