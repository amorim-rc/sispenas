# -*- coding: utf-8 -*-
"""Gera docs/completude.md — o acompanhamento de completude do catálogo.

A página é DERIVADA de ``data/diplomas.json`` (denominador da Fase 1) e de
``data/crimes.json`` (o catálogo): índice de diplomas com contagens, lista
exaustiva dos tipos já reunidos por diploma e os diplomas ainda sem coleta.
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

# Diplomas cuja coleta foi CONFERIDA integralmente contra o texto compilado
# (todos os preceitos vigentes têm registro). Entra aqui só com conferência
# artigo a artigo documentada na release note correspondente.
CONFERIDOS: dict[str, str] = {
    "lcp": "v1.1.2",
    "lei9279": "v1.1.2",
}


def _num_artigo(artigo: str) -> tuple:
    m = re.search(r"(\d+)", artigo or "")
    return (int(m.group(1)) if m else 0, artigo)


def _slug(texto: str) -> str:
    """Slug de heading do Docusaurus (github-slugger): minúsculas, pontuação
    removida, cada espaço vira um hífen (sem colapsar — travessão entre
    espaços produz hífen duplo), acentos preservados."""
    s = texto.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return s.replace(" ", "-")


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
        if d["id"] in CONFERIDOS:
            return f"✅ completo (conferido na {CONFERIDOS[d['id']]})"
        if not tipos_por_slug.get(d["id"]):
            return "⛔ não iniciado"
        return "🔶 em coleta"

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
    p("| Diploma | Preceitos vigentes | Tipos coletados | Situação |")
    p("|---|---:|---:|---|")
    ordem = sorted(vigentes, key=lambda d: (-len(tipos_por_slug.get(d["id"], [])),
                                            -d["preceitos_esperados"]))
    for d in ordem:
        n = len(tipos_por_slug.get(d["id"], []))
        nome = f"[{d['nome']}](#{_slug(d['nome'])})" if n else d["nome"]
        p(f"| {nome} | {d['preceitos_esperados']} | {n} | {situacao(d)} |")
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

    # ------------------------------------------- lista exaustiva por diploma
    p("## Tipos reunidos, por diploma")
    p("")
    p("Lista exaustiva do que já está no catálogo. O `id` é a URL pública do tipo")
    p("(`/pesquisa/tipos?tipo=N`).")
    p("")
    for d in ordem:
        tipos = tipos_por_slug.get(d["id"])
        if not tipos:
            continue
        tipos = sorted(tipos, key=lambda r: (_num_artigo(r["artigo"]), r["id"]))
        p(f"### {d['nome']}")
        p("")
        p(f"*{d['norma']}* — {d['preceitos_esperados']} preceitos vigentes, "
          f"{len(tipos)} tipos coletados. {situacao(d)}")
        p("")
        p("| id | Dispositivo | Tipo penal |")
        p("|---:|---|---|")
        for r in tipos:
            crime = r["crime"].replace("|", "\\|")
            p(f"| [{r['id']}](/pesquisa/tipos?tipo={r['id']}) | {r['artigo']} | {crime} |")
        p("")

    destino = RAIZ / "docs" / "completude.md"
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
        fh.write("\n")
    print(f"escrito {destino} ({len(L)} linhas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
