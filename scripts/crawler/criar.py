# -*- coding: utf-8 -*-
"""Gera linhas NOVAS do catálogo a partir dos achados (F6, segunda parte).

Enquanto `corrigir.py` ajusta linha existente, este módulo propõe linha que
falta: dispositivo com pena própria ausente do catálogo, e a **segunda moldura**
de um preceito que comina duas penas — o art. 254 do CP pune com reclusão de
três a seis anos no dolo e detenção de seis meses a dois anos na culpa, e cada
uma é um tipo penal, com sua URL.

**Nem tudo vem da lei.** Uma linha tem 14 campos; do texto saem seis. Os demais
seguem regra ou herança, e cada proposta declara qual foi a origem de cada campo,
para que a revisão saiba onde olhar:

- `elemento` — do próprio texto ("no caso de culpa", "se o crime é culposo");
- `tentativa` e `hediondo` — **regra**: crime culposo não admite tentativa nem é
  hediondo (os 43 culposos do catálogo confirmam a segunda; a primeira estava
  errada em 23 deles, corrigidos nesta mesma leva);
- `acao`, `violencia`, `grave_ameaca` — **herdados do caput** do mesmo artigo,
  que acerta em 90% dos parágrafos; é proposta, não certeza;
- `id` — o próximo livre, nunca reaproveitado.
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
from corrigir import inteiro  # noqa: E402
from transform_data import _faixa_de_meses  # noqa: E402

FONTE = RAIZ / "data" / "crimes.json"
FONTES = RAIZ / "data" / "fontes.json"
TIPOS = {"reclusão": "Reclusão", "detenção": "Detenção",
         "prisão simples": "Prisão simples"}
_CULPA = re.compile(r"\bculpos|\bculpa\b", re.IGNORECASE)


def _caput_do_artigo(catalogo: list[dict], lei: str, artigo: str) -> dict | None:
    """A linha do caput, de onde vêm os campos que a lei não declara."""
    base = re.match(r"(Art\.\s*[\w-]+)", artigo)
    if not base:
        return None
    alvo = base.group(1).lower()
    candidatas = [c for c in catalogo
                  if c["lei"] == lei
                  and (m := re.match(r"(Art\.\s*[\w-]+)", c["artigo"]))
                  and m.group(1).lower() == alvo]
    return next((c for c in candidatas if "caput" in c["artigo"].lower()),
                candidatas[0] if candidatas else None)


_CONDICAO = re.compile(
    r"\b(?:no caso de|se o|se a|se os|se as|quando)\b[^,.;:]{3,60}", re.IGNORECASE)


def _condicao(contexto: str) -> str | None:
    """A oração que distingue esta moldura das outras do mesmo preceito.

    O art. 299 do CP comina "reclusão, de um a cinco anos… se o documento é
    público, e reclusão de um a três anos… se o documento é particular": o que
    separa as duas linhas não é o dolo, é a condição. Rotular pela condição diz
    ao leitor por que existem duas.
    """
    m = _CONDICAO.search(contexto or "")
    return re.sub(r"\s+", " ", m.group(0)).strip().rstrip(",.;") if m else None


_QUALIFICADORA = re.compile(r"^(se\b|no caso\b|quando\b)[^:]{3,80}", re.IGNORECASE)


def _nome_do_crime(epigrafe: str | None, texto: str | None,
                   caput: dict | None, condicao: str | None) -> str:
    """Nome do tipo: epígrafe, nome do caput ou a conduta do próprio texto.

    Parágrafo qualificado costuma começar pela hipótese — "Se resulta lesão
    corporal de natureza grave" — e não repete o nome do crime. Herdar só o nome
    do caput daria dois registros homônimos para penas diferentes; o catálogo já
    resolve isso no estilo "Crime — Se resulta X", que é o adotado aqui.
    """
    base = epigrafe or (caput or {}).get("crime")
    limpo = re.sub(r"\s+", " ", (texto or "")).strip()
    if not base:
        return (limpo.split(":")[0][:110]).rstrip(" ,.;")
    base = base.rstrip(" ,.;")
    if condicao:
        return f"{base} ({condicao})"
    q = _QUALIFICADORA.match(limpo)
    if q:
        return f"{base} — {q.group(0).strip().rstrip(' ,.;')}"[:180]
    return base


def montar(achado: dict, fonte: dict, catalogo: list[dict], novo_id: int) -> dict:
    """Monta a linha proposta e o registro de onde veio cada campo."""
    lei = fonte["rotulos"][0]
    pena = achado["pena_lei"]
    chave = achado["chave"]
    artigo_base, marcador = chave.split("|", 1)
    artigo = artigo_base if marcador == "caput" else f"{artigo_base}, {marcador}"

    contexto = achado.get("contexto") or achado.get("detalhe", "")
    culposo = bool(_CULPA.search(contexto))
    condicao = _condicao(contexto) if achado["tipo"] == "MOLDURA-EXTRA" else None
    if achado["tipo"] == "MOLDURA-EXTRA":
        # Mesmo dispositivo, outra moldura: precisa de rótulo próprio, senão os
        # dois registros colidem na checagem de duplicata.
        artigo += f" ({condicao})" if condicao else " (2ª moldura)"

    caput = _caput_do_artigo(catalogo, lei, artigo_base)
    herda = lambda campo, padrao: (caput or {}).get(campo, padrao)  # noqa: E731

    linha = {
        "id": novo_id,
        "lei": lei,
        "artigo": artigo,
        "crime": _nome_do_crime(achado.get("epigrafe"), achado.get("texto_lei"),
                                caput, condicao),
        "pena_min": inteiro(pena["min"]),
        "pena_max": inteiro(pena["max"]),
        "tipo_pena": TIPOS.get((pena["tipo"] or "").lower(), "Reclusão"),
        "acao": herda("acao", "Pública Incondicionada"),
        "hediondo": "Não" if culposo else herda("hediondo", "Não"),
        "elemento": "Culposo" if culposo else "Doloso",
        "tentativa": "Não" if culposo else herda("tentativa", "Sim"),
        "violencia": "Não" if culposo else herda("violencia", "Não"),
        "grave_ameaca": "Não" if culposo else herda("grave_ameaca", "Não"),
        "obs": "",
    }
    faixa = _faixa_de_meses(pena["min"], pena["max"])
    origem = ("segunda moldura do mesmo preceito"
              if achado["tipo"] == "MOLDURA-EXTRA" else "dispositivo com pena própria")
    linha["obs"] = (f"{faixa} {linha['tipo_pena'].lower()}. Acrescido a partir do "
                    f"texto compilado ({origem}).")
    return {"linha": linha, "achado": achado,
            "herdado": [c for c in ("acao", "violencia", "grave_ameaca")
                        if caput and not culposo],
            "caput_id": (caput or {}).get("id")}


def gerar(fonte_id: str, proximo_id: int) -> tuple[list[dict], int]:
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    fonte = next(f for f in fontes["fontes"] if f["id"] == fonte_id) \
        if isinstance(fontes, dict) else next(f for f in fontes if f["id"] == fonte_id)
    achados = conferir_fonte(fonte, indexar_catalogo().get(fonte_id, {}),
                             carregar_excecoes())
    catalogo = json.loads(FONTE.read_text(encoding="utf-8"))

    propostas = []
    for a in achados:
        if a["tipo"] not in ("AUSENTE", "MOLDURA-EXTRA"):
            continue
        if not a.get("pena_lei"):
            continue                      # sem moldura legível não vira linha
        propostas.append(montar(a, fonte, catalogo, proximo_id))
        proximo_id += 1
    return propostas, proximo_id


def aplicar(propostas: list[dict]) -> None:
    dados = json.loads(FONTE.read_text(encoding="utf-8"))
    dados.extend(p["linha"] for p in propostas)
    texto = json.dumps(dados, ensure_ascii=False, indent=2) + "\n"
    FONTE.write_bytes(texto.replace("\n", "\r\n").encode("utf-8"))


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Propõe linhas novas do catálogo.")
    p.add_argument("--fonte", required=True)
    p.add_argument("--aplicar", action="store_true")
    args = p.parse_args()

    catalogo = json.loads(FONTE.read_text(encoding="utf-8"))
    propostas, _ = gerar(args.fonte, max(c["id"] for c in catalogo) + 1)
    print(f"{args.fonte}: {len(propostas)} linha(s) proposta(s)")
    for x in propostas:
        l = x["linha"]
        print(f"  id {l['id']:5d} {l['artigo']:26s} {l['pena_min']}–{l['pena_max']} "
              f"{l['tipo_pena']:14s} {l['elemento']:10s} {l['crime'][:44]}")
    if args.aplicar and propostas:
        aplicar(propostas)
        print("aplicado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
