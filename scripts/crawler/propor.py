# -*- coding: utf-8 -*-
"""Monta a proposta da rodada: escolhe o diploma, aplica e escreve o PR (F6b).

`corrigir.py` e `criar.py` sabem propor mudanças de UM diploma; este módulo é o
que falta entre eles e o workflow semanal — decide qual diploma vai na rodada,
aplica as duas coisas na mesma árvore, escreve a entrada de changelog, sobe a
versão e deixa pronto o corpo do PR com a evidência de cada mudança.

Quatro decisões, todas para que o PR seja revisável por gente:

- **Um diploma por PR.** Revisar pena exige abrir o texto compilado; misturar
  vinte diplomas num PR só produz aprovação no atacado. O escolhido é o de mais
  propostas, e o próximo vai na semana seguinte.
- **Por padrão, só CORRIGE linha existente.** Criar linha é decidir se o
  dispositivo é crime autônomo, causa de aumento ou nada — e a primeira leva
  automática de linhas novas (F6) trouxe 29 registros que não eram tipos penais
  vigentes: contravenções revogadas, infrações administrativas do ECA e, sobre-
  tudo, redações do Código Penal transcritas dentro das leis que o alteraram.
  As guardas contra esses casos existem agora (`parsear._marcar_citacoes`,
  espécie de pena, revogação anotada), mas quem cria linha continua sendo gente:
  `--com-novas` liga a proposta de linha nova, e o workflow só a usa quando
  alguém pedir explicitamente.
- **O PR fecha uma versão.** Ele sobe `package.json` e `CITATION.cff` e escreve
  a entrada de changelog: mergear publica a release, como em qualquer outro PR
  do projeto. Entrada sem bump seria pior — anunciaria no feed uma versão já
  publicada (é o que `scripts/validar-changelog.mjs` reprova).
- **Nada de silencioso.** O bump é conferido depois de escrito (substituição de
  texto já falhou em silêncio aqui) e cada mudança leva no corpo o trecho da lei
  que a motivou.

Uso:
    python scripts/crawler/propor.py                 # o que sairia (não escreve)
    python scripts/crawler/propor.py --aplicar --saida crawler/proposta

Saídas: 0 = proposta pronta; 1 = nada mecânico nesta rodada; 2 = erro.
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

import corrigir  # noqa: E402
import criar  # noqa: E402
from conferir import SNAPSHOTS  # noqa: E402
from transform_data import _faixa_de_meses, proximo_id  # noqa: E402

FONTES = RAIZ / "data" / "fontes.json"
CATALOGO_FONTE = RAIZ / "data" / "crimes.json"
PACKAGE = RAIZ / "package.json"
CITATION = RAIZ / "CITATION.cff"
ENTRADAS = RAIZ / "src" / "data" / "changelog" / "entries"
SITE = "https://amorim-rc.github.io/sispenas"


# ── Versão ──────────────────────────────────────────────────────────────────
def versao_atual() -> str:
    return json.loads(PACKAGE.read_text(encoding="utf-8"))["version"]


def proxima_versao(atual: str) -> str:
    """Correção de dado é patch (roadmap: `1.1.Z`)."""
    maior, menor, patch = (int(x) for x in atual.split("."))
    return f"{maior}.{menor}.{patch + 1}"


def _substituir_versao(caminho: Path, padrao: str, atual: str, nova: str) -> None:
    """Troca a versão e CONFERE o resultado.

    O bump por substituição de texto já falhou em silêncio neste repositório
    (três entradas anunciaram versões que nunca saíram). Aqui, se a troca não
    pegar, o processo morre — nunca segue com o arquivo intacto.

    Trabalha sobre os bytes porque o repositório é CRLF: reescrever pelo modo
    texto trocaria a quebra de linha do arquivo inteiro e o diff do PR deixaria
    de mostrar uma linha para mostrar cinquenta.
    """
    texto = caminho.read_bytes().decode("utf-8")
    novo, trocas = re.subn(padrao.format(v=re.escape(atual)),
                           lambda m: m.group(0).replace(atual, nova), texto, count=1)
    if trocas != 1 or nova not in novo:
        raise SystemExit(f"bump falhou em {caminho.name}: {trocas} substituição(ões)")
    caminho.write_bytes(novo.encode("utf-8"))


def subir_versao(nova: str) -> None:
    atual = versao_atual()
    _substituir_versao(PACKAGE, r'"version":\s*"{v}"', atual, nova)
    _substituir_versao(CITATION, r'version:\s*"{v}"', atual, nova)
    conferida = json.loads(PACKAGE.read_text(encoding="utf-8"))["version"]
    if conferida != nova:
        raise SystemExit(f"package.json ficou em {conferida}, não em {nova}")


# ── Escolha do diploma ──────────────────────────────────────────────────────
def carregar_fontes() -> list[dict]:
    return json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]


def propostas_da_fonte(fonte_id: str, proximo_id: int,
                       com_novas: bool) -> tuple[list[dict], list[dict], list[dict]]:
    """(correções, linhas novas, achados que ficam para gente)."""
    correcoes, humanos = corrigir.gerar(fonte_id)
    novas = criar.gerar(fonte_id, proximo_id)[0] if com_novas else []
    return correcoes, novas, humanos


def escolher(com_novas: bool, apenas: str | None = None) -> dict | None:
    """O diploma da rodada: o de mais propostas mecânicas.

    Empate desfeito pela ordem de `fontes.json`, que é estável — duas execuções
    na mesma árvore têm de produzir o mesmo PR.
    """
    catalogo = json.loads(CATALOGO_FONTE.read_text(encoding="utf-8"))
    # Conta os ids aposentados: um endereço público nunca é reaproveitado.
    proximo = proximo_id(catalogo)

    melhor = None
    for f in carregar_fontes():
        if apenas and f["id"] != apenas:
            continue
        if not (SNAPSHOTS / f["id"]).exists():
            continue  # sem snapshot não há o que conferir (nem o que propor)
        correcoes, novas, humanos = propostas_da_fonte(f["id"], proximo, com_novas)
        if not correcoes and not novas:
            continue
        if melhor is None or len(correcoes) + len(novas) > melhor["total"]:
            melhor = {"fonte": f, "correcoes": correcoes, "novas": novas,
                      "humanos": humanos, "total": len(correcoes) + len(novas)}
    return melhor


# ── Textos ──────────────────────────────────────────────────────────────────
def _rotulo(fonte: dict) -> str:
    return fonte["rotulos"][0]


def corpo_pr(escolha: dict, versao: str) -> str:
    """Corpo do PR: uma seção por mudança, cada uma com o trecho da lei."""
    f = escolha["fonte"]
    correcoes, novas, humanos = escolha["correcoes"], escolha["novas"], escolha["humanos"]
    L = [
        f"## Diploma: **{', '.join(f['rotulos'])}**", "",
        f"Rodada automática do conferidor. Texto oficial conferido: <{f['url']}>", "",
        f"- **{len(correcoes)}** correção(ões) de moldura ou espécie de pena em linha existente;",
        f"- **{len(novas)}** linha(s) nova(s) proposta(s);",
        f"- fecha a versão **v{versao}** (o merge publica a release).", "",
        "> Cada mudança é uma **proposta** conferida contra o texto compilado, não uma "
        "conclusão jurídica. O merge continua exigindo revisão humana.", "",
    ]

    if correcoes:
        L += ["## Correções de linha existente", ""]
        for p in correcoes:
            a, d = p["antes"], p["depois"]
            L += [
                f"### `{a['artigo']}` — id {a['id']}", f"*{a['crime'][:110]}*", "",
                f"- **Na lei:** {p['evidencia']}",
                f"- **Antes:** {a['pena_min']}–{a['pena_max']} meses, {a['tipo_pena']}",
                f"- **Depois:** {d['pena_min']}–{d['pena_max']} meses, {d['tipo_pena']}",
                f"- **obs:** `{d['obs'][:150]}`",
                f"- Conferir: <{SITE}/pesquisa/tipos?tipo={a['id']}>", "",
            ]

    if novas:
        L += [
            "## Linhas novas", "",
            "Do texto saem seis campos; `acao`, `violencia` e `grave_ameaca` são "
            "herdados do caput do mesmo artigo, e `tentativa`/`hediondo` seguem a "
            "regra do crime culposo. **É aí que a revisão deve olhar primeiro.**", "",
        ]
        for p in novas:
            linha, achado = p["linha"], p["achado"]
            herdado = ", ".join(p["herdado"]) or "nenhum"
            L += [
                f"### `{linha['artigo']}` — id {linha['id']} (novo)",
                f"*{linha['crime'][:110]}*", "",
                f"- **Na lei:** {achado['detalhe'][:220]}",
                f"- **Pena proposta:** {linha['pena_min']}–{linha['pena_max']} meses, "
                f"{linha['tipo_pena']} ({linha['elemento'].lower()})",
                f"- **Herdado do caput** (id {p['caput_id']}): {herdado}",
                f"- **Origem do achado:** {achado['tipo']}", "",
            ]

    if humanos:
        L += [
            f"## Fora do automático ({len(humanos)}) — seguem na issue", "",
            "Dispositivo revogado, pena só de multa, leitura incerta ou mais de uma "
            "linha do catálogo para o mesmo dispositivo: decisão de modelagem, não "
            "leitura de texto.", "",
        ]
        for a in humanos[:25]:
            L += [f"- `{a.get('chave', '?')}` — **{a['tipo']}**: {a['detalhe'][:110]}"]
        L += [""]

    L += [
        "---", "",
        "Gerado por `scripts/crawler/propor.py` a partir do texto compilado baixado "
        "nesta execução. Reproduzível localmente:", "",
        "```", f"python scripts/crawler/baixar.py --fonte {f['id']}",
        f"python scripts/crawler/propor.py --fonte {f['id']}", "```", "",
    ]
    return "\n".join(L) + "\n"


def _plural(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def _artigo_em_prosa(artigo: str) -> str:
    """"Art. 50, I" -> "art. 50, I" — sem derrubar o algarismo romano."""
    return re.sub(r"^Art\.", "art.", artigo.strip())


def _frase_correcoes(correcoes: list[dict]) -> str:
    """Até três correções descritas em prosa, para o corpo da entrada.

    Em anos e meses, como a lei fala e como o site mostra: o feed é lido por
    gente, e "12 a 60 meses" obriga quem lê a fazer a conta.
    """
    exemplos = []
    for p in correcoes[:3]:
        a, d = p["antes"], p["depois"]
        exemplos.append(
            f"o {_artigo_em_prosa(a['artigo'])} constava com "
            f"{_faixa_de_meses(a['pena_min'], a['pena_max'])} de "
            f"{a['tipo_pena'].lower()} e passa a "
            f"{_faixa_de_meses(d['pena_min'], d['pena_max'])} de "
            f"{d['tipo_pena'].lower()}")
    return "; ".join(exemplos)


def entrada_changelog(escolha: dict, versao: str, hoje: str) -> tuple[Path, str]:
    """A entrada do feed — texto puro, sem markdown (contrato do ChangelogEntry)."""
    f = escolha["fonte"]
    correcoes, novas = escolha["correcoes"], escolha["novas"]
    ident = f"{hoje}-conferidor-{f['id']}"
    destino = ENTRADAS / hoje[:4] / f"{ident}.ts"
    n = 2
    while destino.exists():
        ident = f"{hoje}-conferidor-{f['id']}-{n}"
        destino = ENTRADAS / hoje[:4] / f"{ident}.ts"
        n += 1

    rotulo = _rotulo(f)
    partes = []
    if correcoes:
        partes.append(_plural(len(correcoes), "pena corrigida", "penas corrigidas"))
    if novas:
        partes.append(_plural(len(novas), "tipo acrescentado", "tipos acrescentados"))
    # Rótulo na frente e travessão: o artigo definido varia com o diploma ("no
    # CP", "na Lei 6.766/79", "no ECA") e não há como acertá-lo sem uma tabela.
    titulo = f"{rotulo} — {' e '.join(partes)} contra o texto oficial"

    corpo = []
    if correcoes:
        n = len(correcoes)
        quantos = "Um registro" if n == 1 else f"São {n} registros"
        corpo.append(
            f"{quantos} cuja moldura ou espécie de pena "
            f"não correspondia ao que o diploma comina hoje: "
            f"{_frase_correcoes(correcoes)}. Cada correção foi conferida contra o "
            "texto compilado no Planalto, dispositivo a dispositivo.")
    if novas:
        corpo.append(
            f"Entram {_plural(len(novas), 'tipo', 'tipos')} que a lei prevê e o "
            "catálogo não registrava — dispositivos com pena própria e preceitos que "
            "cominam mais de uma pena, cada qual um tipo penal com sua própria página. "
            "Os campos que a lei não declara seguem regra ou herdam do caput do mesmo "
            "artigo, e é para eles que a revisão deve olhar primeiro.")
    corpo.append(
        "A conferência é semanal e determinística: baixa o texto compilado, lê as "
        "molduras e compara com o publicado. Onde não há leitura segura, o achado vira "
        "pergunta na triagem da semana em vez de virar dado.")

    ts = f"""import type {{ChangelogEntry}} from '../../types';

