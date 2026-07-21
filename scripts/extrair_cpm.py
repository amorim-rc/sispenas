# -*- coding: utf-8 -*-
"""Extrator estruturado do Código Penal Militar (DL 1.001/69) para a cobertura.

Para cada preceito ('Pena') vigente, captura: artigo, dispositivo (§), nomen
juris (o título em destaque que antecede o artigo, como no CP), a conduta e a
pena já convertida para meses + tipo_pena. Produz registros prontos para
revisão — a conferência humana ajusta nome, elemento e ação penal.

Uso: python scripts/extrair_cpm.py --cache DIR --frente paz|guerra
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

# "Art  . 190" (espaços antes do ponto) ocorre no compilado do CPM.
RE_ART = re.compile(r"^\s*Art\s*\.?\s*(\d+)")
# § seguido do número e, opcionalmente, de sufixo letrado "-A" (o CPM usa
# "§ 2º-A" para os parágrafos inseridos por leis posteriores).
RE_PAR = re.compile(r"^\s*§\s*(\d+)\s*[ºo°]?\s*(-[A-Z])?")
RE_PAR_UNICO = re.compile(r"^\s*Par[áa]grafo\s+[úu]nico", re.IGNORECASE)
RE_INC = re.compile(r"^\s*([IVXLC]+)\s*[-–]\s")
RE_ALINEA = re.compile(r"^\s*([a-z])\)\s")
UNID = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
        "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9}
DEZ = {"dez": 10, "onze": 11, "doze": 12, "treze": 13, "catorze": 14,
       "quatorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17,
       "dezoito": 18, "dezenove": 19, "vinte": 20, "trinta": 30}


def _num(tok: str) -> int | None:
    """Número por extenso ou dígito, inclusive composto ('vinte e quatro')."""
    tok = tok.strip().lower()
    if tok.isdigit():
        return int(tok)
    if tok in DEZ:
        return DEZ[tok]
    if tok in UNID:
        return UNID[tok]
    m = re.match(r"(vinte|trinta)\s+e\s+(\w+)$", tok)
    if m and m.group(2) in UNID:
        return DEZ[m.group(1)] + UNID[m.group(2)]
    return None


_TP = [("reclus", "Reclusão"), ("detenç", "Detenção"), ("prisão", "Prisão"),
       ("impedimento", "Impedimento"), ("suspensão", "Suspensão do exercício"),
       ("reforma", "Reforma"), ("morte", "Morte")]
_N = r"(\d+|vinte\s+e\s+\w+|trinta\s+e\s+\w+|\w+)"


def parse_pena(linha: str):
    """(pena_min_meses, pena_max_meses, tipo_pena) a partir da linha de Pena.

    Trata unidades mistas ('seis meses a dois anos') e números compostos.
    """
    tp = next((rot for chave, rot in _TP if chave in linha.lower()), None)
    # Remove parentéticos: "(um)", "(dois)", "(Redação dada pela Lei...)" —
    # o dígito antes deles é o número que importa.
    linha = re.sub(r"\s*\([^)]*\)", " ", linha)
    mn = mx = None
    # Pena de morte em tempo de guerra (art. 56 CPM): "morte, grau máximo;
    # reclusão, de N anos, grau mínimo". Representa como reclusão do mínimo
    # cominado ao teto (30 anos), com a morte anotada no obs pela geração.
    morte = re.search(r"morte,\s*grau\s+m[áa]ximo.*?reclus[ãa]o,?\s*de\s+" + _N
                      + r"\s*anos?,?\s*grau\s+m[íi]nimo", linha, re.I)
    if morte:
        n = _num(morte.group(1))
        if n is not None:
            return n * 12, 360, "Reclusão (morte no grau máximo)"
    # "de <A> [unidadeA] a <B> <unidadeB>"  — unidadeA opcional (herda de B)
    faixa = re.search(
        _N + r"\s*(anos?|mes(?:es)?)?\s+a\s+" + _N + r"\s*(anos?|mes(?:es)?)",
        linha, re.I)
    ate = re.search(r"at[ée]\s+" + _N + r"\s*(anos?|mes(?:es)?)", linha, re.I)
    if faixa:
        a, ua, b, ub = faixa.groups()
        na, nb = _num(a), _num(b)
        fb = 12 if ub.lower().startswith("ano") else 1
        fa = (12 if ua.lower().startswith("ano") else 1) if ua else fb
        if na is not None and nb is not None:
            mn, mx = na * fa, nb * fb
    elif ate:
        b, ub = ate.groups()
        nb = _num(b)
        if nb is not None:
            mn, mx = 0, nb * (12 if ub.lower().startswith("ano") else 1)
    return mn, mx, tp


def _clausula(linha: str) -> str:
    """Texto definidor de um dispositivo, limpo: sem 'Art. N.'/'§N'/inciso no
    início, sem parentéticos de redação, cortado antes do ':' que abre a pena."""
    t = re.sub(r"^\s*Art\s*\.?\s*\d+[ºo°.\-\s]*", "", linha)
    t = re.sub(r"^\s*§\s*\d+\s*[ºo°]?\s*(?:-[A-Z])?\s*\.?\s*", "", t)
    t = re.sub(r"^\s*Par[áa]grafo\s+[úu]nico[.\-\s]*", "", t)
    t = re.sub(r"^\s*[IVXLC]+\s*[-–]\s*", "", t)
    t = re.sub(r"^\s*[a-z]\)\s*", "", t)
    t = re.sub(r"\s*\([^)]*\)", "", t)          # (Redação...), (um)
    t = re.split(r"\bPena\b", t)[0]
    t = t.rstrip(" :;.-–—")
    return re.sub(r"\s+", " ", t).strip()


def extrair(cache: Path, lo: int, hi: int):
    texto = inv._texto_vigente(inv._decodificar((cache / "cpm.html").read_bytes()))
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    art = None
    disp = "caput"
    nomen = None
    caput_desc = ""
    disp_desc = ""
    inciso = None
    inc_desc = ""
    emitidos: set[str] = set()
    registros = []
    for i, l in enumerate(linhas):
        m = RE_ART.match(l)
        if m:
            art = int(m.group(1))
            disp = "caput"
            caput_desc = _clausula(l)
            disp_desc = caput_desc
            inciso = None
            emitidos = set()
            prev = linhas[i - 1] if i else ""
            if (prev and len(prev) < 60 and not RE_ART.match(prev)
                    and not prev.startswith("§") and "Pena" not in prev
                    and not re.match(r"^[IVXLC]+\s*[-–]", prev)
                    and not prev.isupper()):
                nomen = prev
            else:
                nomen = None
        if RE_PAR_UNICO.match(l):
            disp = "par. único"; disp_desc = _clausula(l); inciso = None
        elif (mp := RE_PAR.match(l)):
            disp = f"§{mp.group(1)}" + (mp.group(2) or "")
            disp_desc = _clausula(l); inciso = None
        elif (mi := RE_INC.match(l)):
            inciso = mi.group(1)
            inc_desc = _clausula(l)
        elif (ma := RE_ALINEA.match(l)):
            inciso = f"{ma.group(1)})"
            inc_desc = _clausula(l)
        if art and lo <= art <= hi and inv.RE_PENA.search(l):
            mn, mx, tp = parse_pena(l)
            desc = disp_desc if disp != "caput" else caput_desc
            usar_disp = disp
            usar_desc = desc
            # Colisão: segundo preceito no mesmo dispositivo = inciso com pena
            # própria (ex.: art. 191, I e II). Desambigua pelo inciso.
            if disp in emitidos and inciso:
                usar_disp = f"{disp}, {inciso}" if disp != "caput" else inciso
                usar_desc = inc_desc or desc
            emitidos.add(disp)
            if not usar_desc:
                usar_desc = caput_desc
            registros.append({
                "art": art, "disp": usar_disp, "nomen": nomen,
                "desc": usar_desc[:120], "conduta": linhas[i - 1][:90] if i else "",
                "pena": l[:80], "pena_min": mn, "pena_max": mx, "tipo_pena": tp,
            })
    return registros


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--frente", choices=["paz", "guerra"], required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lo, hi = (136, 354) if args.frente == "paz" else (355, 410)
    regs = extrair(args.cache, lo, hi)
    if args.json:
        print(json.dumps(regs, ensure_ascii=False, indent=1))
        return 0
    for r in regs:
        loc = f"Art. {r['art']}" + (f", {r['disp']}" if r['disp'] != "caput" else "")
        pen = f"{r['pena_min']}-{r['pena_max']} {r['tipo_pena']}" if r['pena_min'] is not None else f"?? {r['pena']}"
        print(f"{loc:20s} | {(r['nomen'] or '—')[:34]:34s} | {pen}")
    print(f"\n{len(regs)} preceitos na frente '{args.frente}' ({lo}-{hi})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
