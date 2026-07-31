# -*- coding: utf-8 -*-
"""Gera correções mecânicas do catálogo a partir dos achados (F6).

Escopo **estrito**: só ajusta moldura e tipo de pena de linha que **já existe**.
Nunca cria nem remove registro — criar exige decidir se o dispositivo é crime
autônomo, causa de aumento ou nada; remover exige decidir o destino da URL
pública. As duas coisas são juízo jurídico.

Este módulo encolheu à metade na v1.2.17. Antes, a moldura publicada era
extraída do TEXTO do `obs`, e corrigir uma pena significava reescrever prosa de
modo que a expressão regular relesse a faixa certa — com conversão de números
por extenso, concordância de singular e uma etapa de verificação para conferir
se o texto gerado voltava a ser lido direito. Com `pena_min`/`pena_max` na
autoridade, corrigir uma pena é atribuir dois números; o `obs` é atualizado
apenas para não descrever a pena antiga.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from conferir import carregar_excecoes, conferir_fonte, indexar_catalogo  # noqa: E402
from transform_data import _faixa_de_meses  # noqa: E402

FONTE = RAIZ / "data" / "crimes.json"
TIPOS = {"reclusão": "Reclusão", "detenção": "Detenção",
         "prisão simples": "Prisão simples"}


def inteiro(v: float):
    """24, nunca 24.0 — a CI reprova float inteiro em `pena_min`/`pena_max`."""
    v = round(float(v), 4)
    return int(v) if float(v).is_integer() else v


def reescrever_obs(obs: str, faixa: str, tipo: str) -> str:
    """Troca a moldura descrita no início do `obs`, preservando o resto.

    O `obs` não define mais a pena, mas continua sendo lido por gente: deixá-lo
    anunciando a moldura antiga seria publicar uma contradição.
    """
    novo = f"{faixa} {tipo.lower()}"
    m = re.search(r"(reclus[ãa]o|deten[çc][ãa]o|pris[ãa]o simples)", obs or "", re.I)
    if not m:
        return f"{novo}. {obs}".strip() if obs else novo
    cauda = obs[m.end():].strip(" .;")
    if not cauda:
        return novo
    return f"{novo} {cauda}" if cauda.startswith(("+", "e ", "ou ")) else f"{novo}. {cauda}"


def propor(linha: dict, alvo_min: float, alvo_max: float,
           tipo_lei: str | None, evidencia: str) -> dict | None:
    """Linha corrigida, ou None quando não há mudança a fazer."""
    nova = dict(linha)
    nova["pena_min"] = inteiro(alvo_min)
    nova["pena_max"] = inteiro(alvo_max)
    if tipo_lei:
        nova["tipo_pena"] = TIPOS.get(tipo_lei.lower(), linha["tipo_pena"])
    nova["obs"] = reescrever_obs(linha.get("obs", ""),
                                 _faixa_de_meses(alvo_min, alvo_max),
                                 nova["tipo_pena"])
    if all(nova[k] == linha.get(k) for k in ("pena_min", "pena_max", "tipo_pena", "obs")):
        return None
    return {"id": linha["id"], "antes": linha, "depois": nova,
            "evidencia": evidencia[:160]}


def gerar(fonte_id: str) -> tuple[list[dict], list[dict]]:
    """(propostas, achados que ficam para decisão humana) de um diploma."""
    fontes = json.loads((RAIZ / "data" / "fontes.json").read_text(encoding="utf-8"))
    fonte = next(f for f in fontes["fontes"] if f["id"] == fonte_id)
    achados = conferir_fonte(fonte, indexar_catalogo().get(fonte_id, {}),
                             carregar_excecoes())
    catalogo = {c["id"]: c for c in json.loads(FONTE.read_text(encoding="utf-8"))}

    propostas, humanos = [], []
    for a in achados:
        # Mecânico é só o que tem UMA linha correspondente e moldura legível na
        # lei. Ausente, revogado, "só multa" e leitura incerta ficam de fora.
        if not a["tipo"].startswith("DIVERGENTE") or len(a.get("ids", [])) != 1:
            humanos.append(a)
            continue
        # Preceito com DUAS molduras (dolosa e culposa no mesmo texto) pede
        # linha nova, não sobrescrita — é modelagem, e vai para a issue.
        # Pena escrita como teto ("reclusão até cinco anos", comum no Código
        # Eleitoral) é caso simples: registra-se sem mínimo, como o catálogo já
        # faz nos tipos que só têm teto.
        if a.get("multiplas"):
            humanos.append(a)
            continue
        linha = catalogo.get(a["ids"][0])
        lei = a.get("pena_lei")
        if linha is None or not lei:
            humanos.append(a)
            continue
        p = propor(linha, lei["min"], lei["max"], lei["tipo"], a["detalhe"])
        (propostas if p else humanos).append(p or a)
    return propostas, humanos


def aplicar(propostas: list[dict]) -> None:
    """Escreve na FONTE (nunca no derivado), preservando ordem e formato."""
    dados = json.loads(FONTE.read_text(encoding="utf-8"))
    por_id = {p["id"]: p["depois"] for p in propostas}
    texto = json.dumps([por_id.get(c["id"], c) for c in dados],
                       ensure_ascii=False, indent=2) + "\n"
    FONTE.write_bytes(texto.replace("\n", "\r\n").encode("utf-8"))


def resumo(fonte_id: str, propostas: list[dict], humanos: list[dict]) -> str:
    """Corpo do PR: uma seção por mudança, com a evidência ao lado."""
    fontes = json.loads((RAIZ / "data" / "fontes.json").read_text(encoding="utf-8"))
    f = next(x for x in fontes["fontes"] if x["id"] == fonte_id)
    linhas = [
        f"## Diploma: **{', '.join(f['rotulos'])}**", "",
        f"Texto oficial conferido: <{f['url']}>", "",
        f"{len(propostas)} correção(ões) de **moldura ou tipo de pena** em linhas "
        "que já existem. Nenhum registro é criado ou removido.", "",
    ]
    for p in propostas:
        a, d = p["antes"], p["depois"]
        linhas += [
            f"### `{a['artigo']}` — id {a['id']}", f"*{a['crime'][:110]}*", "",
            f"- **Na lei:** {p['evidencia']}",
            f"- **Antes:** {a['pena_min']}–{a['pena_max']} meses, {a['tipo_pena']}",
            f"- **Depois:** {d['pena_min']}–{d['pena_max']} meses, {d['tipo_pena']}",
            f"- **obs:** `{d['obs'][:150]}`",
            f"- Conferir: <https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo={a['id']}>",
            "",
        ]
    if humanos:
        linhas += [
            f"### Fora do automático ({len(humanos)})", "",
            "Seguem na issue do conferidor: dispositivo ausente ou revogado, pena "
            "só de multa, leitura incerta, ou mais de uma linha do catálogo para o "
            "mesmo dispositivo.", "",
        ]
        for a in humanos[:25]:
            linhas.append(f"- `{a.get('chave', '?')}` — {a['tipo']}: {a['detalhe'][:100]}")
    return "\n".join(linhas) + "\n"


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Gera correções mecânicas do catálogo.")
    p.add_argument("--fonte", required=True)
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--corpo")
    args = p.parse_args()

    propostas, humanos = gerar(args.fonte)
    print(f"{args.fonte}: {len(propostas)} correção(ões), {len(humanos)} para decisão humana")
    for x in propostas:
        a, d = x["antes"], x["depois"]
        print(f"  id {x['id']:5d} {a['artigo']:24s} {a['pena_min']}–{a['pena_max']} "
              f"→ {d['pena_min']}–{d['pena_max']} {d['tipo_pena']}")
    if args.corpo:
        Path(args.corpo).write_text(resumo(args.fonte, propostas, humanos), encoding="utf-8")
    if args.aplicar and propostas:
        aplicar(propostas)
        print(f"aplicado em {FONTE}")
    return 0 if propostas else 1


if __name__ == "__main__":
    raise SystemExit(main())
