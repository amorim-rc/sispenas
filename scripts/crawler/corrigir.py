# -*- coding: utf-8 -*-
"""Gera correções mecânicas do catálogo a partir dos achados (F6).

Escopo **estrito**: só ajusta moldura e tipo de pena de linha que **já existe**.
Nunca cria nem remove registro — criar exige decidir se o dispositivo é crime
autônomo, causa de aumento ou nada; remover exige decidir o destino da URL
pública. As duas coisas são juízo jurídico, e ficam com quem tem competência
para isso.

**A salvaguarda que sustenta o resto**: cada correção é aplicada e depois
*verificada no derivado*. A moldura publicada não vem de `pena_min`/`pena_max`,
vem do `obs` (via `parse_pena_range`) — foi assim que o id 622 acabou exibindo
"3 meses a 1 ano" por causa de uma faixa secundária no texto ("antes era 3 meses
a 1 ano"). Então o gerador reescreve o `obs`, roda a mesma derivação que a
aplicação usa e **descarta a proposta se o resultado não bater com a lei**. O
que não se verifica não vira PR: volta para a issue, para decisão humana.
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

from conferir import chave, carregar_excecoes, conferir_fonte, indexar_catalogo  # noqa: E402
from pena_parser import UNIDADE_EM_MESES, parse_pena_range  # noqa: E402

FONTE = RAIZ / "data" / "crimes.json"
DERIVADO = RAIZ / "static" / "data" / "crimes.json"

_NUM_POR_EXTENSO = {
    1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco", 6: "seis",
    7: "sete", 8: "oito", 9: "nove", 10: "dez", 11: "onze", 12: "doze",
    15: "quinze", 20: "vinte", 30: "trinta", 40: "quarenta",
}


def _rotulo_faixa(meses_min: float, meses_max: float) -> tuple[str, str]:
    """Escreve a faixa como o catálogo escreve: "2-5 anos", "6 meses a 2 anos"."""
    def parte(m: float) -> tuple[float, str]:
        if m >= 12 and m % 12 == 0:
            return m / 12, "anos"
        if m >= 1:
            return m, "meses"
        return round(m * 30), "dias"

    vmin, umin = parte(meses_min)
    vmax, umax = parte(meses_max)
    fmt = lambda v: f"{int(v)}" if float(v).is_integer() else f"{v:g}"  # noqa: E731
    # "1 anos" não existe: a unidade concorda com o número que a acompanha.
    sing = {"anos": "ano", "meses": "mês", "dias": "dia"}
    u_min = sing[umin] if vmin == 1 else umin
    u_max = sing[umax] if vmax == 1 else umax
    if umin == umax and vmin != 1 and vmax != 1:
        return f"{fmt(vmin)}-{fmt(vmax)} {u_max}", umax
    return f"{fmt(vmin)} {u_min} a {fmt(vmax)} {u_max}", umax


def neutralizar_faixas_extras(texto: str) -> str:
    """Escreve por extenso as faixas numéricas que NÃO são a moldura do tipo.

    `parse_pena_range` pega o primeiro padrão que casar, e "3 meses a 1 ano"
    (duas unidades) vence "2-5 anos" (uma unidade) mesmo aparecendo depois. Em
    vez de exigir que ninguém mencione outra faixa no `obs`, o texto secundário
    passa a ser escrito por extenso — legível para quem lê, invisível para o
    parser.
    """
    def extenso(n: str) -> str:
        return _NUM_POR_EXTENSO.get(int(n), n)

    # O intervalo com hífen vem primeiro: em "1-3 anos" só o "3" está colado à
    # unidade, e converter isoladamente deixaria "1-três anos".
    texto = re.sub(
        r"\b(\d+)\s*[-–—]\s*(\d+)\s*(dias?|meses|m[eê]s|anos?)\b",
        lambda m: f"{extenso(m.group(1))} a {extenso(m.group(2))} {m.group(3)}",
        texto)
    return re.sub(r"\b(\d+)\s*(dias?|meses|m[eê]s|anos?)\b",
                  lambda m: f"{extenso(m.group(1))} {m.group(2)}", texto)


def propor(linha: dict, alvo_min: float, alvo_max: float,
           tipo_lei: str | None, texto_lei: str) -> dict | None:
    """Monta a linha corrigida. None quando não há o que fazer com segurança."""
    nova = dict(linha)
    faixa, _ = _rotulo_faixa(alvo_min, alvo_max)
    tipo = (tipo_lei or linha["tipo_pena"]).capitalize()
    if tipo.lower().startswith("prisão simples"):
        tipo = "Prisão simples"

    # O obs LIDERA pela moldura correta; o que vinha depois é preservado, com as
    # faixas numéricas secundárias escritas por extenso.
    resto = (linha.get("obs") or "")
    m = re.search(r"(?:reclus[ãa]o|deten[çc][ãa]o|pris[ãa]o simples)", resto, re.I)
    cauda = resto[m.end():] if m else resto
    cauda = neutralizar_faixas_extras(cauda).strip(" .;")
    if not cauda:
        obs = f"{faixa} {tipo.lower()}"
    elif cauda.startswith(("+", "e ", "ou ")):
        obs = f"{faixa} {tipo.lower()} {cauda}"
    else:
        obs = f"{faixa} {tipo.lower()}. {cauda}"

    # Inteiro quando o valor é inteiro: o catálogo escreve 24, não 24.0, e um
    # float espúrio polui o diff e muda o tipo no JSON público.
    inteiro = lambda v: int(v) if float(v).is_integer() else round(v, 4)  # noqa: E731
    nova["pena_min"] = inteiro(alvo_min)
    nova["pena_max"] = inteiro(alvo_max)
    nova["tipo_pena"] = tipo
    nova["obs"] = obs.strip()
    if (nova["pena_min"], nova["pena_max"], nova["tipo_pena"], nova["obs"]) == \
       (linha.get("pena_min"), linha.get("pena_max"), linha.get("tipo_pena"), linha.get("obs")):
        return None
    return {"id": linha["id"], "antes": linha, "depois": nova,
            "texto_lei": texto_lei[:160]}


def verificar(proposta: dict, alvo_min: float, alvo_max: float) -> bool:
    """A moldura DERIVADA da proposta bate com a lei?

    Esta é a linha de defesa: o obs é reescrito por heurística, e heurística
    erra. Se a derivação — a mesma que a aplicação usa — não reproduzir a faixa
    da lei, a proposta é descartada em vez de virar PR.
    """
    faixa = parse_pena_range(proposta["depois"]["obs"])
    if not faixa:
        return False
    vmin, umin, vmax, umax = faixa
    obtido = (round(vmin * UNIDADE_EM_MESES[umin], 4),
              round(vmax * UNIDADE_EM_MESES[umax], 4))
    return obtido == (round(alvo_min, 4), round(alvo_max, 4))


def gerar(fonte_id: str) -> tuple[list[dict], list[dict]]:
    """(propostas verificadas, achados recusados) para um diploma."""
    fontes = json.loads((RAIZ / "data" / "fontes.json").read_text(encoding="utf-8"))
    fonte = next(f for f in fontes["fontes"] if f["id"] == fonte_id)
    achados = conferir_fonte(fonte, indexar_catalogo().get(fonte_id, {}),
                             carregar_excecoes())
    catalogo = {c["id"]: c for c in json.loads(FONTE.read_text(encoding="utf-8"))}

    propostas, recusados = [], []
    for a in achados:
        if not a["tipo"].startswith("DIVERGENTE") or len(a.get("ids", [])) != 1:
            recusados.append(a)
            continue
        m = re.search(r"lei\s+([\d.]+)–([\d.]+)", a["detalhe"])
        tipo_m = re.search(r"lei\s+(reclusão|detenção|prisão simples)", a["detalhe"])
        if not m and not tipo_m:
            recusados.append(a)   # "só multa", teto sem mínimo, leitura incerta
            continue
        linha = catalogo.get(a["ids"][0])
        if not linha:
            recusados.append(a)
            continue
        if m:
            alvo = (float(m.group(1)), float(m.group(2)))
        else:
            alvo = (float(linha.get("pena_min") or 0), float(linha.get("pena_max") or 0))
        p = propor(linha, alvo[0], alvo[1],
                   tipo_m.group(1) if tipo_m else None, a["detalhe"])
        if p and verificar(p, *alvo):
            p["achado"] = a
            propostas.append(p)
        else:
            recusados.append(a)
    return propostas, recusados


def aplicar(propostas: list[dict]) -> None:
    """Escreve na FONTE (nunca no derivado), preservando formato e ordem."""
    dados = json.loads(FONTE.read_text(encoding="utf-8"))
    por_id = {p["id"]: p["depois"] for p in propostas}
    saida = [por_id.get(c["id"], c) for c in dados]
    texto = json.dumps(saida, ensure_ascii=False, indent=2) + "\n"
    FONTE.write_bytes(texto.replace("\n", "\r\n").encode("utf-8"))


def resumo(fonte_id: str, propostas: list[dict], recusados: list[dict]) -> str:
    """Corpo do PR: cada mudança com a evidência, para revisão dispositivo a
    dispositivo. O diploma vem no título e em cada bloco, para que ninguém
    precise adivinhar qual lei está sendo alterada."""
    fontes = json.loads((RAIZ / "data" / "fontes.json").read_text(encoding="utf-8"))
    fonte = next(f for f in fontes["fontes"] if f["id"] == fonte_id)
    rotulos = ", ".join(fonte["rotulos"])
    linhas = [
        f"## Diploma: **{rotulos}**",
        "",
        f"Fonte oficial conferida: <{fonte['url']}>",
        "",
        f"{len(propostas)} correção(ões) mecânica(s) proposta(s) pelo conferidor. "
        "Cada uma ajusta **moldura ou tipo de pena de linha existente** — nenhuma "
        "cria ou remove registro.",
        "",
        "> Toda proposta foi verificada: depois de reescrita, a moldura **derivada** "
        "(a mesma que a aplicação publica) foi comparada com a da lei. O que não "
        "reproduziu a faixa foi descartado e segue na issue.",
        "",
    ]
    for p in propostas:
        a, d = p["antes"], p["depois"]
        linhas += [
            f"### `{a['artigo']}` — id {a['id']}",
            f"*{a['crime'][:110]}*",
            "",
            f"- **Lei:** {p['texto_lei']}",
            f"- **Antes:** {a['pena_min']}–{a['pena_max']} meses, {a['tipo_pena']}",
            f"- **Depois:** {d['pena_min']}–{d['pena_max']} meses, {d['tipo_pena']}",
            f"- **obs:** `{d['obs'][:150]}`",
            f"- Conferir: <https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo={a['id']}>",
            "",
        ]
    if recusados:
        linhas += [
            f"### Não automatizado ({len(recusados)})", "",
            "Segue para decisão humana na issue do conferidor — dispositivo "
            "ausente, revogado, pena só de multa, leitura incerta ou mais de uma "
            "linha do catálogo para o mesmo dispositivo.", "",
        ]
        for a in recusados[:20]:
            linhas.append(f"- `{a.get('chave', '?')}` — {a['tipo']}: {a['detalhe'][:100]}")
    return "\n".join(linhas) + "\n"


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Gera correções mecânicas do catálogo.")
    p.add_argument("--fonte", required=True)
    p.add_argument("--aplicar", action="store_true",
                   help="escreve em data/crimes.json (sem isto, só simula)")
    p.add_argument("--corpo", help="arquivo para o corpo do PR")
    args = p.parse_args()

    propostas, recusados = gerar(args.fonte)
    print(f"{args.fonte}: {len(propostas)} correção(ões) verificada(s), "
          f"{len(recusados)} para decisão humana")
    for x in propostas:
        print(f"  id {x['id']:5d} {x['antes']['artigo']:22s} "
              f"{x['antes']['pena_min']}–{x['antes']['pena_max']} → "
              f"{x['depois']['pena_min']}–{x['depois']['pena_max']} "
              f"{x['depois']['tipo_pena']}")
    if args.corpo:
        Path(args.corpo).write_text(resumo(args.fonte, propostas, recusados),
                                    encoding="utf-8")
    if args.aplicar and propostas:
        aplicar(propostas)
        print(f"aplicado em {FONTE}")
    return 0 if propostas else 1


if __name__ == "__main__":
    raise SystemExit(main())
