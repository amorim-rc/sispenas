# -*- coding: utf-8 -*-
"""Converte um snapshot do Planalto em dispositivos estruturados (F2).

Entrada: HTML normalizado em UTF-8 por `baixar.py`. Saída: lista de
dispositivos — a unidade que o conferidor compara com as linhas do catálogo.

**Por que não usar a árvore HTML.** O acervo é HTML exportado do Word, com tags
cruzadas (`<b>` aberto fora do `<p>`, `</font>` sobrando). Qualquer parser de
árvore "conserta" isso remontando a hierarquia ao seu modo, e as fronteiras de
parágrafo saem erradas — o caput do art. 121, por exemplo, some dentro do bloco
anterior. Como o documento é essencialmente uma lista de parágrafos, fatiar o
HTML cru em `<p>`/`<br>` e limpar cada pedaço é mais fiel e mais simples.

**As três regras que a F0 levantou** e que este módulo implementa:

1. *Anotação mais recente vence.* Quando um dispositivo é alterado, o Planalto
   mantém a redação antiga logo acima da nova — e nem sempre riscada (o art.
   24-A da Lei Maria da Penha traz duas linhas "Pena" seguidas, sem `<strike>`).
   Datar cada versão pela anotação e ficar com a mais nova é o único critério
   que funciona em todos os casos.
2. *Artigo revogado perde o corpo.* Sobra só o cabeçalho e a anotação de
   revogação — daí `situacao="revogado"` sem preceito nem pena.
3. *A anotação é um link* cujo texto diz ação, norma e ano ("(Incluído pela Lei
   nº 15.384, de 2026)").
"""
from __future__ import annotations

import html as _html
import re
import unicodedata
from dataclasses import dataclass, field

# ── Fatiamento em parágrafos ────────────────────────────────────────────────
_TAG = re.compile(r"(?is)<[^>]+>")
_QUEBRA = re.compile(r"(?i)<p\b[^>]*>|<br\s*/?>|</p\s*>")
_LINK = re.compile(r"(?is)<a\b[^>]*>(.*?)</a>")


def _texto(bruto: str) -> str:
    """Texto limpo do trecho, com os acentos SEMPRE compostos (NFC).

    O acervo do Planalto escreve parte dos acentos como entidade separada — "i"
    seguido de `&#769;` (acento agudo combinante). Depois do unescape, "feminicídio"
    fica com dois caracteres onde o resto do mundo vê um, e toda expressão regular
    com letra acentuada deixa de casar **em silêncio**: "é aumentada" não é
    encontrado, "três" não é convertido em 3, "Redação dada" não é reconhecido
    como anotação. Normalizar aqui, uma vez, protege todo o pipeline.
    """
    limpo = re.sub(r"\s+", " ", _html.unescape(_TAG.sub(" ", bruto))).strip()
    return unicodedata.normalize("NFC", limpo)


@dataclass
class Paragrafo:
    texto: str
    anotacoes: list[str] = field(default_factory=list)


def paragrafos(documento: str) -> list[Paragrafo]:
    """Quebra o HTML em parágrafos com o texto limpo e as anotações do trecho."""
    saida: list[Paragrafo] = []
    for pedaco in _QUEBRA.split(documento):
        if not pedaco:
            continue
        texto = _texto(pedaco)
        if not texto:
            continue
        saida.append(Paragrafo(texto, [_texto(m) for m in _LINK.findall(pedaco)]))
    return saida


# ── Anotações ("(Incluído pela Lei nº X, de AAAA)") ─────────────────────────
ACOES = {
    "inclu": "incluido",
    "reda": "redacao",
    "revog": "revogado",
    "renumer": "renumerado",
    "vide": "vide",
    "vig": "vigencia",
    "produ": "producao_efeitos",
}
# Buscas separadas em vez de uma expressão só: com grupos opcionais aninhados, o
# motor acha um casamento curto e devolve norma/ano vazios mesmo quando estão
# lá. Três buscas simples são mais previsíveis — e mais fáceis de depurar.
_ACAO = re.compile(
    r"\(\s*(Inclu[^\s]*d[oa]|Reda[^\s]*o dada|Revogad[oa]|Renumerad[oa]|Vide|"
    r"Vig[^\s)]*ncia|Produ[^\s]*o de efeitos)", re.IGNORECASE)
