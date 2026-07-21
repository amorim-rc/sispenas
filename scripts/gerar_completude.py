# -*- coding: utf-8 -*-
"""Gera docs/completude.md e docs/acervo-historico.md.

Ambas são DERIVADAS de ``data/diplomas.json`` (denominador da Fase 1) e de
``data/crimes.json`` (o catálogo). ``completude.md`` traz o índice de diplomas
vigentes com o total de tipos coletados e a situação de cada um;
``acervo-historico.md`` lista os diplomas revogados/não recepcionados e a meta
do acervo (v1.3.0). Não edite os ``.md`` à mão — regenere com:

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

# Dispositivos históricos identificados na conferência, a catalogar no acervo
# (v1.3.0): (dispositivo, categoria, o que houve). Categoria ∈ revogado |
# alterado | não recepcionado | vetado.
ACERVO_CASOS: list[tuple[str, str, str]] = [
    ("Lei 9.807/99, art. 19 (revelação de identidade de testemunha protegida)",
     "vetado",
     "Vetado na sanção da lei; nunca vigorou. O catálogo chegou a ter um "
     "registro indevido (id 1038), removido na v1.1.2."),
    ("CP, art. 240 (adultério)", "revogado", "Revogado pela Lei 11.106/2005."),
    ("CP, art. 217 (sedução)", "revogado", "Revogado pela Lei 12.015/2009."),
    ("CP, arts. 219 a 222 (rapto)", "revogado", "Revogados pela Lei 12.015/2009."),
    ("ECA, art. 233 (tortura de criança)", "revogado",
     "Revogado pela Lei 9.455/1997 (Lei de Tortura)."),
    ("LCP, arts. 60 e 61 (mendicância e importunação ofensiva)", "revogado",
     "Revogados pelas Leis 11.983/2009 e 13.718/2018."),
]


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
    # O índice só lista diplomas que TÊM tipo penal a coletar. Diploma vigente
    # sem preceito algum (ex.: Lei 9.807/99, cujo único crime foi vetado na
    # sanção) não é lacuna — não entra, para não aparecer como "não iniciado".
    indice = [d for d in vigentes
              if d["preceitos_esperados"] > 0 or tipos_por_slug.get(d["id"])]
    com_coleta = [d for d in indice if tipos_por_slug.get(d["id"])]

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
    p("sidebar_position: 2")
    p("---")
    p("")
    p("{/* GERADO AUTOMATICAMENTE por scripts/gerar_completude.py — não edite à mão. */}")
    p("")
    p("# Completude do catálogo")
    p("")
    p(":::note[Página gerada]")
    p("Este acompanhamento é derivado de `data/diplomas.json` (o denominador da")
    p("conferência do catálogo) e de")
    p("`data/crimes.json` (o catálogo). Para atualizá-lo:")
    p("`python scripts/gerar_completude.py`.")
    p(":::")
    p("")
    p("| Indicador | Valor |")
    p("|---|---|")
    p(f"| Tipos penais catalogados | **{len(catalogo)}** |")
    p(f"| Diplomas com tipo penal vigente | {len(indice)} |")
    p(f"| — com coleta iniciada | {len(com_coleta)} |")
    p(f"| Diplomas revogados/não recepcionados | [{len(historicos)}](/docs/acervo-historico) |")
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
    ordem = sorted(indice, key=lambda d: (-len(tipos_por_slug.get(d["id"], [])),
                                          -d["preceitos_esperados"]))
    for d in ordem:
        n = len(tipos_por_slug.get(d["id"], []))
        p(f"| {d['nome']} | {n} | {situacao(d)} |")
    p("")
    p("A lista completa dos tipos já reunidos, com o texto de cada um, está na "
      "[busca por tipo penal](/pesquisa/tipos).")
    p("")

    destino = RAIZ / "docs" / "completude.md"
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
        fh.write("\n")
    print(f"escrito {destino} ({len(L)} linhas)")

    _gerar_acervo(historicos)
    return 0


def _gerar_acervo(historicos: list[dict]) -> None:
    """docs/acervo-historico.md — os diplomas revogados/não recepcionados já
    inventariados, e a meta da v1.3.0 (reunir os tipos históricos)."""
    L: list[str] = []
    p = L.append
    p("---")
    p("id: acervo-historico")
    p("title: Acervo histórico")
    p("sidebar_position: 3")
    p("---")
    p("")
    p("{/* GERADO AUTOMATICAMENTE por scripts/gerar_completude.py — não edite à mão. */}")
    p("")
    p("# Acervo histórico")
    p("")
    p("Reunir **o que já foi crime no Brasil** — os tipos penais revogados, "
      "alterados e não recepcionados — é a "
      "[meta da v1.4.0](/docs/roadmap#v140--cobertura-completa-e-acervo-histórico), "
      "a ser executada **após** a completude dos tipos vigentes. A pergunta \"o "
      "que deixou de ser crime, e quando?\" é tão relevante para a pesquisa "
      "quanto \"o que é crime hoje\", e hoje nenhuma ferramenta a responde de "
      "forma estruturada.")
    p("")
    p("A entrega será uma aba de pesquisa própria, separada da busca vigente para "
      "que nenhum tipo revogado contamine estatística de direito vigente, com "
      "uma tela por tipo mostrando o **texto original**, o que houve com ele "
      "(alteração, revogação ou não recepção), **quando** e por **qual "
      "dispositivo**.")
    p("")
    p("## Diplomas revogados e não recepcionados já inventariados")
    p("")
    p("Ponto de partida do acervo: os diplomas inteiros que saíram de vigência, "
      "registrados na [Fase 1](/docs/completude). Faltam ainda os tipos "
      "**revogados dentro de diplomas vigentes** (ex.: adultério, sedução, rapto "
      "no CP) e as **redações anteriores** alteradas.")
    p("")
    p("| Diploma | Norma | O que houve |")
    p("|---|---|---|")
    for d in historicos:
        rotulo = "não recepcionado" if d["situacao"] == "nao_recepcionado" else "revogado"
        p(f"| {d['nome']} | {d['norma']} | {rotulo} — {d['norma_revogadora']} |")
    p("")
    p("## Casos já identificados para o acervo")
    p("")
    p("Dispositivos que saíram de vigência, foram alterados ou nunca vigoraram, "
      "encontrados durante a conferência do catálogo. São a semente do acervo — "
      "cada um receberá, na v1.3.0, uma entrada com o texto original e o histórico.")
    p("")
    p("| Dispositivo | Categoria | O que houve |")
    p("|---|---|---|")
    for disp, cat, hist in ACERVO_CASOS:
        p(f"| {disp} | {cat} | {hist} |")
    p("")
    destino = RAIZ / "docs" / "acervo-historico.md"
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
        fh.write("\n")
    print(f"escrito {destino} ({len(L)} linhas)")


if __name__ == "__main__":
    raise SystemExit(main())
