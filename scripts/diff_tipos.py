# -*- coding: utf-8 -*-
"""Diff em nível de TIPO (não de artigo) entre o texto compilado e o catálogo.

Para um diploma, lista cada preceito secundário ('Pena —') com o contexto do
dispositivo que o rege (caput / §N / inciso), permitindo ver quais figuras
autônomas — qualificadas, privilegiadas, equiparadas — ainda não foram
desmembradas em registro próprio no catálogo. Complementa o denominador em
nível de artigo do inventario_diplomas.py.

Uso:
    python scripts/diff_tipos.py SLUG --cache DIR

Não escreve nada: é ferramenta de leitura para a conferência dispositivo a
dispositivo (Fase 2 do roadmap).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("inv", RAIZ / "scripts" / "inventario_diplomas.py")
inv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inv)

# Marcadores de dispositivo dentro de um artigo.
RE_ART = re.compile(r"^\s*Art\s*\.?\s*(\d+)")
RE_PAR = re.compile(r"^\s*§\s*(\d+)\s*(?:[ºo°]|\-[A-Z])?", re.IGNORECASE)
RE_PAR_UNICO = re.compile(r"^\s*Par[áa]grafo\s+[úu]nico", re.IGNORECASE)
RE_INC = re.compile(r"^\s*([IVXLC]+)\s*[-–—]\s")


def contexto(slug: str, cache: Path) -> list[dict]:
    meta = inv.META[slug]
    faixas = meta["faixas"]
    texto = inv._texto_vigente(inv._decodificar((cache / f"{slug}.html").read_bytes()))
    art = None
    disp = "caput"
    inciso = None
    saida: list[dict] = []
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    for i, l in enumerate(linhas):
        m = RE_ART.match(l)
        if m:
            art = int(m.group(1))
            disp = "caput"
            inciso = None
        if RE_PAR_UNICO.match(l):
            disp = "par. único"; inciso = None
        elif (mp := RE_PAR.match(l)):
            disp = f"§{mp.group(1)}"; inciso = None
        if (mi := RE_INC.match(l)):
            inciso = mi.group(1)
        if art and inv._nas_faixas(art, faixas) and len(inv.RE_PENA.findall(l)):
            desc = linhas[i - 1][:70] if i else ""
            saida.append({"art": art, "disp": disp, "inciso": inciso,
                          "pena": l[:75], "antes": desc})
    return saida


def _chave(art: int, disp: str, inciso: str | None) -> str:
    """Chave canônica de dispositivo, tolerante à grafia (§1º vs §1, incisos)."""
    k = f"{art}"
    if disp and disp != "caput":
        k += "|" + disp.replace(" ", "").replace("º", "").replace("°", "").lower()
    if inciso:
        k += "|" + inciso.upper()
    return k


def _chave_registro(artigo: str) -> str:
    m = RE_ART.match(artigo) or re.match(r"\s*Art\.?\s*(\d+)", artigo)
    art = int(m.group(1)) if m else 0
    resto = artigo
    disp = "caput"
    inciso = None
    mp = re.search(r"§\s*(\d+)", artigo)
    if mp:
        disp = f"§{mp.group(1)}"
    if re.search(r"par[áa]grafo\s+[úu]nico", artigo, re.IGNORECASE):
        disp = "par.único"
    mi = re.search(r",\s*([IVXLC]+)\b", artigo)
    if mi:
        inciso = mi.group(1)
    return _chave(art, disp, inciso)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--full", action="store_true", help="mostra tudo, não só o não casado")
    args = ap.parse_args()

    catalogo = json.loads((RAIZ / "data" / "crimes.json").read_text(encoding="utf-8"))
    rotulos = set(inv.META[args.slug].get("rotulos", []))
    no_cat = [r for r in catalogo if r["lei"] in rotulos]
    chaves_cat = {}
    for r in no_cat:
        chaves_cat.setdefault(_chave_registro(r["artigo"]), []).append(r)

    ctx = contexto(args.slug, args.cache)
    faltam = []
    for c in ctx:
        k = _chave(c["art"], c["disp"], c["inciso"])
        # casa por dispositivo exato ou, na falta, pelo caput do artigo
        if k in chaves_cat or str(c["art"]) in chaves_cat:
            if args.full:
                print(f"  OK   art {c['art']} {c['disp']} {c['inciso'] or ''}")
        else:
            faltam.append(c)

    print(f"# {args.slug}: {len(no_cat)} registros | {len(ctx)} preceitos no texto "
          f"| {len(faltam)} preceitos SEM registro casado\n")
    for c in faltam:
        loc = f"Art. {c['art']}" + (f", {c['disp']}" if c['disp'] != "caput" else "")
        if c["inciso"]:
            loc += f", {c['inciso']}"
        print(f"  FALTA  {loc:22s} | {c['antes'][:56]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