_NORMA = re.compile(
    r"(Lei Complementar|Lei|Medida Provis[^\s]*ria|Decreto-Lei|Emenda Constitucional)"
    r"\s*n?[ºo°.\s]*\s*([\d][\d.]*)", re.IGNORECASE)
# O ano vem como "de 2024" ou embutido numa data ("de 24.5.1977"): pegar o
# último grupo de quatro dígitos do parêntese cobre as duas formas.
_ANO = re.compile(r"(\d{4})\D*$")

# Ações que datam uma VERSÃO do dispositivo. "Vide", "Vigência" e "Produção de
# efeitos" são remissões: não criam redação nova e não podem desempatar versões.
ACOES_DE_VERSAO = {"incluido", "redacao", "revogado", "renumerado"}


@dataclass
class Anotacao:
    acao: str
    norma: str | None
    ano: int | None
    texto: str


def ler_anotacao(texto: str) -> Anotacao | None:
    """Extrai a primeira anotação legislativa de um texto, se houver."""
    m = _ACAO.search(texto)
    if not m:
        return None
    bruta = m.group(1).lower()
    acao = next((v for k, v in ACOES.items() if bruta.startswith(k)), bruta)
    # Norma e ano são procurados no MESMO parêntese da ação, para não capturar
    # a lei citada no corpo do dispositivo.
    fim = texto.find(")", m.start())
    escopo = texto[m.start(): fim + 1 if fim > 0 else len(texto)]
    mn = _NORMA.search(escopo)
    ma = _ANO.search(escopo)
    norma = f"{mn.group(1)} nº {mn.group(2)}" if mn else None
    return Anotacao(acao, norma, int(ma.group(1)) if ma else None, escopo)


# ── Classificação dos parágrafos ────────────────────────────────────────────
# "Art. 121.", "Art 121 -", "Art. 121-A.", "Art. 359-M." — e também "Art . 37",
# com espaço antes do ponto: a Lei 6.766 escreve assim do art. 37 em diante, e
# sem aceitar essa forma o parser perdia 25 artigos, grudando as penas deles no
# último dispositivo reconhecido (foi assim que o art. 36-A, que trata de
# administração de imóveis, ganhou "pena" de detenção).
#
# O sufixo de letra é COLADO ao número, sem espaço, e pode repetir-se: o
# "Art. 359-M-B" do CP tem duas letras. Duas armadilhas resolvidas aqui:
#
# 1. **Sufixo depois do ordinal.** A Lei 7.716 escreve "Art. 2º-A"; o marcador
#    ordinal vem ANTES da letra. Sem aceitá-lo nessa ordem, o parser lia "Art. 2"
#    e devolvia "-A Injuriar alguém…" como corpo do art. 2º — foi por isso que a
#    majorante da injúria racial apareceu na auditoria como "art. 2º, parágrafo
#    único", identificador que a lei não tem.
# 2. **Sufixo duplo.** "Art. 359-M-B." virava "Art. 359-M" com corpo "B. Quando
#    os crimes…", isto é, a redução por contexto de multidão colada ao golpe de
#    Estado, que é outro crime.
#
# O sufixo NÃO admite espaço em volta do hífen, e é essa exigência que separa
# "Art. 2º-A" de "Art. 155 - A subtração…", em que o hífen é pontuação e o "A"
# é artigo definido.
# O marcador ordinal e a letra do sufixo ficam FORA do `re.I` — `(?-i:…)`. Com o
# `o` do ordinal insensível a caixa, "Art. 13 O disposto nesta lei…" perdia o
# artigo definido, e o texto começava em "disposto"; com a letra insensível, um
# hífen seguido de minúscula viraria sufixo. Só "Art" é que se lê em qualquer
# caixa.
_ARTIGO = re.compile(
    r"^Art\s*\.?\s*(\d+)\s*(?-i:[ºo°])?((?:[-–—](?-i:[A-Z]))*)\s*(?:[.\-–—º°]|\s)", re.I)
