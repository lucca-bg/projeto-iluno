"""Médias das avaliações por tópico, separadas do Firebase para poderem ser testadas."""


def calcular_medias(avaliacoes: list[dict], topicos: list[str]) -> dict:
    """Média aritmética das notas de cada tópico, arredondada em duas casas.

    `avaliacoes` são os documentos de disciplinas/{id}/avaliacoes ({"notas": {...}}).
    Notas ausentes ou fora de 1 a 5 são ignoradas; tópico sem notas fica com média None.
    """
    medias = {}
    for topico in topicos:
        notas = [
            n
            for a in avaliacoes
            if isinstance(n := (a.get("notas") or {}).get(topico), int)
            and not isinstance(n, bool)
            and 1 <= n <= 5
        ]
        medias[topico] = round(sum(notas) / len(notas), 2) if notas else None
    return {"total": len(avaliacoes), "medias": medias}
