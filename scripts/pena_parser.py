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

    # Vale o intervalo que aparece PRIMEIRO no texto, não o primeiro padrão que
    # casar. Testar RANGE_2U antes de RANGE_1U fazia uma pena posterior vencer a
    # anterior: no art. 254 do CP — "reclusão, de três a seis anos, e multa, no
    # caso de dolo, ou detenção, de seis meses a dois anos, no caso de culpa" —
    # a moldura lida era a culposa. O preceito do caput é sempre o primeiro.
    candidatos = []
    m = RANGE_2U.search(text)
    if m:
        candidatos.append((m.start(), (int(m.group(1)), _norm_unidade(m.group(2)),
                                       int(m.group(3)), _norm_unidade(m.group(4)))))
    m = RANGE_1U.search(text)
    if m:
        u = _norm_unidade(m.group(3))
        candidatos.append((m.start(), (int(m.group(1)), u, int(m.group(2)), u)))
    m = ABBR.search(text)
    if m:
        candidatos.append((m.start(), (int(m.group(1)), _ABBR_U[m.group(2).lower()],
                                       int(m.group(3)), _ABBR_U[m.group(4).lower()])))
    return min(candidatos)[1] if candidatos else None


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
# Preceito PECUNIÁRIO escrito à moda de 1965: "Pena - pagamento de 250 a 300
# dias-multa". O Código Eleitoral comina assim dezenas de tipos, e a fórmula não
# começa pela palavra "multa" — começa por "pagamento".
#
# Enquanto ela não era reconhecida, `ler_penas` devolvia lista vazia e o
# conferidor PULAVA o dispositivo: o registro entrava na conta dos
# "indeterminados" e nunca era confrontado. Foi por esse buraco que três artigos
# do CE publicaram por meses pena privativa de liberdade — o 313 com reclusão de
# 2 a 6 anos, o 303 com detenção de 6 meses a 2 anos e o 306 com 1 a 6 meses —
# para artigos que não cominam prisão nenhuma. O erro inverte a classe inteira
# de benefícios do registro, e era invisível justamente por ser silêncio.
_SO_PECUNIARIA = re.compile(
    r"^\s*pena\s*[-–—:]?\s*(?:o\s+)?pagamento\s+de\b.{0,80}?\bmulta\b",
    re.IGNORECASE | re.DOTALL)
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


_TIPO_RE = re.compile(r"(reclus[ãa]o|deten[çc][ãa]o|pris[ãa]o simples)", re.IGNORECASE)
# "reclusão OU detenção, de um a três anos" (CP, art. 306, § único) é UMA
# moldura com espécie alternativa, não duas molduras. O que separa as duas
# palavras é só um conectivo; quando há duas penas de verdade, entre elas está
# a moldura da primeira ("reclusão, de três a seis anos, … ou detenção, …").
_CONECTIVO = re.compile(r"[\s,;]*(?:ou|e)?[\s,;]*")


def ler_penas(texto: str) -> list[dict]:
    """TODAS as molduras de um preceito secundário, na ordem em que aparecem.

    Um mesmo preceito às vezes comina duas penas — o art. 254 do CP traz
    "reclusão, de três a seis anos… no caso de dolo, ou detenção, de seis meses
    a dois anos, no caso de culpa". São **dois tipos penais**, não um: no
    catálogo, cada moldura é uma linha própria, com sua URL. Ler só a primeira
    (ou pior, a última) apagaria uma delas.

    Devolve lista vazia quando não há pena privativa reconhecível.
    """
    if not texto:
        return []
    bruto = texto.strip()
    marcas = list(_TIPO_RE.finditer(bruto))
    if not marcas:
        lida = ler_pena(bruto)          # pode ser "só multa"
        return [lida] if lida else []

    molduras: list[dict] = []
    i = 0
    while i < len(marcas):
        j = i
        while (j + 1 < len(marcas)
               and _CONECTIVO.fullmatch(bruto[marcas[j].end():marcas[j + 1].start()])):
            j += 1                      # espécie alternativa: mesma moldura
        fim = marcas[j + 1].start() if j + 1 < len(marcas) else len(bruto)
        trecho = bruto[marcas[i].start():fim]
        lida = ler_pena(trecho)
        if lida is None:
            # Espécie DEPOIS da moldura: "será punida com a pena de 2 (dois) a 5
            # (cinco) anos de reclusão e multa" (Lei 7.643, art. 2º). Fatiar a
            # partir da espécie deixa o intervalo para trás. A janela de 70
            # caracteres alcança o que veio antes sem arrastar a conduta inteira,
            # que costuma trazer números alheios à pena.
            inicio = max(0 if i == 0 else marcas[i - 1].end(), marcas[i].start() - 70)
            lida = ler_pena(bruto[inicio:fim])
        if lida and not lida["so_multa"]:
            tipos = [m.group(0).lower() for m in marcas[i:j + 1]]
            lida["tipos"] = tipos
            # Com espécie alternativa, `tipo` fica com as duas: escolher uma é
            # decisão de modelagem, e os geradores recusam o que não é uma das
            # três espécies do catálogo.
            lida["tipo"] = " ou ".join(tipos)
            lida["contexto"] = trecho[:120]
            molduras.append(lida)
        i = j + 1
    return molduras