# "§ 1º", "§ 1o", "§ 2°", "§ 2º-D", "Parágrafo único".
_PAR_NUMERO = re.compile(r"^§\s*(\d+)\s*[ºo°]?", re.I)
_PAR_SUFIXO = re.compile(r"^(\s*)[-–—]\s?([A-Z])(?![a-zà-ÿ])")
_PROSA = re.compile(r"\s+[A-Za-zÀ-ÿ]")
_PAR_UNICO = re.compile(r"^Par[áa]grafo\s+[úu]nico", re.I)
_INCISO = re.compile(r"^([IVXLC]+)\s*[-–—]\s", re.I)
_ALINEA = re.compile(r"^([a-z])\)\s")
_PENA = re.compile(r"^Pena\b", re.I)
_VETADO = re.compile(r"\(VETADO\)", re.I)
# "(Revogado)" às vezes vem no TEXTO do parágrafo, não no link da anotação —
# caso do art. 67, § único da Lei 9.605, onde o link diz "Redação dada".
_REVOGADO_TXT = re.compile(r"\(Revogad[oa]\b", re.I)


def _norm_marcador(numero: str, sufixo: str | None) -> str:
    return f"§ {numero}º" + (f"-{sufixo}" if sufixo else "")


def ler_paragrafo(texto: str) -> tuple[str, str | None, int] | None:
    """"§ 2 o -A (Revogado…)" -> ("2", "A"); "§ 1º - A pena é…" -> ("1", None).

    A letra maiúscula depois do travessão é ambígua no acervo do Planalto: tanto
    marca parágrafo sufixado ("§ 2º-D", "§ 4º-A A pena é…") quanto abre a frase
    ("§ 1º - A pena é de reclusão, de dois a cinco anos:"). Distinguir por dois
    sinais, nesta ordem:

    1. **hífen colado ao ordinal** ("§ 4º-A") — é sufixo, sempre;
    2. hífen espaçado ("§ 2 o -A") — só é sufixo se o que vier depois NÃO for
       prosa: "(Revogado pela Lei…)", ".", ":" etc.

    Ler "A pena" como sufixo criava um "§ 1º-A" fantasma e fazia sumir do parse o
    § 1º de verdade — e, com ele, os registros do catálogo que apontavam para lá
    (arts. 148, 168 e 317 do CP, entre outros: dezesseis registros que a
    conferência simplesmente não alcançava).
    """
    m = _PAR_NUMERO.match(texto)
    if not m:
        return None
    resto = texto[m.end():]
    s = _PAR_SUFIXO.match(resto)
    if s:
        colado = s.group(1) == ""
        if colado or not _PROSA.match(resto[s.end():]):
            return m.group(1), s.group(2), m.end() + s.end()
    return m.group(1), None, m.end()


def _epigrafe(texto: str) -> str | None:
    """Nomen juris do artigo seguinte ("Homicídio simples", "Feminicídio").

    Heurística: linha curta, sem pontuação de fim de frase, uma vez removidas as
    anotações. O Planalto imprime a epígrafe no parágrafo anterior ao "Art.".
    """
    limpo = re.sub(r"\([^)]*\)", "", texto).strip()
    if 0 < len(limpo) <= 70 and not limpo.endswith((".", ":", ";")):
        return limpo
    return None