const entrada: ChangelogEntry = {{
  id: '{ident}',
  date: '{hoje}',
  title: {json.dumps(titulo, ensure_ascii=False)},
  summary:
    {json.dumps(f"Rodada automática do conferidor — {rotulo}: " + " e ".join(partes) + ", contra o texto compilado do Planalto.", ensure_ascii=False)},
  body: [
{chr(10).join('    ' + json.dumps(p, ensure_ascii=False) + ',' for p in corpo)}
  ],
  tipo: '{'correcao' if correcoes else 'novidade'}',
  areas: ['Tipos penais'],
  version: 'v{versao}',
}};

export default entrada;
"""
    return destino, ts


# ── Execução ────────────────────────────────────────────────────────────────
def aplicar(escolha: dict, versao: str, hoje: str, saida: Path) -> dict:
    if escolha["correcoes"]:
        corrigir.aplicar(escolha["correcoes"])
    if escolha["novas"]:
        criar.aplicar(escolha["novas"])

    destino, ts = entrada_changelog(escolha, versao, hoje)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # CRLF como o resto do repositório (as demais entradas são CRLF).
    destino.write_bytes(ts.replace("\n", "\r\n").encode("utf-8"))
    subir_versao(versao)

    fonte = escolha["fonte"]
    meta = {
        "fonte": fonte["id"],
        "rotulo": _rotulo(fonte),
        "correcoes": len(escolha["correcoes"]),
        "novas": len(escolha["novas"]),
        "humanos": len(escolha["humanos"]),
        "versao": versao,
        "ramo": f"conferidor/{fonte['id']}-{hoje}",
        "titulo": (f"fix(catalogo): {escolha['total']} ajuste(s) em "
                   f"{_rotulo(fonte)} conferidos com o texto compilado"),
        "entrada": str(destino if RAIZ not in destino.parents
                       else destino.relative_to(RAIZ)).replace("\\", "/"),
    }
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "corpo.md").write_text(corpo_pr(escolha, versao), encoding="utf-8", newline="\n")
    (saida / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8", newline="\n")
    return meta


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Monta a proposta da rodada do conferidor.")
    p.add_argument("--fonte", help="força o diploma (padrão: o de mais propostas)")
    p.add_argument("--com-novas", action="store_true",
                   help="também propõe linhas NOVAS (exige revisão de modelagem)")
    p.add_argument("--aplicar", action="store_true",
                   help="escreve no catálogo, no changelog e na versão")
    p.add_argument("--saida", default=str(RAIZ / "crawler" / "proposta"))
    args = p.parse_args()

    escolha = escolher(com_novas=args.com_novas, apenas=args.fonte)
    if escolha is None:
        print("nada mecânico nesta rodada — os achados restantes exigem decisão humana")
        return 1

    f = escolha["fonte"]
    print(f"{f['id']}: {len(escolha['correcoes'])} correção(ões), "
          f"{len(escolha['novas'])} linha(s) nova(s), "
          f"{len(escolha['humanos'])} para decisão humana")
    for x in escolha["correcoes"]:
        a, d = x["antes"], x["depois"]
        print(f"  corrige id {x['id']:5d} {a['artigo']:24s} {a['pena_min']}–{a['pena_max']} "
              f"→ {d['pena_min']}–{d['pena_max']} {d['tipo_pena']}")
    for x in escolha["novas"]:
        linha = x["linha"]
        print(f"  cria    id {linha['id']:5d} {linha['artigo']:24s} "
              f"{linha['pena_min']}–{linha['pena_max']} {linha['tipo_pena']}")

    versao = proxima_versao(versao_atual())
    if not args.aplicar:
        print(f"(simulação — nada foi escrito; fecharia a v{versao})")
        return 0

    meta = aplicar(escolha, versao, date.today().isoformat(), Path(args.saida))
    print(f"aplicado; ramo {meta['ramo']}, versão v{meta['versao']}, "
          f"corpo em {args.saida}/corpo.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