def ler_pena(texto: str) -> dict | None:
    """Interpreta uma linha de pena do Planalto.

    Devolve `{"tipo", "min_meses", "max_meses", "so_multa", "teto_apenas"}` ou
    None quando não há pena reconhecível. `so_multa=True` marca o dispositivo
    cuja única sanção é pecuniária — caso da LCP, art. 32.
    """
    if not texto:
        return None
    bruto = texto.strip()
    # A MULTA vem primeiro: preceito que começa por "Pena - multa" comina multa,
    # e o que vier depois do ponto e vírgula é consequência, não espécie de pena.
    # O art. 254 do ECA ("Pena - multa …; duplicada em caso de reincidência a
    # autoridade judiciária poderá determinar a SUSPENSÃO da programação da
    # emissora por até dois dias") era lido como pena de "suspensão" de dois
    # dias, e virou um "crime" no catálogo — sendo infração administrativa.
    # Procurar a espécie antes do teste de multa é o que permitia isso.
    if (_SO_MULTA.match(bruto) or _SO_PECUNIARIA.match(bruto)) and not _TIPO_RE.search(bruto):
        return {"tipo": None, "min_meses": 0.0, "max_meses": 0.0,
                "so_multa": True, "teto_apenas": False}
    tipo = next((t for t in _TIPOS if t in bruto.lower()), None)
    if tipo is None:
        # Sem tipo de pena privativa: ou é só multa, ou não é preceito de pena.
        return ({"tipo": None, "min_meses": 0.0, "max_meses": 0.0,
                 "so_multa": True, "teto_apenas": False}
                if (_SO_MULTA.match(bruto) or _SO_PECUNIARIA.match(bruto)) else None)

    limpo = _extenso_para_numero(_limpar(bruto))
    faixa = parse_pena_range(limpo)
    if faixa:
        vmin, umin, vmax, umax = faixa
        minimo, maximo = _meses(vmin, umin), _meses(vmax, umax)
        # Mínimo maior que máximo não é moldura: é leitura errada. Acontece
        # quando a pena vem embutida no corpo do artigo junto de outros números
        # — o art. 58 do DL 6.259/44 comina "prisão simples e multa de dez mil
        # cruzeiros a cinquenta mil cruzeiros", e os valores monetários viram
        # faixa de tempo. Recusar é melhor que propor pena invertida.
        if minimo > maximo:
            return None
        return {"tipo": tipo, "tipos": [tipo], "min_meses": minimo,
                "max_meses": maximo, "so_multa": False, "teto_apenas": False}

    m = _ATE.search(limpo)
    if m:
        valor = m.group(1)
        valor = int(valor) if valor.isdigit() else _EXTENSO[valor.lower()]
        return {"tipo": tipo, "tipos": [tipo], "min_meses": 0.0,
                "max_meses": _meses(valor, _norm_unidade(m.group(2))),
                "so_multa": False, "teto_apenas": True}
    return None