@dataclass
class Dispositivo:
    artigo: str                      # "121"
    sufixo: str | None               # "A" em 121-A
    marcador: str                    # "caput", "§ 1º", "parágrafo único"
    texto: str = ""
    pena_texto: str | None = None
    situacao: str = "vigente"        # vigente | revogado | vetado
    anotacao: Anotacao | None = None
    epigrafe: str | None = None
    vigencia_pendente: bool = False
    # Texto CITADO: o artigo só altera outro diploma, e o que vem embaixo dele é
    # a redação transcrita da lei alterada (ver `_marcar_citacoes`).
    citacao: bool = False
    # Quantos parágrafos separam o texto do dispositivo da linha "Pena". Um
    # preceito e sua sanção são vizinhos (1, ou 2 com uma anotação no meio);
    # distância grande é sinal de que a pena pertence a OUTRO dispositivo e o
    # cabeçalho dele não foi reconhecido.
    pena_distancia: int | None = None
    incisos: list[dict] = field(default_factory=list)
    # Versões coletadas antes de decidir qual vale (ver `_consolidar`).
    _versoes_situacao: list[tuple[int, str]] = field(default_factory=list)
    _versoes_texto: list[tuple[int, str, Anotacao | None]] = field(default_factory=list)
    _versoes_pena: list[tuple[int, str, Anotacao | None]] = field(default_factory=list)

    @property
    def rotulo_artigo(self) -> str:
        return f"Art. {self.artigo}" + (f"-{self.sufixo}" if self.sufixo else "")

    @property
    def chave(self) -> str:
        return f"{self.rotulo_artigo}|{self.marcador}"


def _distribuir_penas_por_inciso(d: Dispositivo) -> None:
    """Dispositivo que é só CHAPEAU: cada inciso traz a sua própria pena.

        Art. 157, § 3º  Se da violência resulta:
        I - lesão corporal grave, a pena é de reclusão de 7 a 18 anos, e multa;
        II - morte, a pena é de reclusão, de 24 a 30 anos, e multa.

    Antes, as duas linhas "Pena" caíam no § 3º e a de ORDEM MAIOR vencia: o
    parágrafo ficava com a pena do último inciso e a do primeiro sumia. Pior que
    silêncio — é leitura errada, e quem "corrigisse" o catálogo por ela trocaria
    a pena da lesão grave pela do latrocínio. Foi o que fez o conferidor acusar
    os arts. 400 e 408 do CPM, ambos corretos no catálogo.

    A regra de desempate é conservadora, porque o caso COMUM é o oposto: em
    "Constitui crime …: I - …; V - … / Pena - reclusão" (Lei 8.137, art. 1º) os
    incisos são modalidades da conduta e a pena única é do artigo. Só se
    distribui quando há DUAS OU MAIS penas atrás de incisos DIFERENTES.

    E a pena com anotação de ALTERAÇÃO fica de fora da conta, porque ela é a
    redação nova de uma pena que já estava ali — não o preceito próprio de um
    inciso. Sem essa ressalva o art. 1º da Lei 9.613 se parte em duas: o
    Planalto imprime a pena original depois do inciso VIII antigo e a redação
    da Lei 12.683 depois do "VIII - (revogado)", que é outro inciso na
    estrutura; as duas cominam a mesma coisa, e distribuí-las inventaria um
    segundo crime de lavagem. Mesmo caso no art. 4º da Lei 8.137.
    """
    def e_redacao_nova(anotacao) -> bool:
        return bool(anotacao and anotacao.acao in ("redacao", "renumerado"))

    # A ressalva vale para DECIDIR, não para mover: reconhecido o chapeau, a
    # redação nova de uma pena de inciso vai para o inciso dela como as outras.
    # Duas versões no mesmo inciso resolvem pela ordem — o Planalto imprime a
    # nova depois da antiga.
    if len({v[3] for v in d._versoes_pena
            if v[3] is not None and not e_redacao_nova(v[2])}) < 2:
        return
    for ordem, texto, anotacao, idx in sorted(d._versoes_pena, key=lambda v: v[0]):
        if idx is not None and idx < len(d.incisos):
            d.incisos[idx]["pena_texto"] = texto
    d._versoes_pena = [v for v in d._versoes_pena if v[3] is None]


