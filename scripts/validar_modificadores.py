# -*- coding: utf-8 -*-
"""Valida data/modificadores.json (dosimetria — v1.2.0).

Regras (portão de CI da v1.2.0):
- `id` único e não vazio (append-only, é referência de permalink);
- `natureza` ∈ {judicial, atenuante, agravante, diminuicao, aumento, concurso};
- `fase` coerente com a natureza;
- frações em [0,1] e fracao_min <= fracao_max quando ambas presentes;
- `escopo.tipo` ∈ {geral, titulo, lei, tipos, tipos_por_artigo, combinador};
- se escopo referencia tipos do catálogo, os alvos existem em crimes.json.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parent.parent
NATUREZAS = {"judicial", "atenuante", "agravante", "diminuicao", "aumento", "concurso"}
FASE_DE = {"judicial": 1, "atenuante": 2, "agravante": 2,
           "diminuicao": 3, "aumento": 3, "concurso": "concurso"}
ESCOPOS = {"geral", "titulo", "lei", "tipos", "tipos_por_artigo", "combinador"}


def main() -> int:
    dados = json.loads((RAIZ / "data" / "modificadores.json").read_text(encoding="utf-8"))
    mods = dados["modificadores"]
    catalogo = json.loads((RAIZ / "data" / "crimes.json").read_text(encoding="utf-8"))
    leis_artigos = {(c["lei"], c["artigo"]) for c in catalogo}
    leis = {c["lei"] for c in catalogo}

    erros: list[str] = []
    vistos: set[str] = set()
    for m in mods:
        mid = m.get("id", "")
        rot = f"[{mid or '?'}]"
        if not mid:
            erros.append(f"{rot} sem id")
        elif mid in vistos:
            erros.append(f"{rot} id duplicado")
        vistos.add(mid)

        nat = m.get("natureza")
        if nat not in NATUREZAS:
            erros.append(f"{rot} natureza inválida: {nat!r}")
        elif m.get("fase") != FASE_DE[nat]:
            erros.append(f"{rot} fase {m.get('fase')!r} incoerente com natureza {nat!r} "
                         f"(esperada {FASE_DE[nat]!r})")

        for campo in ("fracao_min", "fracao_max"):
            v = m.get(campo)
            if v is not None and not (0 <= v <= 1):
                erros.append(f"{rot} {campo}={v} fora de [0,1]")
        fmn, fmx = m.get("fracao_min"), m.get("fracao_max")
        if fmn is not None and fmx is not None and fmn > fmx:
            erros.append(f"{rot} fracao_min {fmn} > fracao_max {fmx}")

        esc = m.get("escopo", {})
        tipo = esc.get("tipo")
        if tipo not in ESCOPOS:
            erros.append(f"{rot} escopo.tipo inválido: {tipo!r}")
        if tipo == "lei" and esc.get("valor") not in leis:
            erros.append(f"{rot} escopo lei {esc.get('valor')!r} não existe no catálogo")
        if tipo == "tipos_por_artigo":
            lei = esc.get("lei")
            for art in esc.get("artigos", []):
                # casa por prefixo (o artigo do modificador pode omitir ", caput")
                if not any(l == lei and a.startswith(art) for (l, a) in leis_artigos):
                    erros.append(f"{rot} alvo {lei} {art!r} não existe no catálogo")

    if erros:
        print(f"✗ {len(erros)} problema(s) em modificadores.json:")
        for e in erros:
            print("  " + e)
        return 1
    por_fase = {}
    for m in mods:
        por_fase[m["natureza"]] = por_fase.get(m["natureza"], 0) + 1
    print(f"✓ modificadores.json: {len(mods)} modificadores válidos — {por_fase}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
