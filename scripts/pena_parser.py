# -*- coding: utf-8 -*-
"""Leitura de penas em texto — compartilhado pelo catálogo e pelo conferidor.

Extraído de `transform_data.py` na F3 do conferidor: os dois lados precisam ler
a MESMA moldura do MESMO jeito, senão o differ acusaria divergência onde só há
duas implementações discordando. O `transform_data` importa daqui; o conferidor
usa as funções estendidas (`ler_pena`) para interpretar o texto do Planalto.

Regras que a revisão manual e a F2 deixaram claras:

- **Dias-multa não é prisão.** "500 a 1.500 dias-multa" casaria um intervalo e
  sobreporia o tempo de reclusão. Neutralizado antes de qualquer busca.
- **Multa em réis não é prisão.** A LCP comina "multa, de duzentos mil réis a
  dois contos de réis": há intervalo, mas não há pena privativa.
- **Algarismos mandam, não o extenso.** O texto oficial erra o por-extenso (o
  art. 121, § 2º-D traz "de 20 (vinte) a 40 (quarenta anos)"), e o extenso entre
  parênteses só repete o algarismo — some antes do parse.
- **Pena só com teto.** "até cinco anos" (CPM, art. 290) não tem mínimo
  explícito: o mínimo é o legal (1 dia), e registrá-lo como zero é diferente de
  "sem pena privativa".
"""
from __future__ import annotations

import re

# ── Unidades ────────────────────────────────────────────────────────────────
# Fator de conversão para MESES (unidade canônica de cálculo). O CP conta o mês
# como 30 dias (Art. 11), então 1 dia = 1/30 mês e 1 ano = 12 meses.
UNIDADE_EM_MESES = {"dias": 1 / 30, "meses": 1.0, "anos": 12.0}
_NOMES_UNIDADE = {"dias": ("dia", "dias"), "meses": ("mês", "meses"),
                  "anos": ("ano", "anos")}


def _norm_unidade(u: str) -> str:
    u = u.lower()
    if u.startswith("d"):
        return "dias"
    if u.startswith("a"):
        return "anos"
    return "meses"  # mês / mes / meses


def _rotulo(valor: float, unidade: str) -> str:
    inteiro = int(valor) if float(valor).is_integer() else valor
    sing, plur = _NOMES_UNIDADE[unidade]
    return f"{inteiro} {sing if inteiro == 1 else plur}"


def _meses(valor: float, unidade: str) -> float:
    return round(valor * UNIDADE_EM_MESES[unidade], 4)


# ── Intervalos em algarismos (comportamento histórico do catálogo) ──────────
_U = r"(dias?|meses|m[eê]s|anos?)"
RANGE_2U = re.compile(rf"(\d+)\s*{_U}\s*a\s*(\d+)\s*{_U}", re.IGNORECASE)
RANGE_1U = re.compile(rf"(\d+)\s*(?:a|-|–|—)\s*(\d+)\s*{_U}", re.IGNORECASE)
ABBR = re.compile(r"(\d+)\s*([dma])\s*(?:-|a|–|—)\s*(\d+)\s*([dma])", re.IGNORECASE)
_ABBR_U = {"d": "dias", "m": "meses", "a": "anos"}


def parse_pena_range(obs: str):
    """Extrai o primeiro intervalo de pena do texto -> (vmin, umin, vmax, umax).

    Reconhece "15 dias a 6 meses", "1-5 anos", "2 a 5 anos", "3m-1a". Retorna
    None se nada for encontrado. O primeiro match corresponde ao caput.

    Neutraliza antes o "dias-multa" (pena de MULTA em dias-multa, art. 49 do CP):
    ele nunca é a pena de prisão, mas casaria o padrão "5 a 15 dias" e sobreporia
    o tempo de reclusão/detenção — o que corromperia, p.ex., os crimes eleitorais
    ("reclusão até 5 anos e 5 a 15 dias-multa") e os de tráfico ("500 a 1.500
    dias-multa").
    """
    text = re.sub(r"dias?\s*[-\s]?\s*multa", " multa ", obs or "", flags=re.IGNORECASE)
    m = RANGE_2U.search(text)
    if m:
        return (int(m.group(1)), _norm_unidade(m.group(2)),
                int(m.group(3)), _norm_unidade(m.group(4)))
    m = RANGE_1U.search(text)
    if m:
        u = _norm_unidade(m.group(3))
        return int(m.group(1)), u, int(m.group(2)), u
    m = ABBR.search(text)
    if m:
        return (int(m.group(1)), _ABBR_U[m.group(2).lower()],
                int(m.group(3)), _ABBR_U[m.group(4).lower()])
    return None


