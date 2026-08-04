# -*- coding: utf-8 -*-
"""Compara o catálogo com o texto compilado e relata as divergências (F3).

Lê os snapshots baixados por `baixar.py`, estrutura cada diploma com
`parsear.py`, lê as molduras com `scripts/pena_parser.py` e confronta tudo com
`static/data/crimes.json`.

**Relata, nunca escreve.** Acuidade jurídica é o valor central do projeto: dado
errado publicado é pior que dado ausente, e boa parte dos achados exige juízo
(um dispositivo novo pode ser linha, modificador ou nada). O relatório é a
entrada de uma sessão humana, não um patch automático.

Decisões que a revisão manual impôs:

- **Comparar com o DERIVADO**, não com a fonte: a moldura real vem do `obs` via
  `parse_pena_range`, e ela vence os campos `pena_min/max` da fonte.
- **Casar por artigo em TODOS os rótulos**: artigos do CP aparecem rotulados
  pela lei que os criou ("Lei 14.811/24"), então o vínculo diploma→rótulos vem
  de `data/fontes.json`, nunca do campo `lei` cru.
- **Exceções explícitas**: o que já foi julgado e decidido (equiparação que
  virou modificador, aumento que não é linha) vive em `excecoes.json`, senão o
  relatório repetiria para sempre os mesmos achados já resolvidos.

Uso:
    python scripts/crawler/conferir.py                 # relatório de tudo
    python scripts/crawler/conferir.py --fonte lcp     # só um diploma

Saídas: 0 = nada a rever; 2 = erro de execução; 3 = há achados.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from parsear import parsear  # noqa: E402
from tempo import hoje  # noqa: E402
from pena_parser import ler_pena, ler_penas  # noqa: E402

SNAPSHOTS = RAIZ / "crawler" / "snapshots"
RELATORIOS = RAIZ / "crawler" / "relatorios"
CATALOGO = RAIZ / "static" / "data" / "crimes.json"
FONTES = RAIZ / "data" / "fontes.json"
EXCECOES = Path(__file__).resolve().parent / "excecoes.json"
LIMITES = Path(__file__).resolve().parent / "cobertura-limites.json"
TRILHA = RAIZ / "data" / "conferencia.json"

# Tolerância na comparação de molduras: 1 dia. Abaixo disso é arredondamento da
# conversão para meses (o CP conta o mês como 30 dias), não divergência real.
TOLERANCIA_MESES = 1 / 30 + 1e-6


# ── Normalização de dispositivo ─────────────────────────────────────────────
# O sufixo de letra vem COLADO ao número e pode repetir-se, com ou sem o
# marcador ordinal no meio: o catálogo escreve "Art. 121-A", "Art. 2º-A" e
# "Art. 359-M-B". A forma com ordinal era a que faltava, e por ela o art. 2º-A
# da Lei 7.716 (injúria racial) e o art. 7º-B da Lei 8.906 (prerrogativa de
# advogado) caíam na chave do artigo-base e ficavam sem conferência. Espelha o
# `_ARTIGO` de parsear.py — os dois lados têm de reduzir à MESMA chave.
_ART = re.compile(r"Art\.?\s*(\d+)\s*(?-i:[ºo°])?((?:[-–—](?-i:[A-Z]))*)", re.I)
_PAR = re.compile(r"§\s*(\d+)\s*[ºo°]?\s*(?:[-–—]\s*([A-Z]))?", re.I)


def chave(artigo: str) -> str | None:
    """"Art. 121, §2º, I" -> "Art. 121|§ 2º"  (o inciso herda a pena do §).

    O catálogo desce ao inciso quando a conduta muda; a pena, porém, é do caput
    ou do parágrafo. Reduzir os dois lados à mesma granularidade é o que faz o
    casamento funcionar sem inventar divergência.
    """
    ma = _ART.search(artigo or "")
    if not ma:
        return None
    sufixo = re.sub(r"[–—]", "-", ma.group(2)).strip("-").upper()
    base = f"Art. {ma.group(1)}" + (f"-{sufixo}" if sufixo else "")
    mp = _PAR.search(artigo)
    if mp:
        marcador = f"§ {mp.group(1)}º" + (f"-{mp.group(2)}" if mp.group(2) else "")
    elif re.search(r"(?:par[áa]grafo|par\.|§)\s*[úu]nico", artigo, re.I):
        # O catálogo abrevia ("par. único"); a lei escreve por extenso. Sem
        # aceitar as duas formas, as linhas do parágrafo único caem no caput e
        # o differ acusa divergência contra a moldura errada.
        marcador = "parágrafo único"
    else:
        marcador = "caput"
    return f"{base}|{marcador}"


def carregar_excecoes() -> list[dict]:
    if not EXCECOES.exists():
        return []
    return json.loads(EXCECOES.read_text(encoding="utf-8")).get("excecoes", [])


def dispensado(excecoes: list[dict], fonte: str, chave_disp: str,
               ids: list[int] | None = None) -> bool:
    """Este achado já foi julgado e decidido?

    A exceção casa por diploma + dispositivo e, opcionalmente, por `ids`: sem
    eles, dispensa o dispositivo inteiro; com eles, só aquelas linhas — de modo
    que uma divergência NOVA no mesmo artigo continue aparecendo.
    """
    for e in excecoes:
        if e.get("fonte") != fonte or e.get("chave") != chave_disp:
            continue
        alvo = e.get("ids")
        if not alvo:
            return True
        if ids and set(ids) <= set(alvo):
            return True
    return False


def indexar_catalogo() -> dict[str, dict[str, list[dict]]]:
    """{fonte_id: {chave_dispositivo: [linhas do catálogo]}}."""
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    de_rotulo = {r: f["id"] for f in fontes for r in f["rotulos"]}
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))

    indice: dict[str, dict[str, list[dict]]] = {}
    for linha in catalogo:
        fid = de_rotulo.get(linha["lei"])
        if not fid:
            continue
        k = chave(linha["artigo"])
        if not k:
            continue
        indice.setdefault(fid, {}).setdefault(k, []).append(linha)
    return indice


def molduras_de(disp) -> list[dict]:
    """As molduras de um dispositivo — descendo aos incisos quando preciso.

    Um parágrafo pode ser só CHAPEAU, com a pena de cada hipótese no inciso:

        Art. 157, § 3º  Se da violência resulta:
        I - lesão corporal grave, a pena é de reclusão de 7 a 18 anos, e multa;
        II - morte, a pena é de reclusão, de 24 a 30 anos, e multa.

    Ler só o preceito do parágrafo devolve lista vazia, e o conferidor pula os
    dois registros sem dizer nada. O LATROCÍNIO — a pena mais grave do Código
    Penal fora dos crimes contra a humanidade — nunca tinha sido conferido.

    A descida só acontece quando o dispositivo NÃO tem moldura própria: onde o
    caput comina a pena e os incisos apenas qualificam a conduta, quem manda é o
    caput. E o catálogo desce ao inciso pela mesma `chave`, então as molduras
    dos incisos entram como molduras do parágrafo — que é o que o casamento por
    proximidade já sabe consumir quando um preceito comina mais de uma pena.
    """
    proprias = ler_penas(disp.pena_texto or disp.texto)
    if proprias:
        return proprias
    molduras: list[dict] = []
    for inc in getattr(disp, "incisos", []) or []:
        if inc.get("situacao") == "revogado":
            continue
        molduras += ler_penas(inc.get("pena_texto") or inc.get("texto") or "")
    return molduras


def distancia(moldura: dict, cmin: float, cmax: float) -> float:
    """Quão longe esta moldura da lei está da que o registro publica.

    Serve para casar N linhas do catálogo com N molduras do preceito. Só entram
    na conta as pontas que a LEI escreveu: uma moldura de teto aberto ("até
    cinco anos") não tem piso a comparar, e uma de piso aberto (a fórmula de
    graus do CPM, cujo teto é a morte) não tem teto.

    Somar a ponta ausente como zero fazia o casamento errar por muito: no art.
    400 do CPM, o registro do homicídio qualificado (240–360) ficava a 360 da
    moldura certa — o inciso III, de piso 240 — e a apenas 96 da do inciso I,
    que é de outro crime. O differ então acusava divergência entre dois
    dispositivos que nada têm com o outro.
    """
    d = 0.0
    if not moldura.get("piso_apenas"):
        d += abs(moldura["max_meses"] - cmax)
    if not moldura.get("teto_apenas"):
        d += abs(moldura["min_meses"] - cmin)
    return d


def moldura_catalogo(linha: dict) -> tuple[float, float]:
    """Moldura canônica, em meses.

    `pena_min`/`pena_max` são os campos CRUS da fonte e podem estar
    desatualizados — `derivar_pena` não os reescreve, ele acrescenta
    `pena_*_meses` a partir do `obs`. São estes que a aplicação usa para
    calcular benefícios, e portanto os únicos que valem comparar. (Ler os campos
    crus produzia divergência falsa em todo registro cujo `obs` já estivesse
    certo e o número, não — caso de metade das contravenções da LCP.)
    """
    return (float(linha.get("pena_min_meses", linha.get("pena_min") or 0) or 0),
            float(linha.get("pena_max_meses", linha.get("pena_max") or 0) or 0))


def conferir_fonte(fonte: dict, do_catalogo: dict[str, list[dict]],
                   excecoes: list[dict]) -> list[dict]:
    """Confronta um diploma e devolve os achados."""
    pasta = SNAPSHOTS / fonte["id"]
    arquivos = sorted(pasta.glob("*.html")) if pasta.exists() else []
    if not arquivos:
        return [{"tipo": "SEM-SNAPSHOT", "gravidade": 0, "fonte": fonte["id"],
                 "detalhe": "rode scripts/crawler/baixar.py antes"}]

    achados: list[dict] = []
    dispositivos = parsear(arquivos[-1].read_text(encoding="utf-8"))
    da_lei = {d.chave: d for d in dispositivos}

    # 1) O que o catálogo tem e a lei diz estar revogado, ou cuja moldura mudou.
    for k, linhas in sorted(do_catalogo.items()):
        if dispensado(excecoes, fonte["id"], k):
            continue
        disp = da_lei.get(k)
        if disp is None:
            continue  # dispositivo não localizado: tratado no bloco 3
        if disp.citacao:
            # A linha do catálogo aponta para artigo que só ALTERA outra lei: o
            # que está ali é a redação transcrita da lei alterada, e o crime
            # verdadeiro mora no diploma de destino (que também é conferido).
            # Comparar a moldura contra essa transcrição é comparar com a
            # redação congelada na data da alteração.
            achados.append({
                "tipo": "TEXTO-CITADO", "gravidade": 3, "chave": k,
                "ids": [x["id"] for x in linhas],
                "detalhe": f"o artigo apenas altera outro diploma — "
                           f"{(disp.texto or '')[:100]}",
            })
            continue
        if disp.situacao in ("revogado", "vetado"):
            achados.append({
                "tipo": "REVOGADO", "gravidade": 3, "chave": k,
                "ids": [x["id"] for x in linhas],
                "detalhe": f"a lei marca como {disp.situacao}"
                           f"{' — ' + disp.anotacao.texto if disp.anotacao else ''}",
            })
            continue

        molduras = molduras_de(disp)
        if not molduras:
            continue
        # Um preceito pode cominar DUAS penas (dolosa e culposa, no mesmo
        # dispositivo): cada uma é uma linha do catálogo. Comparar toda linha
        # com a primeira moldura acusaria divergência falsa e, pior, uma
        # "correção" trocaria a pena de uma pela da outra. Cada linha é
        # confrontada com a moldura MAIS PRÓXIMA; sobrando moldura sem linha,
        # é candidata a linha nova — decisão humana.
        # Preceito que comina DUAS penas (dolosa e culposa no mesmo texto) são
        # dois tipos penais. Se o catálogo tem menos linhas que molduras, falta
        # linha — e ela é candidata a nascer, não a sobrescrever a existente.
        if len(molduras) > len(linhas):
            usadas = set()
            for linha in linhas:
                cmin, cmax = moldura_catalogo(linha)
                i = min(range(len(molduras)),
                        key=lambda j: distancia(molduras[j], cmin, cmax))
                usadas.add(i)
            for j, m in enumerate(molduras):
                if j in usadas:
                    continue
                achados.append({
                    "tipo": "MOLDURA-EXTRA", "gravidade": 1, "chave": k,
                    "ids": [], "fonte": fonte["id"],
                    "detalhe": f"o preceito comina outra pena sem linha no catálogo: "
                               f"{m['tipo']} {m['min_meses']:g}–{m['max_meses']:g} "
                               f"meses — {m.get('contexto', '')[:80]}",
                    "pena_lei": {"tipo": m["tipo"], "min": m["min_meses"],
                                 "max": m["max_meses"], "teto": m["teto_apenas"]},
                    "contexto": m.get("contexto", ""),
                    "epigrafe": disp.epigrafe, "texto_lei": disp.texto,
                })

        for linha in linhas:
            cmin, cmax = moldura_catalogo(linha)
            pena = min(molduras, key=lambda m: distancia(m, cmin, cmax))
            pena = dict(pena, multiplas=len(molduras) > 1)
            if dispensado(excecoes, fonte["id"], k, [linha["id"]]):
                continue
            if pena["so_multa"]:
                if cmax > 0:
                    achados.append({
                        "tipo": "DIVERGENTE-moldura", "gravidade": 2, "chave": k,
                        "ids": [linha["id"]],
                        "detalhe": f"a lei comina só multa; o catálogo traz "
                                   f"{cmin:g}–{cmax:g} meses de {linha['tipo_pena']}",
                    })
                continue
            lmin, lmax = pena["min_meses"], pena["max_meses"]
            if pena["teto_apenas"]:
                difere = abs(cmax - lmax) > TOLERANCIA_MESES
            elif pena.get("piso_apenas"):
                # Fórmula de graus do CPM: a lei escreve o piso e diz "morte" no
                # teto. Confere-se o que a lei escreveu; o teto que o catálogo
                # publica vem da modelagem do projeto, não do compilado.
                difere = abs(cmin - lmin) > TOLERANCIA_MESES
            else:
                difere = (abs(cmin - lmin) > TOLERANCIA_MESES
                          or abs(cmax - lmax) > TOLERANCIA_MESES)
            if difere:
                achados.append({
                    "tipo": "DIVERGENTE-moldura", "gravidade": 2, "chave": k,
                    "ids": [linha["id"]],
                    "detalhe": f"lei {lmin:g}–{lmax:g} × catálogo {cmin:g}–{cmax:g} "
                               f"(meses); texto: {(disp.pena_texto or '')[:90]}",
                    "multiplas": pena.get("multiplas", False),
                    "teto_apenas": pena["teto_apenas"],
                    # A moldura vai ESTRUTURADA: quem for corrigir não deve
                    # precisar reler esta mensagem com expressão regular.
                    "pena_lei": {"tipo": pena["tipo"], "min": pena["min_meses"],
                                 "max": pena["max_meses"],
                                 "teto": pena["teto_apenas"]},
                })
            # Espécie alternativa ("reclusão ou detenção") casa com qualquer uma
            # das duas: o catálogo escolheu uma, e a lei autoriza as duas.
            elif (pena["tipo"] and linha.get("tipo_pena")
                  and not any(t in linha["tipo_pena"].lower()
                              for t in pena.get("tipos") or [pena["tipo"].lower()])):
                achados.append({
                    "tipo": "DIVERGENTE-tipo", "gravidade": 2, "chave": k,
                    "ids": [linha["id"]],
                    "detalhe": f"lei {pena['tipo']} × catálogo {linha['tipo_pena']}",
                    "multiplas": pena.get("multiplas", False),
                    "teto_apenas": pena["teto_apenas"],
                    "pena_lei": {"tipo": pena["tipo"], "min": pena["min_meses"],
                                 "max": pena["max_meses"],
                                 "teto": pena["teto_apenas"]},
                })

    # 2) O que a lei tem com pena própria e o catálogo não registra.
    #
    # Diploma de REFERÊNCIA não entra aqui: a Lei 8.072 é vigiada pelo rol de
    # hediondos, não por tipos próprios, e seus arts. 8º e 9º — que alteram pena
    # de crimes de OUTROS diplomas — apareceriam como dez tipos ausentes.
    if fonte.get("referencia"):
        for a in achados:
            a["fonte"] = fonte["id"]
        return achados
    for d in dispositivos:
        if d.chave in do_catalogo or dispensado(excecoes, fonte["id"], d.chave):
            continue
        if d.situacao != "vigente" or d.citacao:
            # Citação: o artigo apenas altera outro diploma, e o texto embaixo
            # dele é a redação transcrita da lei alterada — que o conferidor já
            # vigia na página dela, com a redação de hoje. Acusar AUSENTE aqui
            # produzia crime duplicado e com a pena da época da alteração.
            continue
        pena = ler_pena(d.pena_texto or "")
        if not pena or pena["so_multa"]:
            continue  # sem pena privativa própria não é linha do catálogo
        # Preceito e sanção são vizinhos no texto (1 parágrafo, ou 2 com uma
        # anotação no meio). Distância grande significa que a linha "Pena" é de
        # OUTRO dispositivo cujo cabeçalho não foi reconhecido — foi assim que a
        # regra de ação penal da Lei de Abuso (art. 3º) apareceu com detenção de
        # 1 a 4 anos, herdada do estatuto da OAB transcrito no fim da lei.
        if (d.pena_distancia or 0) > 3:
            continue
        achados.append({
            "tipo": "AUSENTE", "gravidade": 1, "chave": d.chave,
            "ids": [],
            "detalhe": f"{(d.epigrafe or d.texto or '')[:70]} — "
                       f"{(d.pena_texto or '')[:70]}",
            "vigencia_pendente": d.vigencia_pendente,
            "epigrafe": d.epigrafe, "texto_lei": d.texto,
            "pena_lei": {"tipo": pena["tipo"], "min": pena["min_meses"],
                         "max": pena["max_meses"], "teto": pena["teto_apenas"]},
        })

    for a in achados:
        a["fonte"] = fonte["id"]
    return achados


# ── Por que este registro não foi conferido ─────────────────────────────────
#
# Havia três motivos e um deles se chamava "indeterminado", que não é motivo: é
# a confissão de que ninguém sabe. E os três viravam UM NÚMERO no relatório —
# "253 sem moldura própria" —, sem um id sequer. Ninguém consegue agir sobre um
# número, e foi debaixo dele que três incisos do art. 151 do CP atravessaram
# todas as rodadas publicando seis vezes a pena que a lei comina.
#
# Agora são cinco motivos, e a diferença entre eles é o que se pode fazer a
# seguir. Os quatro primeiros são limites DECLARADOS — a lei não deixou moldura
# ali para comparar. O quinto é o alarme: a lei escreveu a pena e o parser não
# leu. Ele tende a zero, e cada unidade que sobra é uma lacuna com endereço.

# A lei manda aplicar a pena de OUTRO dispositivo. É COPIÁVEL: basta resolver a
# remissão. `auditar.py --so remissao` já confere a família do "na mesma pena
# incorre" — as demais esperam a vez.
_PENA_IMPORTADA = re.compile(
    r"mesmas?\s+pena|penas?\s+do\s+caput|penas?\s+deste\s+artigo"
    r"|incorre\s+n[ao]s?\s+pena|penas?\s*[-–—:]\s*as?\s+(?:d|comina)"
    r"|penas?\s+d[oa]\s+art|aplica-se\s+(?:tamb[ée]m\s+)?a\s+(?:mesma\s+)?pena"
    r"|aplica-se\s+.{0,40}\bo\s+disposto\b|sujeit[oa]s?\s+[àa]s?\s+penas"
    r"|punid[oa]\s+com\s+as\s+penas|pena\s+(?:cominada\s+)?para\s+o\s+tempo"
    r"|constitu[ei]m?\s+crimes?", re.IGNORECASE)

# A lei manda CALCULAR sobre uma base: aumento, diminuição, dobro. É derivável
# por aritmética, e o motor de modificadores do projeto já sabe fazer a conta —
# falta ligá-lo ao conferidor. É o maior dos baldes, e o próximo a atacar.
_PENA_DERIVADA = re.compile(
    r"[ée]\s+aumentad|[ée]\s+agravad|[ée]\s+majorad|[ée]\s+reduzid"
    r"|[ée]\s+diminu[íi]d|s[ãa]o\s+(?:aumentad|reduzid|diminu[íi]d)"
    r"|ser[áã]o?\s+(?:aumentad|reduzid|diminu[íi]d)|aumenta(?:m)?-se|reduz-se"
    r"|diminui-se|poder[áãa]o?\s+ser\s+reduzid|pode\s+(?:ser\s+)?reduzi"
    r"|pode\s+diminuir|ter[áã]\s+.{0,30}pena\s+reduzid|reduz\s+de\s+metade|diminu[íi]-l[ao]|substituir\s+a\s+pena"
    r"|penas?\s*[-–—:]\s*metade|pel[oa]\s+d[ôo]bro|n[oa]\s+d[ôo]bro|em\s+dobro|ao\s+dobro"
    r"|em\s+triplo|duplicad|de\s+um\s+ter[çc]o|[àa]\s+metade", re.IGNORECASE)

# O dispositivo NÃO é preceito secundário: é norma explicativa ("Equipara-se à
# coisa móvel a energia elétrica"), extensiva ("É punível a calúnia contra os
# mortos") ou de extinção de punibilidade. A moldura que o registro publica vem
# do caput, pela estrutura do artigo, e não há remissão a resolver. Reconhecido
# pela AUSÊNCIA de vocabulário de pena — se a palavra não aparece, não há
# preceito ali que possa ter sido mal lido.
_VOCABULARIO_DE_PENA = re.compile(
    r"\bpenas?\b|reclus[ãa]o|deten[çc][ãa]o|pris[ãa]o|multa|\bmorte\b", re.IGNORECASE)

MOTIVOS = {
    "sancao_nao_privativa": "o registro não tem pena privativa (multa ou outra sanção)",
    "pena_importada": "a lei manda aplicar a pena de outro dispositivo — copiável",
    "pena_derivada": "a lei manda calcular sobre uma base (aumento, diminuição) — derivável",
    "sem_preceito_proprio": "o dispositivo não comina pena: é norma explicativa ou extensiva",
    "ilegivel": "A LEI ESCREVEU A PENA E O PARSER NÃO LEU — lacuna a fechar",
}


def _por_referencia(disp, linha: dict) -> str:
    """Por que este registro não foi conferido. Nunca "não sei"."""
    if not linha.get("tem_pena_privativa", True):
        return "sancao_nao_privativa"
    texto = f"{disp.pena_texto or ''} {disp.texto or ''}"
    # A ordem importa: "aplica-se o disposto no § 3º do artigo anterior" importa
    # uma pena inteira, ainda que o dispositivo de destino seja de aumento.
    if _PENA_IMPORTADA.search(texto):
        return "pena_importada"
    if _PENA_DERIVADA.search(texto):
        return "pena_derivada"
    if not _VOCABULARIO_DE_PENA.search(texto):
        return "sem_preceito_proprio"
    return "ilegivel"


def cobertura(fontes: list[dict], indice: dict[str, dict[str, list[dict]]],
              excecoes: list[dict] | None = None) -> dict:
    """Quanto do catálogo é de fato CONFERIDO contra a lei — e quanto não é.

    O relatório de achados responde "o que está errado". Esta função responde a
    pergunta anterior, que é a que decide se dá para confiar no catálogo: **de
    quantos registros o conferidor tem opinião?** Um registro cujo dispositivo
    nem sequer é localizado no texto compilado não aparece como divergente —
    aparece como nada, e silêncio não é aprovação.

    Quatro classes, por registro:

    - `conferido`: dispositivo localizado, vigente, com moldura legível na lei, e
      a pena publicada bate (dentro da tolerância de 1 dia);
    - `divergente`: localizado e a pena NÃO bate — é o que vira achado;
    - `sem_moldura_na_lei`: localizado, mas a lei não traz moldura legível ali
      (pena remetida ao caput, pena embutida na frase, sanção só de multa);
    - `nao_localizado`: o dispositivo do registro não foi encontrado no compilado
      — pode ser rótulo errado no catálogo ou limite do parser. É o número que
      mede o alcance real da conferência.
    """
    excecoes = excecoes or []
    resultado = {"conferido": [], "divergente": [], "sem_moldura_na_lei": [],
                 "nao_localizado": [], "sem_snapshot": [], "dispensado": []}
    for fonte in fontes:
        do_catalogo = indice.get(fonte["id"], {})
        if not do_catalogo:
            continue
        pasta = SNAPSHOTS / fonte["id"]
        arquivos = sorted(pasta.glob("*.html")) if pasta.exists() else []
        if not arquivos:
            resultado["sem_snapshot"] += [x["id"] for v in do_catalogo.values() for x in v]
            continue
        da_lei = {d.chave: d for d in parsear(arquivos[-1].read_text(encoding="utf-8"))}

        for k, linhas in do_catalogo.items():
            disp = da_lei.get(k)
            if disp is None:
                resultado["nao_localizado"] += [(fonte["id"], k, x["id"]) for x in linhas]
                continue
            molduras = [m for m in molduras_de(disp) if not m["so_multa"]]
            for linha in linhas:
                # Já julgado e decidido: não é conferido nem divergente — é
                # dispensado, e o relatório precisa dizê-lo em vez de somar ao
                # número que promete conferência.
                if (dispensado(excecoes, fonte["id"], k, [linha["id"]])
                        or dispensado(excecoes, fonte["id"], k)):
                    resultado["dispensado"].append((fonte["id"], k, linha["id"]))
                    continue
                # Registro sem pena privativa não se confronta com moldura de
                # prisão. A questão aparece desde que o conferidor passou a
                # descer aos incisos: o art. 11 da Lei 6.091 pune o inciso I com
                # detenção e o II só com dias-multa, e o registro do inciso II
                # ia comparar-se à moldura do I. Ele entra onde sempre esteve —
                # entre os que a lei não dá moldura privativa para conferir.
                if not molduras or not linha.get("tem_pena_privativa", True):
                    resultado["sem_moldura_na_lei"].append(
                        (fonte["id"], k, linha["id"], _por_referencia(disp, linha)))
                    continue
                cmin, cmax = moldura_catalogo(linha)
                pena = min(molduras, key=lambda m: distancia(m, cmin, cmax))
                bate_max = (pena.get("piso_apenas")
                            or abs(cmax - pena["max_meses"]) <= TOLERANCIA_MESES)
                bate_min = pena["teto_apenas"] or abs(cmin - pena["min_meses"]) <= TOLERANCIA_MESES
                especie = any(t in (linha.get("tipo_pena") or "").lower()
                              for t in pena.get("tipos") or [])
                alvo = "conferido" if (bate_max and bate_min and especie) else "divergente"
                resultado[alvo].append((fonte["id"], k, linha["id"]))
    return resultado


def carimbar(res: dict, destino: Path) -> int:
    """Grava a trilha de auditoria: quando cada registro foi conferido, e contra o quê.

    O relatório da rodada é sobre a RODADA; some na semana seguinte. Esta trilha é
    sobre o REGISTRO, e é o que permite a quem cita um dado saber quando ele foi
    confrontado com a lei — a pergunta que um catálogo de pesquisa precisa responder.

    Fica num arquivo próprio, e não em `data/crimes.json`, por dois motivos: a fonte é
    escrita à mão e não deve ganhar campo de máquina; e carimbar 1.400 registros por
    semana dentro dela encheria todo diff de ruído. `transform_data` junta os dois no
    derivado, que é o que a aplicação lê.
    """
    fontes = {f["id"]: f for f in json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]}
    dia = hoje().isoformat()
    trilha: dict[str, dict] = {}
    for resultado in ("conferido", "divergente", "sem_moldura_na_lei", "dispensado"):
        for item in res[resultado]:
            fid, chave_disp, ident = item[0], item[1], item[2]
            trilha[str(ident)] = {
                "conferido_em": dia,
                "resultado": resultado,
                "dispositivo": chave_disp,
                "fonte": fontes[fid]["url"],
            }
    conteudo = {
        "_meta": {
            "descricao": "Trilha de auditoria por registro: quando cada tipo penal foi "
                         "confrontado com o texto compilado, com que resultado e contra "
                         "qual página. Gerado por scripts/crawler/conferir.py --carimbar.",
            "resultados": {
                "conferido": "a moldura publicada bate com a que a lei comina",
                "divergente": "não bate — virou achado da rodada",
                "sem_moldura_na_lei": "o dispositivo não traz moldura própria (pena por "
                                      "referência, sanção não privativa)",
                "dispensado": "exceção já julgada, em excecoes.json",
            },
            "gerado_em": dia,
        },
        "registros": dict(sorted(trilha.items(), key=lambda kv: int(kv[0]))),
    }
    destino.write_bytes((json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n")
                        .replace("\n", "\r\n").encode("utf-8"))
    return len(trilha)


def contar_nao_conferidos(res: dict) -> dict[str, int]:
    """Quantos registros o conferidor NÃO garante, por motivo."""
    contas: dict[str, int] = {"nao_localizado": len(res["nao_localizado"])}
    for item in res["sem_moldura_na_lei"]:
        contas[item[3]] = contas.get(item[3], 0) + 1
    return contas


def conferir_limites(contas: dict[str, int]) -> tuple[list[str], list[str]]:
    """A trava: o que o conferidor não garante não pode crescer em silêncio.

    Nos moldes de `excecoes.json` — o que já foi julgado fica escrito, com
    motivo e data. Aqui o que fica escrito é o TAMANHO aceito de cada balde de
    não conferidos. Crescer é regressão e vira achado; encolher é notícia boa e
    vira convite a baixar o limite.

    É isto que impede a próxima lacuna do parser de reabrir o buraco por onde
    passaram o art. 151 do CP e o Código de Trânsito inteiro. Sem a trava, uma
    mudança de redação no Planalto pode tirar dez registros da conferência sem
    que nenhum número no relatório pareça diferente do da semana passada.

    Devolve (regressões, folgas).
    """
    if not LIMITES.exists():
        return [], []
    limites = json.loads(LIMITES.read_text(encoding="utf-8")).get("limites", {})
    regressoes, folgas = [], []
    for motivo, teto in sorted(limites.items()):
        agora = contas.get(motivo, 0)
        if agora > teto:
            regressoes.append(f"**{motivo}**: {agora} registros, e o limite aceito é "
                              f"{teto} — {agora - teto} a mais que na última vez que "
                              "isto foi olhado")
        elif agora < teto:
            folgas.append(f"`{motivo}`: {agora} < {teto} — dá para baixar o limite")
    for motivo, agora in sorted(contas.items()):
        if motivo not in limites and agora:
            regressoes.append(f"**{motivo}**: {agora} registros, e este motivo nem consta "
                              "dos limites — declare-o antes de aceitá-lo")
    return regressoes, folgas


def gravar_limites(contas: dict[str, int]) -> None:
    """Regrava os limites com os números de agora. Ato DELIBERADO, e commitado.

    Não roda sozinho na rodada semanal, de propósito: se o arquivo se
    atualizasse quando a cobertura piora, a trava não travaria nada.
    """
    conteudo = {
        "_meta": {
            "descricao": "Quantos registros o conferidor aceita NÃO garantir, por "
                         "motivo. Crescer é regressão e vira achado da rodada; "
                         "encolher é convite a baixar o número. Regrave com "
                         "`python scripts/crawler/conferir.py --atualizar-limites` e "
                         "commite junto da mudança que justificou.",
            "por_que": "O erro que originou esta trava foi um SILÊNCIO: três incisos "
                       "do art. 151 do CP publicaram por anos seis vezes a pena que a "
                       "lei comina, e nenhuma rodada disse nada, porque um dispositivo "
                       "cuja pena está em outro dispositivo nunca tem pena escrita. "
                       "Contar o silêncio é o que o torna visível.",
            "motivos": MOTIVOS | {"nao_localizado":
                                  "o dispositivo do registro não foi achado no compilado"},
            "gerado_em": hoje().isoformat(),
        },
        "limites": dict(sorted(contas.items())),
    }
    LIMITES.write_bytes((json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n")
                        .replace("\n", "\r\n").encode("utf-8"))


def montar_cobertura(res: dict, total_catalogo: int) -> str:
    """A seção de cobertura do relatório, em números redondos."""
    n = {k: len(v) for k, v in res.items()}
    medido = sum(n.values())
    fora = total_catalogo - medido
    pct = (100 * n["conferido"] / total_catalogo) if total_catalogo else 0
    motivos: dict[str, int] = {}
    for item in res["sem_moldura_na_lei"]:
        motivos[item[3]] = motivos.get(item[3], 0) + 1
    L = [
        "## Cobertura da conferência", "",
        f"De **{total_catalogo}** registros do catálogo:", "",
        f"- **{n['conferido']}** ({pct:.1f}%) conferidos e batendo com o texto compilado;",
        f"- **{n['divergente']}** divergentes (viram achado);",
        f"- **{n['sem_moldura_na_lei']}** sem moldura PRÓPRIA na lei, "
        "discriminados abaixo por motivo;",
        f"- **{n['nao_localizado']}** cujo dispositivo não foi localizado no compilado;",
    ]
    if n["dispensado"]:
        L.append(f"- {n['dispensado']} dispensados por exceção já julgada "
                 "(`scripts/crawler/excecoes.json`).")
    if n["sem_snapshot"]:
        L.append(f"- {n['sem_snapshot']} sem página baixada nesta rodada;")
    if fora:
        L.append(f"- {fora} fora do alcance (rótulo sem diploma em `fontes.json`).")
    L += ["", "Silêncio não é aprovação: as três últimas linhas são o que o "
          "conferidor **não** garante.", ""]

    regressoes, folgas = conferir_limites(contar_nao_conferidos(res))
    if regressoes:
        L += ["> ### ⛔ COBERTURA PIOROU", ">",
              "> Registros saíram da conferência sem que ninguém decidisse isso. "
              "Ou uma redação nova do Planalto deixou de ser legível, ou entrou "
              "registro em dispositivo que a lei não confere. Ache o motivo antes "
              "de subir o limite.", ">"]
        L += [f"> - {r}" for r in regressoes] + [""]
    if folgas:
        L += ["<details><summary>Limites de cobertura com folga — dá para apertar"
              "</summary>", ""]
        L += [f"- {f}" for f in folgas]
        L += ["", "Rode `conferir.py --atualizar-limites` e commite o arquivo.",
              "", "</details>", ""]

    # Cada registro não conferido sai com id e motivo. Enquanto isto era só um
    # número, ninguém tinha como agir sobre ele — e três incisos do art. 151 do
    # CP passaram anos publicando seis vezes a pena da lei debaixo dele.
    if res["sem_moldura_na_lei"]:
        L += ["### Sem moldura própria na lei — por que", ""]
        por_motivo: dict[str, list] = {}
        for fid, k, ident, motivo in res["sem_moldura_na_lei"]:
            por_motivo.setdefault(motivo, []).append((fid, k, ident))
        # O alarme primeiro; os limites declarados depois, do maior ao menor.
        ordem = sorted(por_motivo, key=lambda m: (m != "ilegivel", -len(por_motivo[m])))
        for motivo in ordem:
            itens = sorted(por_motivo[motivo])
            grito = "⚠️ " if motivo == "ilegivel" else ""
            L += [f"<details><summary>{grito}<b>{motivo}</b> — {len(itens)}: "
                  f"{MOTIVOS.get(motivo, '')}</summary>", ""]
            for fid, k, ident in itens:
                L.append(f"- `{fid}` `{k}` — id {ident}")
            L += ["", "</details>", ""]
    if res["nao_localizado"]:
        L += ["<details><summary><b>Dispositivos não localizados no compilado</b> — "
              f"{len(res['nao_localizado'])}</summary>", ""]
        for fid, k, ident in sorted(res["nao_localizado"]):
            L.append(f"- `{fid}` `{k}` — id {ident}")
        L += ["", "</details>", ""]
    return "\n".join(L)


def montar_relatorio(por_fonte: dict[str, list[dict]]) -> str:
    total = sum(len(v) for v in por_fonte.values())
    linhas = [f"# Conferidor — {hoje().isoformat()}", ""]
    if not total:
        linhas.append("Nenhuma divergência entre o catálogo e o texto compilado.")
        return "\n".join(linhas) + "\n"

    contagem: dict[str, int] = {}
    for achados in por_fonte.values():
        for a in achados:
            contagem[a["tipo"]] = contagem.get(a["tipo"], 0) + 1
    linhas.append(f"**{total} achado(s)** em {len(por_fonte)} diploma(s): "
                  + ", ".join(f"{v} {k}" for k, v in sorted(contagem.items())))
    linhas.append("")
    linhas.append("> Cada achado é uma pergunta, não uma conclusão: confira o "
                  "dispositivo no compilado antes de alterar o catálogo.")
    linhas.append("")

    for fid, achados in sorted(por_fonte.items()):
        linhas.append(f"## {fid} — {len(achados)} achado(s)")
        linhas.append("")
        for a in sorted(achados, key=lambda x: (-x["gravidade"], x.get("chave", ""))):
            ids = f" (id {', '.join(str(i) for i in a['ids'])})" if a.get("ids") else ""
            pendente = " ⏳ vigência futura" if a.get("vigencia_pendente") else ""
            linhas.append(f"- **{a['tipo']}** `{a.get('chave', '')}`{ids}{pendente}")
            linhas.append(f"  - {a['detalhe']}")
        linhas.append("")
    return "\n".join(linhas) + "\n"


def main() -> int:
    # Só ao rodar como script: reconfigurar o stdout no import quebraria a
    # captura do pytest, que troca sys.stdout por um arquivo próprio.
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace")
    p = argparse.ArgumentParser(description="Confere o catálogo contra o compilado.")
    p.add_argument("--fonte", action="append", default=[], metavar="ID")
    p.add_argument("--saida", default=str(RELATORIOS))
    p.add_argument("--carimbar", action="store_true",
                   help="grava a trilha de auditoria em data/conferencia.json")
    p.add_argument("--atualizar-limites", action="store_true",
                   help="regrava cobertura-limites.json com os números de agora")
    args = p.parse_args()

    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    if args.fonte:
        fontes = [f for f in fontes if f["id"] in set(args.fonte)]
    excecoes = carregar_excecoes()
    indice = indexar_catalogo()

    por_fonte: dict[str, list[dict]] = {}
    for f in fontes:
        achados = conferir_fonte(f, indice.get(f["id"], {}), excecoes)
        if achados:
            por_fonte[f["id"]] = achados

    total = len(json.loads(CATALOGO.read_text(encoding="utf-8")))
    medida = cobertura(fontes, indice, excecoes)
    contas = contar_nao_conferidos(medida)

    # Só numa rodada COMPLETA: os limites são do catálogo inteiro, e regravá-los
    # depois de conferir um diploma zeraria o teto dos outros 61.
    if args.atualizar_limites and not args.fonte:
        gravar_limites(contas)
        print(f"limites de cobertura regravados em {LIMITES.name}: "
              + ", ".join(f"{k}={v}" for k, v in sorted(contas.items())))

    cob = montar_cobertura(medida, total)
    relatorio = montar_relatorio(por_fonte) + "\n" + cob
    regressoes, _ = conferir_limites(contas)

    # A trilha só é reescrita numa rodada COMPLETA: carimbar depois de conferir um
    # diploma só apagaria o registro dos outros 61.
    if args.carimbar and not args.fonte:
        n = carimbar(medida, TRILHA)
        print(f"trilha de auditoria: {n} registros carimbados em {TRILHA.name}")
    destino = Path(args.saida)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"{hoje().isoformat()}.md").write_text(relatorio, encoding="utf-8")
    (destino / f"{hoje().isoformat()}.json").write_text(
        json.dumps(por_fonte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total = sum(len(v) for v in por_fonte.values())
    print(relatorio if total <= 40 else
          f"{total} achados — relatório em {destino}/{hoje().isoformat()}.md")
    # Cobertura que piorou vale como achado no código de saída, ainda que o
    # differ não tenha encontrado divergência nenhuma: registro que SAIU da
    # conferência é precisamente o que ninguém veria de outro jeito.
    return 3 if (total or regressoes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
