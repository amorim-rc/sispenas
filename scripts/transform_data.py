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
APOSENTADOS = ROOT / "data" / "ids-aposentados.json"
CONFERENCIA = ROOT / "data" / "conferencia.json"
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
    167: {"tem_multa": False, "multa_regime": "nenhuma"},
    898: {"tem_multa": False, "multa_regime": "nenhuma"},
    # Art. 310 do Código Eleitoral: "detenção até seis meses OU pagamento de 90 a
    # 120 dias-multa". A cominação é alternativa, mas a heurística lê "dias-multa"
    # antes de "ou" e conclui cumulativa. A diferença não é de rótulo: com multa
    # alternativa, a multa isolada basta para punir o fato.
    792: {"tem_multa": True, "multa_regime": "alternativa"},
    # Dois registros cujo `obs` EXPLICA que o artigo não comina multa. A palavra
    # está lá — a heurística só sabe procurá-la, não negá-la. Art. 338 do CP
    # ("reclusão, de um a quatro anos, sem prejuízo de nova expulsão") e art. 72
    # da Lei 9.504/97 ("puníveis com reclusão, de cinco a dez anos"): a multa que
    # os dois publicavam veio junto com o nome importado de outro artigo.
    750: {"tem_multa": False, "multa_regime": "nenhuma"},
    537: {"tem_multa": False, "multa_regime": "nenhuma"},
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
    #
    # Vicaricídio (art. 121-B, incluído pela Lei 15.384/2026): é homicídio, mas
    # o nomen juris não contém "homicídio" nem "morte", e a heurística deriva do
    # NOME. Sem estas linhas o crime deixaria de constar como resultado morte —
    # com efeito direto sobre livramento condicional e progressão.
    1318: True,
    1319: True,
    1320: True,
    1321: True,
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
    (_CP, r"^Art\. 140, caput", False),       # injúria simples (§1º: provocação reprovável / retorsão) — não alcança a injúria racial do §3º
    (_CP, r"^Art\. 176$", False),             # outras fraudes (par. único)
    (r"9\.807", r"^Art\. 13", False),         # proteção a vítimas e testemunhas — colaborador
    (r"12\.850", r"^Art\. 4º", False),        # colaboração premiada
]