def _consolidar(d: Dispositivo) -> None:
    """Escolhe a versão vigente de texto e pena: a de anotação mais recente.

    Empate (ou ausência de anotação) resolve pela ordem no documento — o
    Planalto imprime a redação nova depois da antiga. Um dispositivo sem
    anotação nenhuma tem uma versão só, e a regra é inócua.
    """
    def datavel(a: Anotacao | None) -> int:
        # Só anotação de alteração data uma versão; "Vide" não vale como data.
        return a.ano if (a and a.ano and a.acao in ACOES_DE_VERSAO) else 0

    def vigente(versoes):
        if not versoes:
            return None, None, None
        melhor = max(versoes, key=lambda v: (datavel(v[2]), v[0]))
        return melhor[1], melhor[2], melhor[0]

    # A situação também é posicional: vale o ÚLTIMO marcador do documento.
    # Revogação vem DEPOIS do texto antigo ("Art. 350 ... (Revogado pela...)");
    # veto derrubado vem ANTES do texto promulgado ("Art. 9º (VETADO)." seguido
    # do artigo em vigor, com "(Promulgação partes vetadas)"). Fixar a situação
    # no primeiro marcador daria o art. 9º da Lei de Abuso como vetado, e ele
    # está em pleno vigor.
    if d._versoes_situacao:
        d.situacao = max(d._versoes_situacao, key=lambda v: v[0])[1]

    texto, anot_texto, ordem_texto = vigente(d._versoes_texto)
    pena, anot_pena, ordem_pena = vigente(d._versoes_pena)
    if texto:
        d.texto = texto
    if pena:
        d.pena_texto = pena
    if ordem_pena is not None and ordem_texto is not None:
        d.pena_distancia = ordem_pena - ordem_texto
    # Preferir a anotação que descreve uma alteração à mera remissão.
    candidatas = [a for a in (anot_pena, anot_texto, d.anotacao) if a]
    d.anotacao = next((a for a in candidatas if a.acao in ACOES_DE_VERSAO),
                      candidatas[0] if candidatas else None)


# "O art. 129 do Decreto-Lei nº 2.848 … passa a vigorar com as seguintes
# alterações:" — o artigo não cria nada: transcreve a redação que dá a OUTRA lei.
_ALTERA = re.compile(
    r"passa(?:m|r[áa])?\s+a\s+vigorar"
    r"|passa(?:m|r[áa])?\s+a\s+ter\s+a\s+seguinte\s+reda[çc]"
    r"|com\s+as\s+seguintes\s+altera[çc]"
    r"|fica(?:m)?\s+acresc(?:entad|id)", re.IGNORECASE)


def _marcar_citacoes(dispositivos: list[Dispositivo]) -> None:
    """Marca como citação tudo que pende de um artigo meramente alterador.

    Lição cara: a primeira leva de linhas novas (F6) criou nove "crimes" que não
    existem — a Lei de Abuso "contém" o art. 10 da Lei 9.296, a Lei 8.137
    "contém" o art. 172 do Código Penal, a Maria da Penha "contém" o art. 129,
    § 9º — porque o texto compilado transcreve, embaixo do artigo alterador, a
    redação dada à lei alterada. Pior: a transcrição congela a redação da época,
    então o "crime" duplicado nascia com a pena antiga.

    Duas formas de citação, e as duas apareceram naquela leva:

    1. **Pendurada no artigo alterador** — a redação transcrita vira "§" ou
       "parágrafo único" dele (Maria da Penha, art. 44, § 9º = art. 129, § 9º do
       CP). Reconhecida pelo texto do caput.
    2. **Artigo transcrito por inteiro** — o cabeçalho citado é lido como artigo
       novo, e o número denuncia: na Lei 12.850 vem "Art. 24, Art. 288, Art. 25";
       na Lei de Migração, "Art. 115, Art. 232-A, Art. 116". Um número que
       DESTOA da sequência e é seguido pela continuação dela é transcrição.

    O dispositivo citado não some do parse (o relatório continua podendo
    mostrá-lo); fica marcado, e quem cria linha nova o ignora.
    """
    alteradores = {d.rotulo_artigo for d in dispositivos
                   if d.marcador == "caput" and _ALTERA.search(d.texto or "")}

    caputs = [d for d in dispositivos if d.marcador == "caput"]
    for i, d in enumerate(caputs[1:-1], start=1):
        anterior, seguinte = caputs[i - 1], caputs[i + 1]
        try:
            n, ant, seg = (int(x.artigo) for x in (d, anterior, seguinte))
        except (TypeError, ValueError):
            continue
        if ant < seg < n:
            alteradores.add(d.rotulo_artigo)

    for d in dispositivos:
        if d.rotulo_artigo in alteradores:
            d.citacao = True


