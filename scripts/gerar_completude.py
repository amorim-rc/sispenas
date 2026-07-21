# -*- coding: utf-8 -*-
"""Gera docs/completude.md — o acompanhamento de completude do catálogo.

A página é DERIVADA de ``data/diplomas.json`` (denominador da Fase 1) e de
``data/crimes.json`` (o catálogo): índice de diplomas com o total de tipos
coletados e a situação de cada um, mais os diplomas ainda sem coleta.
Não edite ``docs/completude.md`` à mão — regenere com:

    python scripts/gerar_completude.py

Rode após qualquer mudança em ``data/crimes.json`` ou ``data/diplomas.json``.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Diplomas cuja coleta AINDA tem preceitos faltando (a conferência dispositivo
# a dispositivo, via scripts/diff_tipos.py, encontrou lacunas genuínas). Fora
# desta lista, um diploma com coleta é dado como "concluído" — no sentido de
# que a revisão não localizou preceito faltante, sempre passível de erro.
INCOMPLETOS: set[str] = {"cpm"}


def main() -> int:
    inventario = json.loads((RAIZ / "data" / "diplomas.json").read_text(encoding="utf-8"))
    catalogo = json.loads((RAIZ / "data" / "crimes.json").read_text(encoding="utf-8"))

    rotulo_para_slug: dict[str, str] = {}
    for d in inventario["diplomas"]:
        for rotulo in d.get("rotulos_catalogo", []):
            rotulo_para_slug[rotulo] = d["id"]

    tipos_por_slug: dict[str, list[dict]] = {}
    orfaos: dict[str, int] = {}
    for registro in catalogo:
        slug = rotulo_para_slug.get(registro["lei"])
        if slug is None:
            orfaos[registro["lei"]] = orfaos.get(registro["lei"], 0) + 1
        else:
            tipos_por_slug.setdefault(slug, []).append(registro)
    for rotulo, n in sorted(orfaos.items()):
        print(f"AVISO: rótulo sem diploma no inventário: {rotulo!r} ({n})", file=sys.stderr)

    vigentes = [d for d in inventario["diplomas"] if d["situacao"] == "vigente"]
    historicos = [d for d in inventario["diplomas"] if d["situacao"] != "vigente"]
    total_preceitos = inventario["_meta"]["total_preceitos_esperados"]
    com_coleta = [d for d in vigentes if tipos_por_slug.get(d["id"])]
    # Diploma sem tipos E sem preceitos vigentes não é lacuna — nada há a
    # coletar (ex.: Lei 9.807/99, cujo único crime foi vetado na origem).
    sem_coleta = [d for d in vigentes
                  if not tipos_por_slug.get(d["id"]) and d["preceitos_esperados"] > 0]

    def situacao(d: dict) -> str:
        if not tipos_por_slug.get(d["id"]):
            return "⛔ não iniciado"
        if d["id"] in INCOMPLETOS:
            return "🔶 em coleta"
        return "concluído ❓"

    L: list[str] = []
    p = L.append
    p("---")
    p("id: completude")
    p("title: Completude do catálogo")
    p("sidebar_position: 3")
    p("---")
    p("")
    p("{/* GERADO AUTOMATICAMENTE por scripts/gerar_completude.py — não edite à mão. */}")
    p("")
    p("# Completude do catálogo")
    p("")
    p(":::note[Página gerada]")
    p("Este acompanhamento é derivado de `data/diplomas.json` (o denominador, Fase 1 da")
    p("[Conferência integral](/docs/roadmap#conferência-integral-do-catálogo)) e de")
    p("`data/crimes.json` (o catálogo). Para atualizá-lo:")
    p("`python scripts/gerar_completude.py`.")
    p(":::")
    p("")
    p("| Indicador | Valor |")
    p("|---|---|")
    p(f"| Tipos penais catalogados | **{len(catalogo)}** |")
    p(f"| Preceitos secundários vigentes (denominador) | **{total_preceitos}** |")
    p(f"| Diplomas vigentes inventariados | {len(vigentes)} |")
    p(f"| — com coleta | {len(com_coleta)} |")
    p(f"| — sem nenhum registro | **{len(sem_coleta)}** |")
    p(f"| Diplomas revogados/não recepcionados registrados | {len(historicos)} |")
    p("")
    p("A unidade do denominador é o **preceito secundário** (cada cominação de pena no")
    p("texto compilado do Planalto). O catálogo desdobra incisos e condutas, então um")
    p("diploma pode ter mais tipos que preceitos sem estar errado — a comparação serve")
    p("para dimensionar lacunas, não como percentual exato.")
    p("")

    # ------------------------------------------------------------------ índice
    p("## Índice por diploma")
    p("")
    p(":::note[O que significa a situação]")
    p("**concluído ❓** — a conferência dispositivo a dispositivo não localizou "
      "nenhum preceito faltante após as revisões. Não é uma garantia: o "
      "denominador real (quantos tipos a lei comporta) não é conhecido com "
      "certeza, então este estado é **passível de erro** e pode voltar a "
      "\"em coleta\" se uma revisão futura encontrar algo. **em coleta** — há "
      "preceitos sabidamente faltando. **não iniciado** — nenhum tipo reunido "
      "ainda.")
    p(":::")
    p("")
    p("| Diploma | Tipos coletados | Situação |")
    p("|---|---:|---|")
    ordem = sorted(vigentes, key=lambda d: (-len(tipos_por_slug.get(d["id"], [])),
                                            -d["preceitos_esperados"]))
    for d in ordem:
        n = len(tipos_por_slug.get(d["id"], []))
        p(f"| {d['nome']} | {n} | {situacao(d)} |")
    p("")

    # ------------------------------------------------------- sem coleta ainda
    p("## Diplomas ainda sem coleta")
    p("")
    p("Diplomas com preceito penal em vigor dos quais **nenhum** tipo foi reunido —")
    p("o \"scraper\" de tipos ainda não passou por eles:")
    p("")
    p("| Diploma | Norma | Preceitos vigentes | Artigos penais |")
    p("|---|---|---:|---|")
    for d in sorted(sem_coleta, key=lambda d: -d["preceitos_esperados"]):
        p(f"| {d['nome']} | {d['norma']} | {d['preceitos_esperados']} | "
          f"{d.get('artigos_penais', '—')} |")
    p("")

    # ------------------------------------------------- acervo histórico (meta)
    p("## Diplomas revogados e não recepcionados")
    p("")
    p("Registrados no inventário para o **acervo histórico** —")
    p("[meta da v1.3.0](/docs/roadmap#v130--cobertura-completa-e-acervo-histórico), a ser")
    p("executada **após** a completude dos vigentes: reunir os tipos penais revogados,")
    p("alterados e não recepcionados, com o texto original, o que houve com cada um,")
    p("quando e por qual dispositivo.")
    p("")
    p("| Diploma | Norma | O que houve |")
    p("|---|---|---|")
    for d in historicos:
        rotulo = "não recepcionado" if d["situacao"] == "nao_recepcionado" else "revogado"
        p(f"| {d['nome']} | {d['norma']} | {rotulo} — {d['norma_revogadora']} |")
    p("")
    p("A lista completa dos tipos já reunidos, com o texto de cada um, está na "
      "[busca por tipo penal](/pesquisa/tipos).")
    p("")

    destino = RAIZ / "docs" / "completude.md"
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
        fh.write("\n")
    print(f"escrito {destino} ({len(L)} linhas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