# ── Leitura do texto do Planalto (usada pelo conferidor) ────────────────────
_EXTENSO = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3, "quatro": 4,
    "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
    "onze": 11, "doze": 12, "treze": 13, "quatorze": 14, "catorze": 14,
    "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18,
    "dezenove": 19, "vinte": 20, "trinta": 30, "quarenta": 40,
    "cinquenta": 50, "sessenta": 60,
}
_TIPOS = ("reclusão", "detenção", "prisão simples", "impedimento", "suspensão")
# "multa, de duzentos mil réis a dois contos de réis" — intervalo que NÃO é pena
# privativa. Reconhecido para ser descartado, não para ser lido.
_SO_MULTA = re.compile(r"^\s*pena\s*[-–—:]?\s*multa\b", re.IGNORECASE)
_ATE = re.compile(
    rf"at[ée]\s+(\d+|{'|'.join(_EXTENSO)})\s*\(?[^)]*\)?\s*{_U}", re.IGNORECASE)


_NUM_EXTENSO = re.compile("|".join(rf"\b{p}\b" for p in _EXTENSO), re.IGNORECASE)


def _limpar(texto: str) -> str:
    """Tira os dias-multa e o número por extenso, preservando a unidade.

    Não basta apagar o parêntese inteiro: quando o texto oficial erra a
    pontuação — "40 (quarenta anos)" no art. 121, § 2º-D —, a unidade está
    DENTRO dele, e apagá-la deixaria "de 20 a 40", sem unidade, ilegível. Então:
    parêntese com dígitos (anotação, remissão) sai fora; parêntese de palavras
    perde os numerais e devolve o resto ("anos").
    """
    t = re.sub(r"dias?\s*[-\s]?\s*multa", " multa ", texto or "", flags=re.IGNORECASE)

    def trata(m: re.Match) -> str:
        conteudo = m.group(1)
        if re.search(r"\d", conteudo):
            return " "
        resto = _NUM_EXTENSO.sub("", conteudo).strip()
        return f" {resto} " if resto else " "

    return re.sub(r"\(([^()]*)\)", trata, t)


_DEZENAS = ("vinte", "trinta", "quarenta", "cinquenta", "sessenta")
_UNIDADES = [p for p in _EXTENSO if _EXTENSO[p] < 10]
# "vinte e quatro" é UM número (24), não dois. Sem tratar o composto, o art.
# 159, § 3º ("de vinte e quatro a trinta anos") vira "de 20 e 4 a 30 anos" e a
# moldura sai 4–30 em vez de 24–30.
_COMPOSTO = re.compile(
    rf"\b({'|'.join(_DEZENAS)})\s+e\s+({'|'.join(_UNIDADES)})\b", re.IGNORECASE)
_SIMPLES = re.compile("|".join(rf"\b{p}\b" for p in _EXTENSO), re.IGNORECASE)


def _extenso_para_numero(texto: str) -> str:
    """Converte "de seis a vinte anos" em "de 6 a 20 anos" (CP de 1940)."""
    texto = _COMPOSTO.sub(
        lambda m: str(_EXTENSO[m.group(1).lower()] + _EXTENSO[m.group(2).lower()]),
        texto)
    return _SIMPLES.sub(lambda m: str(_EXTENSO[m.group(0).lower()]), texto)


def ler_pena(texto: str) -> dict | None:
    """Interpreta uma linha de pena do Planalto.

    Devolve `{"tipo", "min_meses", "max_meses", "so_multa", "teto_apenas"}` ou
    None quando não há pena reconhecível. `so_multa=True` marca o dispositivo
    cuja única sanção é pecuniária — caso da LCP, art. 32.
    """
    if not texto:
        return None
    bruto = texto.strip()
    tipo = next((t for t in _TIPOS if t in bruto.lower()), None)
    if tipo is None:
        # Sem tipo de pena privativa: ou é só multa, ou não é preceito de pena.
        return ({"tipo": None, "min_meses": 0.0, "max_meses": 0.0,
                 "so_multa": True, "teto_apenas": False}
                if _SO_MULTA.match(bruto) else None)

    limpo = _extenso_para_numero(_limpar(bruto))
    faixa = parse_pena_range(limpo)
    if faixa:
        vmin, umin, vmax, umax = faixa
        return {"tipo": tipo, "min_meses": _meses(vmin, umin),
                "max_meses": _meses(vmax, umax), "so_multa": False,
                "teto_apenas": False}

    m = _ATE.search(limpo)
    if m:
        valor = m.group(1)
        valor = int(valor) if valor.isdigit() else _EXTENSO[valor.lower()]
        return {"tipo": tipo, "min_meses": 0.0,
                "max_meses": _meses(valor, _norm_unidade(m.group(2))),
                "so_multa": False, "teto_apenas": True}
    return None