# Hipóteses legais de perdão judicial AUSENTES do catálogo de tipos penais.
# Não são inventadas aqui: entram no relatório de qualidade como lacuna.
# Perdão judicial de base JURISPRUDENCIAL (não expresso em lei) — fica de fora da lista
# curada, que é só de hipóteses legais expressas, mas registrado como nota.
PERDAO_JUDICIAL_SEM_TIPO = [
    "CP, Art. 218-B, §2º, II — favorecimento da prostituição (cliente): hipótese sem tipo próprio no catálogo",
    "CTB, Art. 302/303 — homicídio/lesão culposa na direção: perdão admitido pelo STJ por ANALOGIA ao CP 121, §5º, não por previsão expressa; por isso não é marcado no campo",
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


def validar_moldura(crimes: list) -> list:
    """A moldura é a AUTORIDADE — e por isso tem de estar bem escrita.

    Desde a v1.2.17 é `pena_min`/`pena_max` que define a pena publicada; o `obs`
    voltou a ser descritivo. Duas exigências, verificadas a cada build:

    1. **Inteiro quando inteiro.** `24.0` e `24` valem o mesmo para o cálculo,
       mas o primeiro polui o diff e muda o tipo no JSON público. A regra vale
       para todo mundo — quem edita à mão e quem gera correção automática.
    2. **Mínimo não pode passar do máximo.**
    """
    problemas = []
    for c in crimes:
        for campo in ("pena_min", "pena_max"):
            v = c.get(campo)
            if isinstance(v, float) and float(v).is_integer():
                problemas.append(
                    f"id {c.get('id')}: {campo}={v!r} deve ser inteiro ({int(v)})")
            if v is not None and not isinstance(v, (int, float)):
                problemas.append(f"id {c.get('id')}: {campo}={v!r} não é número")
        mn, mx = float(c.get("pena_min") or 0), float(c.get("pena_max") or 0)
        if mn > mx:
            problemas.append(f"id {c.get('id')}: pena_min {mn} maior que pena_max {mx}")
    return problemas


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
        # Tipo que comina SÓ multa (multa isolada) é sanção válida — ex.: o caput
        # do art. 146-A (bullying), "Pena: multa, se não constitui crime mais grave".
        tem_multa_isolada = c.get("tipo_pena") == "Multa"
        if not tem_pena and not tem_sancao and not tem_multa_isolada:
            problemas.append(
                f"id={c.get('id')} ({c.get('lei')} {c.get('artigo')}): sem pena cominada, sem "
                f"`sancoes_nao_privativas` e sem multa — se for tipo penal, declare a sanção; se não, remova"
            )
    return problemas


# ── Fonte oficial por diploma (planalto.gov.br) ─────────────────────────────
# Texto COMPILADO (com as alterações posteriores), nunca o original: é ele que
# vale para conferência. Usado no relatório de qualidade, para que cada
# contradição venha com o link de onde resolvê-la.
#
# O registro vive em `data/fontes.json` — mesma fonte que o conferidor usa para
# baixar os textos (scripts/crawler/baixar.py). Antes o mapa era duplicado aqui,
# por expressão regular, e envelheceu: quatro diplomas apontavam para URLs
# "…compilado.htm" que hoje respondem 404. Uma fonte só, casada por rótulo
# exato, elimina a duplicação e mantém os links verificados pelo download.
def _carregar_fontes() -> dict:
    caminho = ROOT / "data" / "fontes.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    return {rotulo: f["url"] for f in dados["fontes"] for rotulo in f["rotulos"]}


PLANALTO = _carregar_fontes()


def url_planalto(lei: str) -> str:
    """Link do texto compilado do diploma, ou busca no Planalto se desconhecido."""
    url = PLANALTO.get((lei or "").strip())
    if url:
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


def validar_vigencia(crimes: list) -> list:
    """Dispositivo que deixou de vigorar precisa dizer O QUE ACONTECEU.

    `vigencia_ate` sozinho é pior que nada: o registro sai do ar sem explicar por
    quê, e quem consulta um fato anterior não sabe se ainda pode se apoiar nele.
    A nota tem de trazer o motivo e, quando houver, o dispositivo que passa a
    reger a conduta.
    """
    problemas = []
    for c in crimes:
        ate = c.get("vigencia_ate")
        if ate and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(ate)):
            problemas.append(
                f"id {c['id']}: `vigencia_ate` = {ate!r} não é uma data AAAA-MM-DD")
        if ate and not (c.get("vigencia_nota") or "").strip():
            problemas.append(
                f"id {c['id']}: declara `vigencia_ate` sem `vigencia_nota` — um "
                "registro que deixou de vigorar tem de dizer o que houve e qual "
                "dispositivo passa a reger a conduta")
        if c.get("vigencia_nota") and not ate:
            problemas.append(
                f"id {c['id']}: tem `vigencia_nota` sem `vigencia_ate` — se o "
                "dispositivo continua vigente, a nota é `obs`")
    return problemas


def validar_condicionais(crimes: list) -> list:
    """Classificação circunstanciada não pode ser afirmada como se fosse do tipo.

    Um registro que declara `hediondo_condicao` está dizendo "depende do caso" —
    e marcar `hediondo: "Sim"` ao lado disso afirmaria o que a lei não afirma,
    além de ligar sozinho as vedações do art. 5º, XLIII, da Constituição.
    """
    problemas = []
    for c in crimes:
        if c.get("hediondo_condicao") and c.get("hediondo") == "Sim":
            problemas.append(
                f"id {c['id']}: declara `hediondo_condicao` e ainda assim marca "
                "`hediondo: Sim` — a condição existe justamente porque o tipo, "
                "sozinho, não decide")
    return problemas


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

    # id APOSENTADO nunca volta. A regra "próximo id = max + 1" tem um furo: se
    # a remoção foi no topo da numeração, o max cai e o id seguinte reaproveita
    # um endereço que já significou outro crime. Aconteceu na v1.4.0, quando 15
    # ids do fim saíram de uma vez.
    reusados = sorted(set(ids) & ids_aposentados())
    if reusados:
        problemas.append(
            f"{len(reusados)} `id` reaproveitado(s) de registro já retirado: "
            f"{reusados[:10]} — ver data/ids-aposentados.json")

    return problemas


