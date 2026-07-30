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
from dataclasses import dataclass, field

# ── Fatiamento em parágrafos ────────────────────────────────────────────────
_TAG = re.compile(r"(?is)<[^>]+>")
_QUEBRA = re.compile(r"(?i)<p\b[^>]*>|<br\s*/?>|</p\s*>")
_LINK = re.compile(r"(?is)<a\b[^>]*>(.*?)</a>")


def _texto(bruto: str) -> str:
    return re.sub(r"\s+", " ", _html.unescape(_TAG.sub(" ", bruto))).strip()


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
# "Art. 121.", "Art 121 -", "Art. 121-A.", "Art. 359-M."
_ARTIGO = re.compile(r"^Art\.?\s*(\d+)(?:\s*[-–—]\s*([A-Z]))?\s*(?:[.\-–—º°]|\s)", re.I)
# "§ 1º", "§ 1o", "§ 2°", "§ 2º-D", "Parágrafo único".
# O sufixo só vale se a letra maiúscula estiver isolada: em "§ 5º - Na hipótese"
# o travessão introduz o texto, e capturar o "N" inventaria um "§ 5º-N".
_PARAGRAFO = re.compile(
    r"^§\s*(\d+)\s*[ºo°]?\s*(?:[-–—]\s*([A-Z])(?![a-zà-ÿ]))?", re.I)
_PAR_UNICO = re.compile(r"^Par[áa]grafo\s+[úu]nico", re.I)
_INCISO = re.compile(r"^([IVXLC]+)\s*[-–—]\s", re.I)
_ALINEA = re.compile(r"^([a-z])\)\s")
_PENA = re.compile(r"^Pena\b", re.I)
_VETADO = re.compile(r"\(VETADO\)", re.I)


def _norm_marcador(numero: str, sufixo: str | None) -> str:
    return f"§ {numero}º" + (f"-{sufixo}" if sufixo else "")


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
    incisos: list[dict] = field(default_factory=list)
    # Versões coletadas antes de decidir qual vale (ver `_consolidar`).
    _versoes_texto: list[tuple[int, str, Anotacao | None]] = field(default_factory=list)
    _versoes_pena: list[tuple[int, str, Anotacao | None]] = field(default_factory=list)

    @property
    def rotulo_artigo(self) -> str:
        return f"Art. {self.artigo}" + (f"-{self.sufixo}" if self.sufixo else "")

    @property
    def chave(self) -> str:
        return f"{self.rotulo_artigo}|{self.marcador}"


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
            return None, None
        melhor = max(versoes, key=lambda v: (datavel(v[2]), v[0]))
        return melhor[1], melhor[2]

    texto, anot_texto = vigente(d._versoes_texto)
    pena, anot_pena = vigente(d._versoes_pena)
    if texto:
        d.texto = texto
    if pena:
        d.pena_texto = pena
    # Preferir a anotação que descreve uma alteração à mera remissão.
    candidatas = [a for a in (anot_pena, anot_texto, d.anotacao) if a]
    d.anotacao = next((a for a in candidatas if a.acao in ACOES_DE_VERSAO),
                      candidatas[0] if candidatas else None)


def parsear(documento: str) -> list[Dispositivo]:
    """HTML de um diploma -> dispositivos (caput e parágrafos) com pena e estado."""
    dispositivos: list[Dispositivo] = []
    por_chave: dict[str, Dispositivo] = {}
    artigo = sufixo = None
    marcador = "caput"
    epigrafe_pendente: str | None = None
    atual: Dispositivo | None = None

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
            artigo, sufixo = m.group(1), m.group(2)
            marcador = "caput"
            d = obter(artigo, sufixo, marcador)
            d.epigrafe = d.epigrafe or epigrafe_pendente
            epigrafe_pendente = None
            corpo = texto[m.end():].strip()
            if anotacao and anotacao.acao == "revogado" and len(corpo) < 80:
                # Artigo revogado perde o corpo: sobra o cabeçalho + a anotação.
                d.situacao = "revogado"
                d.anotacao = anotacao
            else:
                d._versoes_texto.append((ordem, corpo, anotacao))
            if _VETADO.search(texto):
                d.situacao = "vetado"
            d.vigencia_pendente = d.vigencia_pendente or pendente
            continue

        if artigo is None:
            # Ainda no preâmbulo/ementa — mas a epígrafe do PRIMEIRO artigo
            # aparece aqui, e seria perdida se simplesmente pulássemos.
            epigrafe_pendente = _epigrafe(texto) or epigrafe_pendente
            continue

        mp = _PARAGRAFO.match(texto)
        if mp or _PAR_UNICO.match(texto):
            marcador = (_norm_marcador(mp.group(1), mp.group(2)) if mp
                        else "parágrafo único")
            d = obter(artigo, sufixo, marcador)
            corpo = texto[(mp.end() if mp else _PAR_UNICO.match(texto).end()):].strip(" .-–—")
            if anotacao and anotacao.acao == "revogado" and len(corpo) < 80:
                d.situacao = "revogado"
                d.anotacao = anotacao
            else:
                d._versoes_texto.append((ordem, corpo, anotacao))
            if _VETADO.search(texto):
                d.situacao = "vetado"
            d.vigencia_pendente = d.vigencia_pendente or pendente
            continue

        if _PENA.match(texto) and atual is not None:
            atual._versoes_pena.append((ordem, texto, anotacao))
            atual.vigencia_pendente = atual.vigencia_pendente or pendente
            continue

        mi = _INCISO.match(texto) or _ALINEA.match(texto)
        if mi and atual is not None:
            atual.incisos.append({
                "marcador": mi.group(1),
                "texto": texto[mi.end():].strip(),
                "situacao": "revogado" if anotacao and anotacao.acao == "revogado" else "vigente",
                "anotacao": anotacao.texto if anotacao else None,
            })
            continue

        epigrafe_pendente = _epigrafe(texto) or epigrafe_pendente

    for d in dispositivos:
        _consolidar(d)
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
        "incisos": d.incisos,
    } for d in dispositivos]
