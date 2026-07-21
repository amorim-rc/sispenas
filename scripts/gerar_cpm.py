# -*- coding: utf-8 -*-
"""Gera/reconcilia os registros do CPM a partir da extração conferida.

Os 69 registros de CPM herdados estão sistematicamente errados (penas e nomes
trocados — verificado contra o texto compilado). Este script reconcilia por
dispositivo (art + §): onde já existe registro para o dispositivo, CORRIGE em
lugar (mantém o id/URL, C3); onde falta, ADICIONA com id novo. O texto oficial
é a fonte — nome vem do nomen juris, pena da extração.

Uso:
    python scripts/gerar_cpm.py --entrada cpm_paz.json [--aplicar]

Sem --aplicar, só relata. Com --aplicar, reescreve data/crimes.json.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parent.parent
LEI = "CPM (DL 1.001/69)"

# Penas cominadas por remissão (não parseáveis): conferidas à mão.
REMISSAO = {
    "315": (24, 72, "Reclusão", "Uso de documento falso: pena a cominada à "
            "falsificação ou à alteração (arts. 311-313; reclusão de 2 a 6 anos)"),
    "391": (9, 36, "Detenção", "Deserção especial em tempo de guerra: pena a "
            "cominada à deserção (art. 187) com aumento de metade"),
    "404": (0, 144, "Reclusão", "Furto em tempo de guerra: reclusão no dobro da "
            "cominada para o furto em tempo de paz (art. 240, até 6 anos)"),
    "405": (240, 360, "Reclusão (morte no grau máximo)", "Pena: morte no grau "
            "máximo se cominada reclusão de 30 anos; reclusão no grau mínimo "
            "(roubo/extorsão em tempo de guerra)"),
}


def _chave_txt(art, disp):
    k = str(art)
    if disp and disp != "caput":
        k += "|" + disp.replace(" ", "").replace(".", "").replace("º", "").replace("§", "p").lower().replace("parúnico", "pu")
    return k


def _chave_reg(artigo):
    m = re.match(r"Art\.?\s*(\d+)", artigo)
    k = m.group(1) if m else "?"
    mp = re.search(r"§\s*(\d+)", artigo)
    if mp:
        k += "|p" + mp.group(1)
    elif re.search(r"nico", artigo):
        k += "|pu"
    return k


def _label_faixa(mn, mx):
    """Faixa legível para o transformador ler o rótulo (C7)."""
    if mn is None or mx is None:
        return ""
    def u(m):
        return (f"{m // 12} anos" if m % 12 == 0 and m >= 12
                else (f"{m} meses" if m else "0"))
    if mn == 0:
        return f"até {u(mx)}"
    if mn % 12 == 0 and mx % 12 == 0:
        return f"{mn // 12}-{mx // 12} anos"
    return f"{mn}-{mx} meses"


def _artigo(art, disp):
    if disp == "caput":
        return f"Art. {art}, caput"
    if disp == "par. único":
        return f"Art. {art}, par. único"
    # disp: "§2", "§2-A", "I" (inciso), ou "§2, I" (inciso dentro de §)
    def fmt(seg):
        mm = re.match(r"§(\d+)(-[A-Z])?$", seg)
        return f"§{mm.group(1)}º{mm.group(2) or ''}" if mm else seg
    partes = [fmt(s.strip()) for s in disp.split(",")]
    return f"Art. {art}, " + ", ".join(partes)


def _nome(r):
    # nomen juris = nome oficial do crime militar; normaliza typo de OCR.
    nomen = re.sub(r"\s{2,}", " ", (r["nomen"] or "").strip())
    nomen = nomen.replace("I njúria", "Injúria").replace("Seqüestro", "Sequestro")
    desc = (r.get("desc") or "").strip()
    if r["disp"] == "caput":
        # nome = nomen juris; a descrição fica no obs, não no nome
        return (nomen or desc)[:150]
    # § / par. único: nomen juris do artigo + a cláusula própria da variante
    if nomen and desc:
        return f"{nomen} — {desc}"[:150]
    return (desc or nomen)[:150]


def _tipo(r):
    tp = r["tipo_pena"]
    return tp if tp else "—"


def _elemento(r):
    txt = (r["conduta"] + " " + r.get("desc", "") + " " + r["pena"]).lower()
    if re.search(r"culpa|culposa|culposamente", txt):
        return "Culposo"
    return "Doloso"


def _texto(r):
    return f"{r.get('nomen','')} {r.get('desc','')} {r.get('conduta','')}".lower()


def _violencia(r):
    t = _texto(r)
    return "Sim" if re.search(
        r"violência|violenta|homicídio|lesão corporal|les[ãa]o|"
        r"roubo|estupro|agress|vias de fato|constrang|maus[ -]?tratos|"
        r"tortura|espancar|matar", t) else "Não"


def _grave_ameaca(r):
    t = _texto(r)
    return "Sim" if re.search(
        r"amea[çc]a|grave amea|constrang|extors|coa[çc]|"
        r"violência ou grave|mediante violência", t) else "Não"


def construir(entrada: Path):
    ext = json.loads(entrada.read_text(encoding="utf-8"))
    d = json.loads((RAIZ / "data" / "crimes.json").read_text(encoding="utf-8"))
    existentes = {}
    for r in d:
        if r["lei"] == LEI:
            existentes.setdefault(_chave_reg(r["artigo"]), r)
    max_id = max(r["id"] for r in d)

    corrigidos, novos = [], []
    for r in ext:
        chave = _chave_txt(r["art"], r["disp"])
        mn, mx, tp = r["pena_min"], r["pena_max"], _tipo(r)
        obs_extra = ""
        if str(r["art"]) in REMISSAO and r["disp"] == "caput":
            mn, mx, tp, obs_extra = REMISSAO[str(r["art"])]
        desc = (r.get("desc") or "").strip()
        faixa = _label_faixa(mn, mx)
        if obs_extra:
            obs = obs_extra
        else:
            parte_pena = f"{faixa} {tp.lower()}".strip() if faixa else ""
            obs = ". ".join(x for x in (desc, parte_pena) if x).strip(". ")
        rec_campos = {
            "artigo": _artigo(r["art"], r["disp"]),
            "crime": _nome(r),
            "pena_min": mn if mn is not None else 0,
            "pena_max": mx if mx is not None else 0,
            "tipo_pena": tp,
            "acao": "Pública Incondicionada",
            "hediondo": "Não",
            "elemento": _elemento(r),
            "tentativa": "Sim",
            "violencia": _violencia(r),
            "grave_ameaca": _grave_ameaca(r),
            "obs": obs,
        }
        alvo = existentes.get(chave)
        if alvo:
            antes = (alvo["pena_min"], alvo["pena_max"], alvo["crime"])
            alvo.update(rec_campos)
            corrigidos.append((alvo["id"], antes, alvo))
        else:
            max_id += 1
            novo = {"id": max_id, "lei": LEI, **rec_campos}
            d.append(novo)
            novos.append(novo)
    return d, corrigidos, novos, existentes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True, type=Path)
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    d, corrigidos, novos, existentes = construir(args.entrada)
    print(f"reconciliação {args.entrada.name}: {len(corrigidos)} corrigidos em lugar, "
          f"{len(novos)} novos")
    print("\n== amostra CORRIGIDOS (id | antes → depois) ==")
    for cid, antes, dep in corrigidos[:12]:
        print(f"  {cid} {dep['artigo']:18s} {antes[0]}-{antes[1]} → {dep['pena_min']}-{dep['pena_max']} | {dep['crime'][:52]}")
    print("\n== amostra NOVOS ==")
    for n in novos[:12]:
        print(f"  {n['id']} {n['artigo']:18s} {n['pena_min']}-{n['pena_max']} {n['tipo_pena']:10s} | {n['crime'][:52]}")
    if args.aplicar:
        p = RAIZ / "data" / "crimes.json"
        with open(p, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        print(f"\nAPLICADO: {len(d)} registros em {p}")


if __name__ == "__main__":
    main()