def ids_aposentados() -> set[int]:
    """ids que já foram URL pública e saíram do catálogo (data/ids-aposentados.json)."""
    if not APOSENTADOS.exists():
        return set()
    registro = json.loads(APOSENTADOS.read_text(encoding="utf-8"))
    return {i for grupo in registro.get("aposentados", []) for i in grupo["ids"]}


def proximo_id(crimes: list) -> int:
    """O próximo id livre: acima de tudo que existe E de tudo que já existiu."""
    return max({c["id"] for c in crimes if isinstance(c.get("id"), int)}
               | ids_aposentados()) + 1


# ── Unidades e leitura de pena ──────────────────────────────────────────────
# Extraídas para `scripts/pena_parser.py` (F3 do conferidor): o catálogo e o
# conferidor precisam ler a MESMA moldura do MESMO jeito — duas implementações
# discordando produziriam divergência falsa no relatório semanal.
from pena_parser import (  # noqa: E402
    UNIDADE_EM_MESES, _NOMES_UNIDADE, _norm_unidade, _rotulo, _meses,
    RANGE_2U, RANGE_1U, ABBR, _ABBR_U, parse_pena_range,
)


def _ponta(meses: float) -> tuple[str, float | None, str | None]:
    """(rótulo, valor, unidade) de uma ponta da moldura, a partir dos MESES.

    A unidade volta como None quando a pena é composta ("26 anos e 8 meses"):
    nesse caso não há como compactar o intervalo, e cada ponta se escreve por
    inteiro. Causas de aumento produzem molduras assim (20 anos com um terço
    são 320 meses).

    Dias: o mês do art. 11 do CP tem 30 dias, então `meses * 30` devolve o
    número exato — 0,3333 mês são 10 dias, 0,5 são 15. A ida e volta é exata
    para todo valor de 1 a 29 dias (ver os testes do conferidor).
    """
    if meses <= 0:
        return "—", None, None
    if meses < 1:
        dias = round(meses * 30)
        return _rotulo(dias, "dias"), dias, "dias"
    if float(meses).is_integer() and meses % 12 == 0:
        anos = int(meses // 12)
        return _rotulo(anos, "anos"), anos, "anos"
    if float(meses).is_integer() and meses >= 24:
        anos, resto = divmod(int(meses), 12)
        return f"{_rotulo(anos, 'anos')} e {_rotulo(resto, 'meses')}", None, None
    valor = int(meses) if float(meses).is_integer() else round(meses, 1)
    return _rotulo(valor, "meses"), valor, "meses"


def _rotulo_de_meses(meses: float) -> str:
    return _ponta(meses)[0]


def _faixa_de_meses(minimo: float, maximo: float) -> str:
    """Intervalo por extenso: "2 a 5 anos", "15 dias a 3 meses", "até 6 meses"."""
    rot_min, v_min, u_min = _ponta(minimo)
    rot_max, v_max, u_max = _ponta(maximo)
    if maximo <= 0:
        return "—"
    if minimo <= 0:
        return f"até {rot_max}"
    if minimo == maximo:
        return rot_max          # pena fixa: "1 ano", não "1 a 1 ano"
    if u_min is not None and u_min == u_max:
        sing, plur = _NOMES_UNIDADE[u_max]
        return f"{v_min} a {v_max} {sing if v_max == 1 else plur}"
    return f"{rot_min} a {rot_max}"


def derivar_pena(c: dict):
    """Rótulos de exibição a partir da moldura em meses.

    **`pena_min`/`pena_max` são a autoridade.** Até a v1.2.16 a moldura era
    extraída do TEXTO do `obs` por expressão regular, e o número só valia como
    reserva — o que fazia uma frase secundária mudar a pena publicada: o art.
    32, §1º-A da Lei 9.605 exibia "3 meses a 1 ano" porque o `obs` mencionava a
    pena antiga. Invertida a ordem, o `obs` voltou a ser o que o nome diz.

    Campos acrescentados:
      pena_min_meses / pena_max_meses  -> float (unidade de cálculo)
      pena_min_rotulo / pena_max_rotulo -> str (exibição com unidade natural)
      pena_faixa_rotulo -> str (o intervalo como se lê)
    """
    mn = float(c.get("pena_min") or 0)
    mx = float(c.get("pena_max") or 0)
    c["pena_min_meses"] = round(mn, 4)
    c["pena_max_meses"] = round(mx, 4)
    c["pena_min_rotulo"] = _rotulo_de_meses(mn)
    c["pena_max_rotulo"] = _rotulo_de_meses(mx)
    c["pena_faixa_rotulo"] = _faixa_de_meses(mn, mx)


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


def carregar_trilha() -> dict:
    """Trilha de auditoria da última rodada do conferidor, se houver.

    Ausente num clone que ainda não rodou o conferidor — nesse caso os campos
    saem nulos, e a aplicação trata como "ainda não conferido". Nunca falha o
    build por causa disso: a trilha é informação SOBRE o dado, não o dado.
    """
    if not CONFERENCIA.exists():
        return {}
    return json.loads(CONFERENCIA.read_text(encoding="utf-8")).get("registros", {})


def main():
    crimes = json.loads(SRC.read_text(encoding="utf-8"))
    trilha = carregar_trilha()
    review_rows = []

    # Invariantes estruturais: falham sempre, independentemente de --estrito.
    problemas = (validar_ids(crimes) + validar_tipos_penais(crimes)
                 + validar_moldura(crimes) + validar_condicionais(crimes)
                 + validar_vigencia(crimes))
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

        # Classificação CIRCUNSTANCIADA: a lei não decide pelo tipo. O art. 121
        # só é hediondo quando praticado em atividade de grupo de extermínio; a
        # ação do art. 161 só é privada se a propriedade for particular. Nesses,
        # o catálogo guarda a CONDIÇÃO e deixa o campo no padrão seguro — quem
        # marca é quem conhece o caso, na simulação.
        c["hediondo_condicional"] = bool(c.get("hediondo_condicao"))
        c["acao_condicional"] = bool(c.get("acao_condicao"))

        # VIGÊNCIA. Um dispositivo pode deixar de valer sem sair do catálogo:
        # declarado inconstitucional com eficácia ex nunc (CPM, art. 232, §3º —
        # ADI 7555) ou revogado. O registro CONTINUA consultável, porque os fatos
        # anteriores seguem regidos por ele; o que muda é que a aplicação passa a
        # dizê-lo. Excluir seria apagar a lei que valia quando o fato ocorreu.
        #
        # O derivado é a ausência do campo, não uma comparação com a data de
        # hoje: o arquivo derivado é commitado e conferido pela CI, e um campo
        # que muda sozinho num dia qualquer quebraria o build sem ninguém ter
        # tocado em nada. Vacatio legis é outro problema, do conferidor
        # (scripts/crawler/vigencia.py), e não se modela aqui.
        c["vigente"] = not c.get("vigencia_ate")

        # Trilha de auditoria: quando este registro foi confrontado com a lei,
        # com que resultado e contra qual página. Vem da última rodada do
        # conferidor (data/conferencia.json) — quem cita um dado precisa saber
        # de quando é a conferência, e não só que ela existe.
        auditoria = trilha.get(str(c["id"]))
        c["fonte"] = (auditoria or {}).get("fonte")
        c["conferido_em"] = (auditoria or {}).get("conferido_em")
        c["conferido_resultado"] = (auditoria or {}).get("resultado")

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
    # Condutas-base: dispositivos colapsados ao artigo-base (sem §/inciso/alínea/
    # caput). Cada tipo é uma moldura penal própria; a conduta-base agrupa as
    # formas (simples, qualificada, privilegiada) de um mesmo crime. A home usa
    # os dois números: "N condutas se desdobram em M tipos/molduras".
    def _base(c):
        m = re.match(r"(Art\.?\s*\d+(?:-[A-Z])?)", c["artigo"])
        return (c["lei"], m.group(1) if m else c["artigo"])
    relatorio = {
        "total_tipos_penais": len(crimes),
        "condutas_base": len({_base(c) for c in crimes}),
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
