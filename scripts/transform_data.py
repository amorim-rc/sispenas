#!/usr/bin/env python3
"""
Enriquece o catálogo de tipos penais (crimes.json).

Deriva campos estruturados a partir do texto legal para permitir filtros
combinados por modalidade de pena e cálculo de benefícios penais:

  - pena_privativa : Reclusão | Detenção | Prisão simples | Nenhuma
  - tem_multa      : bool  (multa cumulada OU alternativa OU isolada)
  - multa_regime   : cumulativa | alternativa | isolada | nenhuma
  - infracao_menor_potencial : bool (pena máx <= 2 anos -> JECRIM)
  - tem_pena_privativa : bool (comina prisão? entra nas estatísticas de alcance?)
  - resultado_morte : bool (qualificado pelo resultado morte -> art. 112, VI/VIII, LEP)
  - perdao_judicial_previsto : bool (há previsão legal expressa de perdão judicial?)
  - chave_dispositivo / duplicata : rastreiam registros repetidos

Impõe também as convenções do catálogo (ver CONTRIBUTING.md, C1 a C3): só tipos
penais, toda sanção declarada e `id` append-only. Violá-las falha o build.

Todos os campos derivados são heurísticos (regex sobre `crime`/`obs`/`artigo`) e
serão revisados individualmente. Correções finas ficam nas tabelas CORRECOES_*.

O arquivo de saída (static/data/crimes.json) é o único consumido pela aplicação;
data/crimes.json é a FONTE editável à mão (inclusive pela interface web do
GitHub) e regenerada pelo workflow .github/workflows/regen-data.yml.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "crimes.json"
OUT = ROOT / "static" / "data" / "crimes.json"
RELATORIO = ROOT / "static" / "data" / "qualidade.json"

PENA_PRIVATIVA_MAP = {
    "Reclusão": "Reclusão",
    "Detenção": "Detenção",
    "Prisão simples": "Prisão simples",
    "Multa": "Nenhuma",
    "—": "Nenhuma",
    "": "Nenhuma",
    None: "Nenhuma",
}

# padrões negativos que NÃO indicam pena de multa criminal
NEG_MULTA = re.compile(r"sem multa|multa reparat|reparação do dano", re.IGNORECASE)

# Correções manuais (revisão do usuário). Sobrepõem a heurística e retiram o
# registro da lista de casos ambíguos.
CORRECOES = {
    # Art. 227 CP (caput): a multa só incide na hipótese do §3º (fim de lucro);
    # o tipo-base não comina multa.
    176: {"tem_multa": False, "multa_regime": "nenhuma"},
    898: {"tem_multa": False, "multa_regime": "nenhuma"},
}

# ── O catálogo contém APENAS tipos penais ───────────────────────────────────
# Regra estrutural: cada registro é um tipo penal. Não entram notas de
# referência, agravantes, causas de aumento, excludentes de ilicitude nem regras
# de ação penal — todos foram removidos na v1.1.0. Com pena zero, eles
# satisfaziam qualquer teto de pena e eram contados como "cabíveis" em transação
# penal, ANPP e sursis.
#
# A regra é IMPOSTA aqui (e não apenas sinalizada) para que as atualizações
# automáticas da v2.0.0 não a violem: ver docs/catalogo-tipos-penais.md.
NAO_TIPIFICA = re.compile(r"REFER[ÊE]NCIA|EXCLUDENTE", re.IGNORECASE)

# ── Resultado morte (art. 112, VI e VIII, LEP; art. 122, §2º, LEP) ──────────
# Casa apenas contra o NOME do tipo, nunca contra `obs`: o campo obs costuma
# descrever a pena de OUTROS parágrafos do mesmo artigo ("se resulta morte,
# triplica"), o que produziria falsos positivos — p.ex. Art. 135 (omissão de
# socorro), Art. 267 (epidemia dolosa) e Art. 270 (envenenamento), cujos caputs
# não são qualificados pela morte.
RESULTADO_MORTE = re.compile(
    r"\bmortes?\b|latroc[íi]nio|homic[íi]dio|feminic[íi]dio|infantic[íi]dio|genoc[íi]dio",
    re.IGNORECASE,
)

# Exceções à regra acima, por id. Revisão manual.
CORRECOES_MORTE = {
    # Art. 158, §3º, CP: o dispositivo remete às penas do art. 159, §§2º e 3º,
    # cobrindo TANTO lesão grave QUANTO morte no mesmo registro. Não é possível
    # afirmar o resultado morte a partir deste registro — fica em revisão.
    # (mantido False; ver relatório de qualidade)
}

# ── Perdão judicial (art. 107, IX, CP) ──────────────────────────────────────
# NÃO existe perdão judicial genérico: só incide onde a lei o prevê
# expressamente, e não se estende por analogia (daí a lista ser curada, e não
# inferida do elemento culposo). O benefício é atribuído ao CRIME que o admite,
# não apenas ao parágrafo que o institui: o perdão do art. 121, §5º alcança o
# homicídio culposo do §3º.
#
# `^CP$` é ancorado de propósito: `^CP` casaria também "CPM (DL 1.001/69)",
# atribuindo perdão judicial à ofensa aviltante a inferior (art. 176 do CPM).
# Cada regra é (regex da lei, regex do artigo, exige_culposo). `exige_culposo`
# filtra os dispositivos cujo perdão a lei restringe à modalidade culposa: o
# art. 121, §4º tem uma 1ª parte culposa e uma 2ª parte DOLOSA (aumento contra
# menor de 14), e só a primeira admite o perdão do §5º.
_CP = r"^CP( \(atualiz\.\))?$"
PERDAO_JUDICIAL = [
    (_CP, r"^Art\. 121, §[345]º", True),      # homicídio culposo (§3º/§4º) e o perdão (§5º)
    (_CP, r"^Art\. 129, §(5|6|7|11)º?", True),  # lesão corporal culposa e o perdão
    (_CP, r"^Art\. 180, §3º", True),          # receptação culposa (perdão no §5º)
    (_CP, r"^Art\. 168-A", False),            # apropriação indébita previdenciária (§3º)
    (_CP, r"^Art\. 337-A", False),            # sonegação de contribuição previdenciária (§2º)
    (_CP, r"^Art\. 242", False),              # parto suposto (par. único — motivo de nobreza)
    (_CP, r"^Art\. 249", False),              # subtração de incapazes (§2º)
    (r"9\.807", r"^Art\. 13", False),         # proteção a vítimas e testemunhas — colaborador
    (r"12\.850", r"^Art\. 4º", False),        # colaboração premiada
]

# Hipóteses legais de perdão judicial AUSENTES do catálogo de tipos penais.
# Não são inventadas aqui: entram no relatório de qualidade como lacuna.
PERDAO_JUDICIAL_SEM_TIPO = [
    "CP, Art. 140, §1º — injúria (retorsão imediata / provocação reprovável)",
    "CP, Art. 176, par. único — outras fraudes",
    "CP, Art. 218-B, §2º, II — favorecimento da prostituição (cliente)",
    "CTB, Art. 291 c/c CP 121, §5º — homicídio culposo na direção (perdão admitido pelo STJ)",
]


def _casa(regra, c: dict) -> bool:
    lei_re, art_re, exige_culposo = regra
    if not re.search(lei_re, c.get("lei") or "", re.I):
        return False
    if not re.search(art_re, c.get("artigo") or "", re.I):
        return False
    if exige_culposo and c.get("elemento") != "Culposo":
        return False
    return True


def validar_tipos_penais(crimes: list) -> list:
    """Invariante DURO: todo registro é um tipo penal com sanção cominada.

    Um registro sem pena privativa E sem sanções próprias (ex.: uma nota de
    referência) não é um tipo penal: com pena zero ele satisfaria qualquer teto e
    contaminaria as estatísticas de alcance dos benefícios.

    A exceção legítima é o tipo penal cujas sanções não são privativas de
    liberdade — art. 28 da Lei 11.343/06 —, que declara `sancoes_nao_privativas`.
    """
    problemas = []
    for c in crimes:
        nome = c.get("crime") or ""
        if NAO_TIPIFICA.search(nome):
            problemas.append(
                f"id={c.get('id')} ({c.get('lei')} {c.get('artigo')}): "
                f"não é tipo penal — {nome[:60]}"
            )
            continue
        tem_pena = bool(c.get("pena_max") or c.get("pena_min"))
        tem_sancao = bool(c.get("sancoes_nao_privativas"))
        if not tem_pena and not tem_sancao:
            problemas.append(
                f"id={c.get('id')} ({c.get('lei')} {c.get('artigo')}): sem pena cominada e sem "
                f"`sancoes_nao_privativas` — se for tipo penal, declare a sanção; se não for, remova"
            )
    return problemas


# ── Fonte oficial por diploma (planalto.gov.br) ─────────────────────────────
# Texto COMPILADO (com as alterações posteriores), nunca o original: é ele que
# vale para conferência. Usado no relatório de qualidade, para que cada
# contradição venha com o link de onde resolvê-la.
PLANALTO = {
    r"^CP( \(atualiz\.\))?$": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
    r"^CPM": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del1001compilado.htm",
    r"^LCP": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3688.htm",
    r"^CTB|9\.503": "https://www.planalto.gov.br/ccivil_03/leis/l9503compilado.htm",
    r"^CE |4\.737": "https://www.planalto.gov.br/ccivil_03/leis/l4737compilado.htm",
    r"^ECA|8\.069": "https://www.planalto.gov.br/ccivil_03/leis/l8069compilado.htm",
    r"11\.343": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11343compilado.htm",
    r"9\.455": "https://www.planalto.gov.br/ccivil_03/leis/l9455.htm",
    r"8\.072": "https://www.planalto.gov.br/ccivil_03/leis/l8072compilado.htm",
    r"10\.826": "https://www.planalto.gov.br/ccivil_03/leis/2003/l10.826compilado.htm",
    r"13\.869": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13869.htm",
    r"9\.605": "https://www.planalto.gov.br/ccivil_03/leis/l9605compilado.htm",
    r"12\.850": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850compilado.htm",
    r"8\.137": "https://www.planalto.gov.br/ccivil_03/leis/l8137compilado.htm",
}


def url_planalto(lei: str) -> str:
    """Link do texto compilado do diploma, ou busca no Planalto se desconhecido."""
    for padrao, url in PLANALTO.items():
        if re.search(padrao, lei or "", re.I):
            return url
    return f"https://www.planalto.gov.br/ccivil_03/ (buscar: {lei})"


def chave_dispositivo(c: dict) -> str:
    """Identidade do dispositivo, para detectar registros repetidos."""
    lei = re.sub(r"\s+", " ", (c.get("lei") or "")).strip().lower()
    art = re.sub(r"\s+", " ", (c.get("artigo") or "")).strip().lower()
    return f"{lei}|{art}"


# Palavras vazias que não ajudam a decidir se dois registros descrevem a MESMA
# conduta (aparecem em quase todo nome de tipo penal).
_VAZIAS = {
    "a", "ao", "aos", "as", "com", "contra", "da", "das", "de", "do", "dos", "e",
    "em", "na", "nas", "no", "nos", "o", "os", "ou", "para", "por", "que", "se",
    "sem", "um", "uma", "aumento", "qualificado", "qualificada", "majorado",
    "majorada", "art", "pena", "caput",
}


def _radical(p: str) -> str:
    """Radical grosseiro: os 5 primeiros caracteres, sem acento.

    Basta para casar as flexões que o catálogo usa para a MESMA conduta —
    "Inscrição fraudulenta de eleitor" × "Inscrever-se fraudulentamente como
    eleitor" viram {inscr, fraud, eleit} nos dois casos. Sem isso, a diferença
    entre substantivo e verbo seria lida como crime diferente.
    """
    sem_acento = p.translate(str.maketrans("áàâãäéèêëíìîïóòôõöúùûüç", "aaaaaeeeeiiiiooooouuuuc"))
    return sem_acento[:5]


def _termos(nome: str) -> set:
    palavras = re.findall(r"[a-zà-ú]{3,}", (nome or "").lower())
    return {_radical(p) for p in palavras if p not in _VAZIAS}


def mesma_conduta(a: dict, b: dict) -> bool:
    """Dois registros do mesmo dispositivo descrevem a mesma conduta?

    Compara o vocabulário dos nomes (Jaccard). Serve para separar dois defeitos
    de gravidade muito diferente:

    - nomes PARECIDOS + penas diferentes -> divergência de pena: um dos dois erra
      o quantum do mesmo crime;
    - nomes DIFERENTES -> divergência de IDENTIDADE: o catálogo afirma dois
      crimes distintos sob o mesmo dispositivo, ou seja, ao menos um registro
      está sob o rótulo errado. É o defeito mais grave, porque a pena "certa"
      pode estar atribuída ao artigo errado.

    Ex.: `LCP, Art. 32` aparece como "Disparar arma de fogo" e como "Dirigir sem
    habilitação" — não é divergência de pena, é rótulo trocado.

    Usa o coeficiente de SOBREPOSIÇÃO (interseção / menor conjunto), não Jaccard:
    é comum um registro trazer o nome curto ("Peculato culposo") e o outro uma
    paráfrase longa ("Peculato culposo — concorre culposamente para o crime de
    outrem"). Jaccard puniria a paráfrase (a união cresce) e acusaria identidade
    onde a conduta é a mesma.
    """
    ta, tb = _termos(a.get("crime")), _termos(b.get("crime"))
    if not ta or not tb:
        return True  # sem vocabulário útil: não afirmar divergência de identidade
    return (len(ta & tb) / min(len(ta), len(tb))) >= 0.5


def classificar_contradicao(grupo: list) -> str:
    """`identidade` | `hediondez` | `pena` — o tipo do defeito, do pior ao menor."""
    for i in range(len(grupo)):
        for j in range(i + 1, len(grupo)):
            if not mesma_conduta(grupo[i], grupo[j]):
                return "identidade"
    if len({g["hediondo"] for g in grupo}) > 1:
        return "hediondez"
    return "pena"


def validar_ids(crimes: list) -> list:
    """Invariantes DUROS do identificador. Nunca são débito tolerável.

    O `id` é a URL pública de cada tipo penal (`/pesquisa/tipos?tipo=N`) e o site
    está publicado. Ele é APPEND-ONLY: um id novo vai para o fim (max + 1) e um id
    existente jamais é reatribuído a outro dispositivo, sob pena de um link antigo
    passar a apontar para o crime errado — falha silenciosa e difícil de notar.

    Importa sobretudo a partir da v2.0.0, quando o crawler do DOU passa a propor
    inclusões automáticas no catálogo.
    """
    problemas = []
    ids = [c.get("id") for c in crimes]

    sem_id = [i for i, v in enumerate(ids) if v is None]
    if sem_id:
        problemas.append(f"{len(sem_id)} registro(s) sem `id` (posições {sem_id[:5]})")

    repetidos = sorted(i for i, n in Counter(ids).items() if n > 1 and i is not None)
    if repetidos:
        problemas.append(
            f"{len(repetidos)} `id` repetido(s): {repetidos[:10]} — cada id é uma URL pública"
        )

    nao_inteiros = [v for v in ids if v is not None and not isinstance(v, int)]
    if nao_inteiros:
        problemas.append(f"{len(nao_inteiros)} `id` não inteiro(s): {nao_inteiros[:5]}")

    return problemas


# ── Unidades de pena (dias / meses / anos) ──────────────────────────────────
# Fator de conversão para MESES (unidade canônica de cálculo). O CP conta o mês
# como 30 dias (Art. 11), então 1 dia = 1/30 mês e 1 ano = 12 meses.
UNIDADE_EM_MESES = {"dias": 1 / 30, "meses": 1.0, "anos": 12.0}
_NOMES_UNIDADE = {"dias": ("dia", "dias"), "meses": ("mês", "meses"), "anos": ("ano", "anos")}


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
        return int(m.group(1)), _norm_unidade(m.group(2)), int(m.group(3)), _norm_unidade(m.group(4))
    m = RANGE_1U.search(text)
    if m:
        u = _norm_unidade(m.group(3))
        return int(m.group(1)), u, int(m.group(2)), u
    m = ABBR.search(text)
    if m:
        return int(m.group(1)), _ABBR_U[m.group(2).lower()], int(m.group(3)), _ABBR_U[m.group(4).lower()]
    return None


def _rotulo_de_meses(meses: float) -> str:
    """Rótulo de fallback quando não há intervalo parseável (usa pena_* em meses)."""
    if meses <= 0:
        return "—"
    if meses < 1:
        return _rotulo(round(meses * 30), "dias")
    if float(meses).is_integer() and meses % 12 == 0:
        return _rotulo(int(meses // 12), "anos")
    return _rotulo(int(meses) if float(meses).is_integer() else round(meses, 1), "meses")


def derivar_pena(c: dict):
    """Define rótulos de exibição e valores canônicos em meses.

    Campos adicionados:
      pena_min_meses / pena_max_meses  -> float (unidade de cálculo)
      pena_min_rotulo / pena_max_rotulo -> str (exibição com unidade natural)
      pena_unidade_derivada -> bool (True se veio do parser do texto)
    """
    parsed = parse_pena_range(c.get("obs", ""))
    if parsed is not None:
        vmin, umin, vmax, umax = parsed
        c["pena_min_meses"] = _meses(vmin, umin)
        c["pena_max_meses"] = _meses(vmax, umax)
        c["pena_min_rotulo"] = _rotulo(vmin, umin)
        c["pena_max_rotulo"] = _rotulo(vmax, umax)
        c["pena_unidade_derivada"] = True
        if umin == umax:
            sing, plur = _NOMES_UNIDADE[umax]
            c["pena_faixa_rotulo"] = f"{vmin} a {vmax} {sing if vmax == 1 else plur}"
        else:
            c["pena_faixa_rotulo"] = f"{c['pena_min_rotulo']} a {c['pena_max_rotulo']}"
    else:
        mn = float(c.get("pena_min") or 0)
        mx = float(c.get("pena_max") or 0)
        c["pena_min_meses"] = round(mn, 4)
        c["pena_max_meses"] = round(mx, 4)
        c["pena_min_rotulo"] = _rotulo_de_meses(mn)
        c["pena_max_rotulo"] = _rotulo_de_meses(mx)
        c["pena_unidade_derivada"] = False
        if mx <= 0:
            c["pena_faixa_rotulo"] = "—"
        elif c["pena_min_rotulo"] == "—":
            c["pena_faixa_rotulo"] = f"até {c['pena_max_rotulo']}"
        else:
            c["pena_faixa_rotulo"] = f"{c['pena_min_rotulo']} a {c['pena_max_rotulo']}"


def detect_multa(obs: str, tipo_pena: str):
    """Retorna (tem_multa, regime, ambiguo, motivo)."""
    text = obs or ""
    low = text.lower()

    if tipo_pena == "Multa":
        return True, "isolada", False, ""

    has_word = "multa" in low
    if not has_word:
        return False, "nenhuma", False, ""

    ambiguo = False
    motivo = ""
    if NEG_MULTA.search(text):
        ambiguo = True
        motivo = "menção a multa possivelmente não-criminal (ex.: 'sem multa'/'multa reparatória')"

    # cumulativa: "e multa", "+ multa", ", multa", "dias-multa" (multa cumulada,
    # inclusive Lei 11.343/06: "reclusão + 500-1.500 dias-multa")
    if re.search(r"(?:\be\s+multa|\+[^.;]*multa|,\s*multa|e,?\s*multa|dias-multa)", low):
        return True, "cumulativa", ambiguo, motivo
    # alternativa: "ou multa"
    if re.search(r"\bou\s+multa", low):
        return True, "alternativa", ambiguo, motivo
    # menção genérica -> tratar como cumulativa mas marcar ambíguo
    ambiguo = True
    if not motivo:
        motivo = "menção a 'multa' sem conector claro (e/ou) — regime presumido"
    return True, "cumulativa", ambiguo, motivo


def main():
    crimes = json.loads(SRC.read_text(encoding="utf-8"))
    review_rows = []

    # Invariantes estruturais: falham sempre, independentemente de --estrito.
    problemas = validar_ids(crimes) + validar_tipos_penais(crimes)
    if problemas:
        for p in problemas:
            print(f"ERRO: {p}", file=sys.stderr)
        return 1

    for c in crimes:
        tipo = c.get("tipo_pena")
        c["pena_privativa"] = PENA_PRIVATIVA_MAP.get(tipo, "Nenhuma")
        tem_multa, regime, ambiguo, motivo = detect_multa(c.get("obs"), tipo)
        correcao = CORRECOES.get(c["id"])
        if correcao is not None:
            tem_multa = correcao["tem_multa"]
            regime = correcao["multa_regime"]
            ambiguo = False
            c["multa_revisado"] = True
        c["tem_multa"] = tem_multa
        c["multa_regime"] = regime
        c["derivado_auto"] = True

        derivar_pena(c)
        pmax = c["pena_max_meses"]
        c["infracao_menor_potencial"] = bool(pmax and pmax <= 24)

        # Todo registro é tipo penal (garantido por validar_tipos_penais). O que
        # varia é ter ou não pena PRIVATIVA: só quem tem entra nas estatísticas de
        # alcance dos benefícios, que se medem por patamar de pena.
        c["tem_pena_privativa"] = bool(pmax or c["pena_min_meses"])
        c.setdefault("sancoes_nao_privativas", [])
        if not c["tem_pena_privativa"]:
            c["pena_faixa_rotulo"] = "sem pena privativa"

        # Resultado morte — derivado do nome do tipo, sobreponível por revisão.
        morte = bool(RESULTADO_MORTE.search(c.get("crime") or ""))
        if c["id"] in CORRECOES_MORTE:
            morte = CORRECOES_MORTE[c["id"]]
            c["resultado_morte_revisado"] = True
        c["resultado_morte"] = morte
        c["resultado_morte_derivado"] = c["id"] not in CORRECOES_MORTE

        # Perdão judicial — só onde a lei prevê expressamente.
        c["perdao_judicial_previsto"] = any(_casa(p, c) for p in PERDAO_JUDICIAL)

        c["chave_dispositivo"] = chave_dispositivo(c)

        if ambiguo:
            review_rows.append(
                (c["id"], c["lei"], c["artigo"], c["crime"], regime, motivo, (c.get("obs") or "")[:120])
            )

    # ── Duplicatas ──────────────────────────────────────────────────────────
    # Mesmo dispositivo (lei + artigo) registrado mais de uma vez. Quando as
    # penas divergem entre as cópias, há uma CONTRADIÇÃO factual no catálogo:
    # não é possível saber qual está correta sem revisão jurídica do artigo.
    por_chave = defaultdict(list)
    for c in crimes:
        por_chave[c["chave_dispositivo"]].append(c)

    contraditorios = []
    for chave, grupo in por_chave.items():
        if len(grupo) == 1:
            continue
        penas = {(g["pena_min_meses"], g["pena_max_meses"]) for g in grupo}
        hedis = {g["hediondo"] for g in grupo}
        divergente = len(penas) > 1 or len(hedis) > 1
        tipo = classificar_contradicao(grupo) if divergente else ""
        for g in grupo:
            g["duplicata"] = True
            g["duplicata_divergente"] = divergente
            g["duplicata_tipo"] = tipo
            g["duplicata_ids"] = sorted(x["id"] for x in grupo if x["id"] != g["id"])
        if divergente:
            contraditorios.append(
                {
                    "chave": chave,
                    "tipo": tipo,
                    "ids": sorted(g["id"] for g in grupo),
                    "crimes": [g["crime"][:90] for g in grupo],
                    "fonte": url_planalto(grupo[0].get("lei")),
                    "crime": grupo[0]["crime"][:80],
                    "penas_meses": sorted(f"{a}-{b}" for a, b in penas),
                    "hediondo": sorted(hedis),
                }
            )
    for c in crimes:
        c.setdefault("duplicata", False)
        c.setdefault("duplicata_divergente", False)
        c.setdefault("duplicata_ids", [])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(crimes, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── Relatório de qualidade ──────────────────────────────────────────────
    com_pena = [c for c in crimes if c["tem_pena_privativa"]]
    relatorio = {
        "total_tipos_penais": len(crimes),
        "com_pena_privativa": len(com_pena),
        "sem_pena_privativa": len(crimes) - len(com_pena),
        "dispositivos_distintos": len(por_chave),
        "registros_duplicados": sum(1 for c in crimes if c["duplicata"]),
        "duplicatas_divergentes": len(contraditorios),
        "resultado_morte": sum(1 for c in crimes if c["resultado_morte"]),
        "perdao_judicial_previsto": sum(1 for c in crimes if c["perdao_judicial_previsto"]),
        "multa_ambigua": len(review_rows),
        "perdao_judicial_sem_tipo": PERDAO_JUDICIAL_SEM_TIPO,
        "contradicoes": sorted(contraditorios, key=lambda x: x["ids"][0]),
    }
    RELATORIO.write_text(json.dumps(relatorio, ensure_ascii=False, indent=1), encoding="utf-8")

    priv = Counter(c["pena_privativa"] for c in crimes)
    multa = Counter(c["multa_regime"] for c in crimes)
    print("pena_privativa:", dict(priv))
    print("multa_regime:", dict(multa))
    print("tem_multa=True:", sum(1 for c in crimes if c["tem_multa"]))
    print("ambiguos remanescentes:", len(review_rows))
    print("correções manuais aplicadas:", sum(1 for c in crimes if c.get("multa_revisado")))
    print()
    print(f"tipos penais ............ {relatorio['total_tipos_penais']}")
    print(f"  com pena privativa .... {relatorio['com_pena_privativa']}")
    print(f"  sem pena privativa .... {relatorio['sem_pena_privativa']} (fora das estatísticas de alcance)")
    print(f"dispositivos distintos .. {relatorio['dispositivos_distintos']}")
    print(f"  registros duplicados .. {relatorio['registros_duplicados']}")
    print(f"  com dados divergentes . {relatorio['duplicatas_divergentes']}  <-- contradições a revisar")
    print(f"resultado morte ......... {relatorio['resultado_morte']}")
    print(f"perdão judicial previsto  {relatorio['perdao_judicial_previsto']}")
    print("escrito em:", OUT)
    print("relatório em:", RELATORIO)

    # --estrito: usado pela CI para impedir a INTRODUÇÃO de novas contradições.
    if "--estrito" in sys.argv:
        limite = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--max-contradicoes=")), 0))
        if len(contraditorios) > limite:
            print(
                f"\nERRO: {len(contraditorios)} duplicatas divergentes (limite: {limite}).",
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
