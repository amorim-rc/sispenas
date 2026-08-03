# -*- coding: utf-8 -*-
"""Audita os campos que o conferidor de penas não alcança.

O conferidor responde "a pena publicada é a que a lei comina?". Sobram quatro
campos que decidem benefício e que ninguém vigiava:

- **hediondez** — rol fechado (Lei 8.072, art. 1º); a auditoria é comparação
  contra a tabela curada em `data/hediondos.json`, mais um alarme quando o texto
  da lei muda;
- **ação penal** — a regra é pública incondicionada (art. 100 do CP), e a
  exceção está escrita no próprio diploma, em fórmulas reconhecíveis
  ("somente se procede mediante representação");
- **causas de aumento e diminuição** — o dispositivo que só majora pena não é
  tipo do catálogo, é modificador; aqui se lista o que a lei tem e
  `data/modificadores.json` não;
- **nome do tipo** — comparado com a epígrafe e com o texto do dispositivo, para
  achar registro que descreve outro crime.

E um quinto bloco que não é auditoria de dado: as **pendências jurídicas**
declaradas em `data/pendencias.json` — o que o projeto examinou e deixou em
aberto de propósito, repetido toda semana para não apodrecer no arquivo.

**Nenhuma conclusão jurídica.** Cada achado é uma pergunta, e os que viram
proposta de mudança saem em PR, para revisão — nunca aplicados direto.

Uso:
    python scripts/crawler/auditar.py                # relatório de tudo
    python scripts/crawler/auditar.py --so hediondez
    python scripts/crawler/auditar.py --so pendencias
    python scripts/crawler/auditar.py --json crawler/relatorios/auditoria.json

Saídas: 0 = nada a rever; 2 = erro; 3 = há achados.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from conferir import SNAPSHOTS, chave  # noqa: E402
from parsear import parsear  # noqa: E402
from tempo import hoje  # noqa: E402

CATALOGO = RAIZ / "static" / "data" / "crimes.json"
FONTES = RAIZ / "data" / "fontes.json"
HEDIONDOS = RAIZ / "data" / "hediondos.json"
MODIFICADORES = RAIZ / "data" / "modificadores.json"
PENDENCIAS = RAIZ / "data" / "pendencias.json"


def carregar(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def dispositivos_de(fonte_id: str) -> dict:
    pasta = SNAPSHOTS / fonte_id
    arquivos = sorted(pasta.glob("*.html")) if pasta.exists() else []
    if not arquivos:
        return {}
    return {d.chave: d for d in parsear(arquivos[-1].read_text(encoding="utf-8"))}


# ── 1. Hediondez ────────────────────────────────────────────────────────────
def _impressao(fonte_id: str, chaves: list[str]) -> str | None:
    """Digital do texto vigente dos dispositivos que definem o rol.

    Serve a uma pergunta só: *a lista mudou desde que a tabela foi escrita?*
    Compara o texto consolidado (o que o parser elegeu como vigente), não o HTML
    — assim uma reformatação da página não dispara alarme falso, e uma emenda
    dispara.
    """
    disp = dispositivos_de(fonte_id)
    if not disp:
        return None
    partes = []
    for k in chaves:
        d = disp.get(k)
        if d is None:
            return None
        partes.append(d.texto or "")
        partes += [i["texto"] for i in d.incisos]
    bruto = unicodedata.normalize("NFC", "\n".join(partes))
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()[:16]


def _casa(regra: dict, registro: dict) -> bool:
    return bool(re.search(regra["lei"], registro["lei"] or "")
                and re.search(regra["artigo"], registro["artigo"] or ""))


def auditar_hediondez(catalogo: list[dict]) -> list[dict]:
    tabela = carregar(HEDIONDOS)
    achados: list[dict] = []
    condicionais: list[int] = []

    impressao = _impressao("hediondos-8072", tabela["_meta"]["dispositivos_vigiados"])
    if impressao is None:
        achados.append({
            "campo": "hediondez", "tipo": "SEM-FONTE", "gravidade": 1,
            "detalhe": "a Lei 8.072 não está entre as fontes baixadas — sem ela, a "
                       "tabela de hediondez não pode ser verificada contra a lei",
        })
    elif tabela.get("impressao_do_texto") is None:
        achados.append({
            "campo": "hediondez", "tipo": "IMPRESSAO-AUSENTE", "gravidade": 1,
            "detalhe": f"grave `impressao_do_texto: \"{impressao}\"` em data/hediondos.json "
                       "para que a próxima mudança do rol seja detectada",
        })
    elif tabela["impressao_do_texto"] != impressao:
        achados.append({
            "campo": "hediondez", "tipo": "ROL-ALTERADO", "gravidade": 3,
            "detalhe": f"o texto do rol mudou desde {tabela['_meta']['conferido_em']} "
                       f"(impressão {tabela['impressao_do_texto']} → {impressao}). "
                       "Releia o art. 1º da Lei 8.072 e ajuste a tabela ANTES de "
                       "confiar nos achados abaixo",
        })

    fora = [f for f in tabela.get("fora_de_alcance", [])]
    n_fora = 0
    for registro in catalogo:
        if any(re.search(f["lei"], registro["lei"] or "") for f in fora):
            n_fora += 1
            continue
        # Registro que já DECLARA a condição está modelado: a hediondez dele é
        # circunstância do caso, e o catálogo diz isso em texto. Acusá-lo seria
        # cobrar uma resposta que ele deliberadamente não dá.
        if registro.get("hediondo_condicao"):
            continue
        excecao = next((e for e in tabela["excecoes"] if _casa(e, registro)), None)
        regra = next((r for r in tabela["regras"] if _casa(r, registro)), None)
        atual = registro.get("hediondo")

        if excecao:
            esperado, fundamento, condicional = excecao["hediondo"], excecao["fundamento"], False
        elif regra:
            esperado, fundamento = "Sim", regra["fundamento"]
            condicional = bool(regra.get("condicional"))
        else:
            esperado, fundamento, condicional = "Não", "fora do rol da Lei 8.072", False

        if atual == esperado:
            continue
        # Regra CONDICIONAL não decide nada: a hediondez depende de circunstância
        # do caso (grupo de extermínio, vítima criança, organização direcionada a
        # crime hediondo) ou de juízo de correspondência (crimes do CPM). Nesses,
        # tanto "Sim" quanto "Não" podem estar certos, e acusar seria ruído — a
        # lista deles sai no rodapé do relatório, para leitura.
        if condicional:
            condicionais.append(registro["id"])
            continue
        achados.append({
            "campo": "hediondez",
            "tipo": "HEDIONDEZ-DIVERGENTE", "gravidade": 2,
            "id": registro["id"], "lei": registro["lei"], "artigo": registro["artigo"],
            "crime": registro["crime"][:90],
            "de": atual, "para": esperado, "fundamento": fundamento,
            "condicional": condicional,
            "detalhe": f"catálogo diz {atual}; {fundamento} indica {esperado}",
        })

    # As pendências declaradas na própria tabela — o que se sabe que falta
    # decidir. Sem isto elas viveriam só no arquivo, e a rodada semanal deixaria
    # de lembrar que existem: silêncio de novo confundido com "está tudo certo".
    for pend in tabela.get("pendentes", []):
        achados.append({
            "campo": "hediondez", "tipo": "PENDENCIA-DECLARADA", "gravidade": 1,
            "detalhe": f"{pend['fundamento']} — {pend['descricao']} "
                       f"(ação prevista: {pend['acao']})",
        })

    if n_fora:
        achados.append({
            "campo": "hediondez", "tipo": "FORA-DE-ALCANCE", "gravidade": 0,
            "detalhe": f"{n_fora} registro(s) fora desta auditoria: "
                       + " ".join(f["motivo"] for f in fora),
        })
    if condicionais:
        achados.append({
            "campo": "hediondez", "tipo": "DEPENDE-DO-CASO", "gravidade": 0,
            "ids": condicionais,
            "detalhe": f"{len(condicionais)} registro(s) em que a hediondez depende de "
                       "circunstância do caso ou de juízo de correspondência — a lei não "
                       "decide pelo tipo. Nenhum foi acusado; ficam para leitura: "
                       + ", ".join(str(i) for i in condicionais[:40]),
        })
    return achados


# ── 2. Ação penal ───────────────────────────────────────────────────────────
# As fórmulas com que a lei excepciona a regra do art. 100 do CP. A ordem
# importa: "mediante queixa" é privada; "representação" é pública condicionada.
_ACAO_PRIVADA = re.compile(r"somente\s+se\s+procede\s+mediante\s+queixa"
                           r"|s[óo]\s+se\s+procede\s+mediante\s+queixa"
                           r"|a[çc][ãa]o\s+penal\s+[ée]\s+privada", re.I)
_ACAO_CONDICIONADA = re.compile(
    r"somente\s+se\s+procede\s+mediante\s+representa[çc]"
    r"|s[óo]\s+se\s+procede\s+mediante\s+representa[çc]"
    r"|proced[ea]-se\s+mediante\s+representa[çc]"
    r"|depende\s+de\s+representa[çc]"
    r"|a[çc][ãa]o\s+penal\s+p[úu]blica\s+condicionada", re.I)

# O catálogo escreve a ação penal privada de duas formas ("Privada" e "Ação
# Penal Privada"); a auditoria aceita as duas e só acusa quando a ESPÉCIE
# diverge, não a grafia.
# Quando o próprio artigo declara a ação INCONDICIONADA numa hipótese (art. 153,
# §2º do CP) ou ressalva casos ("salvo quando praticados em prejuízo de entidade
# de direito público"), a fórmula não vale para o artigo inteiro — e a auditoria
# não pode propor nada sem ler qual hipótese é qual.
_RESSALVA = re.compile(
    r"a[çc][ãa]o\s+penal\s+(?:ser[áa]\s+)?(?:p[úu]blica\s+)?incondicionada"
    r"|salvo\s+quando|salvo\s+se|salvo\s+nos\s+casos", re.I)

_ROTULO_ACAO = {
    "privada": "Ação Penal Privada",
    "condicionada": "Pública Condicionada",
}
_EQUIVALENTES = {
    "ação penal privada": "privada", "privada": "privada",
    "pública condicionada": "condicionada",
    "ação penal pública condicionada": "condicionada",
    "pública incondicionada": "incondicionada",
    "ação penal pública incondicionada": "incondicionada",
}


def _texto_do_artigo(disp: dict, artigo_chave: str) -> str:
    """Texto do dispositivo mais o do caput e dos parágrafos do mesmo artigo.

    A regra de ação penal quase nunca está no dispositivo que tipifica: mora num
    parágrafo do fim do artigo ("§ 4º Somente se procede mediante queixa"), ou
    num artigo próprio de encerramento do capítulo — este último fora do alcance
    desta auditoria, e por isso declarado como limite no relatório.
    """
    base = artigo_chave.split("|")[0]
    partes = []
    for k, d in disp.items():
        if k.split("|")[0] == base:
            partes.append(d.texto or "")
    return " ".join(partes)


def auditar_acao_penal(catalogo: list[dict], indice_fontes: dict) -> list[dict]:
    achados: list[dict] = []
    cache: dict[str, dict] = {}
    for registro in catalogo:
        fid = indice_fontes.get(registro["lei"])
        k = chave(registro["artigo"])
        if not fid or not k:
            continue
        if fid not in cache:
            cache[fid] = dispositivos_de(fid)
        disp = cache[fid]
        if k not in disp:
            continue
        texto = _texto_do_artigo(disp, k)
        if _RESSALVA.search(texto):
            # O artigo distingue hipóteses ("quando resultar prejuízo para a
            # Administração Pública, a ação penal será incondicionada"). Qual
            # registro cai em qual hipótese é leitura humana — vira achado para
            # a issue, nunca proposta de troca.
            if _ACAO_PRIVADA.search(texto) or _ACAO_CONDICIONADA.search(texto):
                achados.append({
                    "campo": "acao_penal", "tipo": "ACAO-COM-RESSALVA", "gravidade": 1,
                    "id": registro["id"], "lei": registro["lei"],
                    "artigo": registro["artigo"], "crime": registro["crime"][:90],
                    "detalhe": "o artigo tem fórmula de ação penal E ressalva de hipótese; "
                               f"o catálogo registra {registro.get('acao')}",
                })
            continue
        if _ACAO_PRIVADA.search(texto):
            esperado = _ROTULO_ACAO["privada"]
        elif _ACAO_CONDICIONADA.search(texto):
            esperado = _ROTULO_ACAO["condicionada"]
        else:
            continue                      # silêncio da lei = regra do art. 100
        if registro.get("acao_condicao"):
            continue                      # a espécie depende do caso, e está declarada
        atual = (registro.get("acao") or "").strip()
        especie_atual = _EQUIVALENTES.get(atual.lower(), atual.lower())
        especie_esperada = "privada" if esperado == _ROTULO_ACAO["privada"] else "condicionada"
        if especie_atual == especie_esperada:
            continue
        achados.append({
            "campo": "acao_penal", "tipo": "ACAO-DIVERGENTE", "gravidade": 2,
            "id": registro["id"], "lei": registro["lei"], "artigo": registro["artigo"],
            "crime": registro["crime"][:90], "de": atual, "para": esperado,
            "detalhe": f"o artigo traz fórmula de ação {esperado.lower()}; "
                       f"o catálogo registra {atual}",
        })
    return achados


# ── 3. Causas de aumento e diminuição ───────────────────────────────────────
_MAJORANTE = re.compile(
    r"pena\s+(?:\w+\s+){0,3}(?:é|será|serão|são)\s+aumentad|aumenta(?:m)?-se\s+a\s+pena"
    r"|pena\s+(?:\w+\s+){0,3}(?:é|será)\s+(?:reduzid|diminu[íi]d)|reduz-se\s+a\s+pena"
    r"|pena\s+ser[áa]\s+aplicada\s+em\s+dobro|aplica-se\s+em\s+dobro", re.I)
_FRACAO = re.compile(r"(?:de\s+)?(um|dois|tr[êe]s|1|2|3)[/\s]*(ter[çc]o|sexto|quarto|metade|meio|"
                     r"quinto|oitavo|d[ée]cimo)|dobro|triplo|metade", re.I)


def auditar_modificadores(indice_fontes: dict) -> list[dict]:
    """Aumentos e diminuições que a lei tem e `modificadores.json` não.

    Só LISTA. Modelar um modificador exige decidir o escopo — sobre quais tipos
    ele incide —, e isso não se lê do dispositivo isolado.
    """
    mods = carregar(MODIFICADORES)["modificadores"]
    ja_modelados = set()
    for m in mods:
        disp = m.get("dispositivo", "")
        mm = re.search(r"art\.?\s*([\w-]+)", disp, re.I)
        lei = re.match(r"([^,]+)", disp)
        if mm and lei:
            ja_modelados.add((lei.group(1).strip().lower(), mm.group(1).lower()))

    achados: list[dict] = []
    fontes = {f["id"]: f for f in carregar(FONTES)["fontes"]}
    vistos = set()
    for rotulo, fid in sorted(indice_fontes.items()):
        for k, d in dispositivos_de(fid).items():
            if d.situacao != "vigente" or d.citacao:
                continue
            texto = d.texto or ""
            if not _MAJORANTE.search(texto) or not _FRACAO.search(texto):
                continue
            artigo = k.split("|")[0].replace("Art. ", "").lower()
            chave_mod = (fontes[fid]["rotulos"][0].lower(), artigo)
            if chave_mod in ja_modelados or (fid, k) in vistos:
                continue
            vistos.add((fid, k))
            achados.append({
                "campo": "modificadores", "tipo": "MODIFICADOR-AUSENTE", "gravidade": 1,
                "fonte": fid, "dispositivo": k,
                "detalhe": texto[:150],
            })
    return achados


# ── 5. Pendências jurídicas declaradas ──────────────────────────────────────
def auditar_pendencias() -> list[dict]:
    """Repete, toda semana, o que se sabe que falta decidir.

    O oposto de um achado: não é a máquina descobrindo divergência, é o projeto
    lembrando de uma pergunta que examinou e deixou aberta de propósito. Sem
    isto, a pendência vive só num arquivo que ninguém abre, e o silêncio da
    rodada semanal volta a ser confundido com "está tudo certo".
    """
    if not PENDENCIAS.exists():
        return []
    itens = carregar(PENDENCIAS).get("pendencias", [])
    return [{
        "campo": "pendencias", "tipo": "PENDENCIA-ABERTA", "gravidade": 1,
        "detalhe": f"**{p['assunto']}** — {p['questao']} _Falta ver:_ {p['o_que_falta']} "
                   f"_Enquanto isso:_ {p['impacto']} (registrada em {p['registrado_em']})",
    } for p in itens]


# ── 4. Nome do tipo ─────────────────────────────────────────────────────────
_PALAVRA = re.compile(r"[a-zà-ÿ]{5,}", re.I)
_VAZIAS = {"artigo", "pessoa", "outrem", "alguem", "alguém", "contra", "mediante",
           "quando", "aquele", "sobre", "qualquer", "outro", "outra", "forma"}


def _radicais(texto: str) -> set[str]:
    """Palavras longas, sem acento, cortadas em quatro letras.

    Comparação grosseira de propósito: o catálogo descreve a conduta, a lei a
    define, e as duas redações nunca coincidem literalmente. Quatro letras é o
    corte que faz "falsidade" alcançar "falsa" — abaixo disso o radical casa
    qualquer coisa, acima dele um nome legítimo vira suspeito."""
    limpo = unicodedata.normalize("NFKD", (texto or "").lower())
    limpo = "".join(c for c in limpo if not unicodedata.combining(c))
    return {p[:4] for p in _PALAVRA.findall(limpo) if p not in _VAZIAS}


def auditar_nomes(catalogo: list[dict], indice_fontes: dict) -> list[dict]:
    """Registros cujo nome não conversa com o texto do dispositivo.

    Heurística, e assumidamente frouxa: sinaliza para leitura humana, nunca
    propõe troca. Foi um caso desses (o art. 350 do Código Eleitoral com o nome
    de outro crime) que passou despercebido por meses.
    """
    achados: list[dict] = []
    cache: dict[str, dict] = {}
    for registro in catalogo:
        fid = indice_fontes.get(registro["lei"])
        k = chave(registro["artigo"])
        if not fid or not k:
            continue
        if fid not in cache:
            cache[fid] = dispositivos_de(fid)
        d = cache[fid].get(k)
        if d is None or d.citacao:
            continue
        # Só o CAPUT: o parágrafo qualificado começa pela hipótese ("Se resulta:")
        # e não repete a conduta, então não há o que comparar — comparar produzia
        # cento e vinte acusações inúteis. E texto curto não sustenta comparação.
        if not k.endswith("|caput") or len((d.texto or "")) < 60:
            continue
        alvo = _radicais(f"{d.epigrafe or ''} {d.texto or ''}")
        nome = _radicais(registro["crime"])
        if not nome or not alvo:
            continue
        comum = nome & alvo
        # Nome curto casa por acaso; exigir duas palavras em comum quando há
        # material suficiente dos dois lados evita acusar rótulo enxuto.
        if comum or len(nome) <= 2:
            continue
        achados.append({
            "campo": "nome", "tipo": "NOME-SUSPEITO", "gravidade": 1,
            "id": registro["id"], "lei": registro["lei"], "artigo": registro["artigo"],
            "crime": registro["crime"][:90],
            "detalhe": f"nenhuma palavra em comum com o dispositivo: "
                       f"{(d.epigrafe or d.texto or '')[:110]}",
        })
    return achados


# ── Relatório ───────────────────────────────────────────────────────────────
TITULOS = {
    "hediondez": "Hediondez (Lei 8.072, art. 1º)",
    "acao_penal": "Ação penal",
    "modificadores": "Causas de aumento e diminuição",
    "nome": "Nome do tipo",
    "pendencias": "Pendências jurídicas em aberto",
}
LIMITES = {
    "hediondez": "O rol é fechado, mas três incisos dependem de circunstância do caso "
                 "(grupo de extermínio, organização direcionada a crime hediondo, lesão "
                 "contra vítima qualificada) — nesses, `Não` é resposta legítima e não é "
                 "acusado. O inciso VI do parágrafo único (crimes do CPM com identidade "
                 "com os do rol) exige juízo de correspondência e está fora da tabela.",
    "acao_penal": "Só enxerga a fórmula quando ela está no MESMO artigo do tipo. Regra de "
                  "ação penal em artigo de encerramento de capítulo (art. 145 do CP, por "
                  "exemplo) ou em outro diploma (Lei 9.099 para a lesão leve) não é "
                  "alcançada.",
    "modificadores": "Lista o que a lei tem e o catálogo de modificadores não. Não propõe "
                     "modelagem: definir o escopo — sobre quais tipos o aumento incide — "
                     "não se lê do dispositivo isolado.",
    "nome": "Heurística de palavras em comum. Falso positivo é esperado em nome enxuto "
            "('Furto') diante de texto longo; serve para leitura, nunca para troca "
            "automática.",
    "pendencias": "Não são achados: é `data/pendencias.json`, a lista do que o projeto "
                  "examinou e deixou em aberto de propósito. Cada entrada diz o que falta "
                  "ver para decidir. Sai daqui quando a decisão for tomada e publicada.",
}


def montar_relatorio(achados: list[dict]) -> str:
    L = [f"## Auditoria dos campos de classificação — {hoje().isoformat()}", ""]
    if not achados:
        L += ["Nenhuma divergência nos quatro campos auditados.", ""]
        return "\n".join(L) + "\n"

    por_campo: dict[str, list[dict]] = {}
    for a in achados:
        por_campo.setdefault(a["campo"], []).append(a)

    L.append(f"**{len(achados)} achado(s)**: "
             + ", ".join(f"{len(v)} em {TITULOS[k].split(' (')[0].lower()}"
                         for k, v in sorted(por_campo.items())))
    L.append("")
    for campo, itens in sorted(por_campo.items()):
        L += [f"### {TITULOS[campo]} — {len(itens)}", "",
              f"> _Limite conhecido:_ {LIMITES[campo]}", ""]
        for a in sorted(itens, key=lambda x: -x["gravidade"])[:60]:
            cabeca = (f"id {a['id']} — `{a['lei']} {a['artigo']}`"
                      if "id" in a else f"`{a.get('fonte', '')} {a.get('dispositivo', '')}`")
            L.append(f"- **{a['tipo']}** {cabeca}")
            if a.get("crime"):
                L.append(f"  - *{a['crime']}*")
            L.append(f"  - {a['detalhe']}")
        if len(itens) > 60:
            L.append(f"- _(+{len(itens) - 60} não listados)_")
        L.append("")
    return "\n".join(L) + "\n"


def rodar(so: str | None = None) -> list[dict]:
    catalogo = carregar(CATALOGO)
    fontes = carregar(FONTES)["fontes"]
    indice_fontes = {r: f["id"] for f in fontes for r in f["rotulos"]}

    achados: list[dict] = []
    if so in (None, "hediondez"):
        achados += auditar_hediondez(catalogo)
    if so in (None, "acao"):
        achados += auditar_acao_penal(catalogo, indice_fontes)
    if so in (None, "modificadores"):
        achados += auditar_modificadores(indice_fontes)
    if so in (None, "nome"):
        achados += auditar_nomes(catalogo, indice_fontes)
    if so in (None, "pendencias"):
        achados += auditar_pendencias()
    return achados


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Audita hediondez, ação penal, modificadores e nomes.")
    p.add_argument("--so", choices=["hediondez", "acao", "modificadores", "nome",
                                    "pendencias"])
    p.add_argument("--json", metavar="ARQUIVO")
    p.add_argument("--saida", default=str(RAIZ / "crawler" / "relatorios"))
    args = p.parse_args()

    achados = rodar(args.so)
    relatorio = montar_relatorio(achados)
    destino = Path(args.saida)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"auditoria-{hoje().isoformat()}.md").write_text(relatorio, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(achados, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
    print(relatorio)
    return 3 if achados else 0


if __name__ == "__main__":
    raise SystemExit(main())