def _revogado_por_link(p: Paragrafo) -> bool:
    """A revogação veio como LINK no próprio parágrafo do dispositivo?

    Nem todo artigo revogado perde o corpo. As contravenções revogadas em lugar
    (LCP, arts. 27, 39, 65 e 69) mantêm texto e pena, com "(Revogado pela Lei
    nº …)" no cabeçalho e, às vezes, também na linha da pena — e a regra do
    corpo curto não as via. Passaram a "crimes vigentes" no catálogo por isso.

    O link é o que dá segurança: uma revogação anotada NESTE parágrafo é sobre
    ESTE dispositivo, enquanto a mesma frase solta no texto pode ser remissão.
    """
    return any((a := ler_anotacao(x)) and a.acao == "revogado" for x in p.anotacoes)


def parsear(documento: str) -> list[Dispositivo]:
    """HTML de um diploma -> dispositivos (caput e parágrafos) com pena e estado."""
    dispositivos: list[Dispositivo] = []
    por_chave: dict[str, Dispositivo] = {}
    artigo = sufixo = None
    marcador = "caput"
    epigrafe_pendente: str | None = None
    atual: Dispositivo | None = None
    # Índice do último inciso/alínea lido dentro do dispositivo corrente. Uma
    # linha "Pena" que vem DEPOIS de um inciso pode pertencer a ele — ver
    # `_distribuir_penas_por_inciso`.
    inciso_atual: int | None = None

    def obter(art, suf, marc) -> Dispositivo:
        nonlocal atual
        chave = f"Art. {art}" + (f"-{suf}" if suf else "") + f"|{marc}"
        d = por_chave.get(chave)
        if d is None:
            d = Dispositivo(art, suf, marc)
            por_chave[chave] = d
            dispositivos.append(d)
        atual = d
        return d

    for ordem, p in enumerate(paragrafos(documento)):
        texto = p.texto
        anotacao = ler_anotacao(" ".join(p.anotacoes) or texto)
        # "Vigência"/"Produção de efeitos" marcam alteração ainda não aplicável.
        pendente = any(
            (a := ler_anotacao(x)) and a.acao in ("vigencia", "producao_efeitos")
            for x in p.anotacoes
        )

        m = _ARTIGO.match(texto)
        if m:
            # group(2) vem com os hífens ("-M-B"); a chave usa "359-M-B".
            artigo = m.group(1)
            sufixo = re.sub(r"[–—]", "-", m.group(2)).strip("-").upper() or None
            marcador = "caput"
            inciso_atual = None
            d = obter(artigo, sufixo, marcador)
            d.epigrafe = d.epigrafe or epigrafe_pendente
            epigrafe_pendente = None
            corpo = texto[m.end():].strip()
            corpo_util = re.sub(r"\([^)]*\)", "", corpo).strip()
            revogado = (_revogado_por_link(p)
                        or ((_REVOGADO_TXT.search(texto)
                             or (anotacao and anotacao.acao == "revogado"))
                            and len(corpo_util) < 80))
            # O "(VETADO)" de um parágrafo não veta o artigo inteiro: só marca
            # quando o próprio dispositivo ficou sem corpo (art. 9º da Lei de
            # Abuso tem § vetado e caput em pleno vigor).
            #
            # E é ALTERNATIVO a "vigente", não somado a ele. Somados, os dois
            # marcadores nasciam com a MESMA `ordem`, o desempate de `max` fica
            # com o primeiro, e o genérico vencia o específico: o art. 359-O do
            # CP — comunicação enganosa em massa, vetado na Lei 14.197/2021 —
            # saía como vigente, e o catálogo publicou por meses um crime que
            # não existe. O veto DERRUBADO continua funcionando, porque ali os
            # dois marcadores estão em parágrafos diferentes e o posterior vence.
            vetado = bool(_VETADO.search(texto)) and len(corpo_util) < 40
            if revogado:
                # Artigo revogado perde o corpo: sobra o cabeçalho + a anotação.
                d._versoes_situacao.append((ordem, "revogado"))
                d.anotacao = anotacao
            elif vetado:
                d._versoes_situacao.append((ordem, "vetado"))
                d.anotacao = anotacao
            else:
                d._versoes_situacao.append((ordem, "vigente"))
                d._versoes_texto.append((ordem, corpo, anotacao))
            d.vigencia_pendente = d.vigencia_pendente or pendente
            continue

        if artigo is None:
            # Ainda no preâmbulo/ementa — mas a epígrafe do PRIMEIRO artigo
            # aparece aqui, e seria perdida se simplesmente pulássemos.
            epigrafe_pendente = _epigrafe(texto) or epigrafe_pendente
            continue

        mp = ler_paragrafo(texto)
        if mp or _PAR_UNICO.match(texto):
            marcador = (_norm_marcador(mp[0], mp[1]) if mp else "parágrafo único")
            inciso_atual = None
            d = obter(artigo, sufixo, marcador)
            corpo = texto[(mp[2] if mp else _PAR_UNICO.match(texto).end()):].strip(" .-–—")
            corpo_util = re.sub(r"\([^)]*\)", "", corpo).strip()
            revogado = (_revogado_por_link(p)
                        or ((_REVOGADO_TXT.search(texto)
                             or (anotacao and anotacao.acao == "revogado"))
                            and len(corpo_util) < 80))
            if revogado:
                d._versoes_situacao.append((ordem, "revogado"))
                d.anotacao = anotacao
            else:
                d._versoes_situacao.append((ordem, "vigente"))
                d._versoes_texto.append((ordem, corpo, anotacao))
            # O "(VETADO)" de um parágrafo não veta o artigo inteiro: só marca
            # quando o próprio dispositivo ficou sem corpo (art. 9º da Lei de
            # Abuso tem § vetado e caput em pleno vigor).
            if _VETADO.search(texto) and len(corpo_util) < 40:
                d._versoes_situacao.append((ordem, "vetado"))
            d.vigencia_pendente = d.vigencia_pendente or pendente
            continue

        if _PENA.match(texto) and atual is not None:
            atual._versoes_pena.append((ordem, texto, anotacao, inciso_atual))
            atual.vigencia_pendente = atual.vigencia_pendente or pendente
            continue

        mi = _INCISO.match(texto) or _ALINEA.match(texto)
        if mi and atual is not None:
            atual.incisos.append({
                "marcador": mi.group(1),
                "texto": texto[mi.end():].strip(),
                "situacao": "revogado" if anotacao and anotacao.acao == "revogado" else "vigente",
                "anotacao": anotacao.texto if anotacao else None,
                "pena_texto": None,
            })
            inciso_atual = len(atual.incisos) - 1
            continue

        epigrafe_pendente = _epigrafe(texto) or epigrafe_pendente

    for d in dispositivos:
        _distribuir_penas_por_inciso(d)
        _consolidar(d)
    _marcar_citacoes(dispositivos)
    return dispositivos


def como_dicionarios(dispositivos: list[Dispositivo]) -> list[dict]:
    """Serialização estável para o relatório e para os testes."""
    return [{
        "artigo": d.rotulo_artigo,
        "marcador": d.marcador,
        "situacao": d.situacao,
        "epigrafe": d.epigrafe,
        "texto": d.texto,
        "pena_texto": d.pena_texto,
        "anotacao": (None if not d.anotacao else
                     {"acao": d.anotacao.acao, "norma": d.anotacao.norma,
                      "ano": d.anotacao.ano}),
        "vigencia_pendente": d.vigencia_pendente,
        "citacao": d.citacao,
        "incisos": d.incisos,
    } for d in dispositivos]
