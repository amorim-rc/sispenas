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
from pena_parser import ler_pena  # noqa: E402

SNAPSHOTS = RAIZ / "crawler" / "snapshots"
RELATORIOS = RAIZ / "crawler" / "relatorios"
CATALOGO = RAIZ / "static" / "data" / "crimes.json"
FONTES = RAIZ / "data" / "fontes.json"
EXCECOES = Path(__file__).resolve().parent / "excecoes.json"

# Tolerância na comparação de molduras: 1 dia. Abaixo disso é arredondamento da
# conversão para meses (o CP conta o mês como 30 dias), não divergência real.
TOLERANCIA_MESES = 1 / 30 + 1e-6


# ── Normalização de dispositivo ─────────────────────────────────────────────
_ART = re.compile(r"Art\.?\s*(\d+)(?:\s*[-–—]\s*([A-Z]))?", re.I)
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
    base = f"Art. {ma.group(1)}" + (f"-{ma.group(2)}" if ma.group(2) else "")
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
        if disp.situacao in ("revogado", "vetado"):
            achados.append({
                "tipo": "REVOGADO", "gravidade": 3, "chave": k,
                "ids": [x["id"] for x in linhas],
                "detalhe": f"a lei marca como {disp.situacao}"
                           f"{' — ' + disp.anotacao.texto if disp.anotacao else ''}",
            })
            continue

        pena = ler_pena(disp.pena_texto or disp.texto)
        if not pena:
            continue
        for linha in linhas:
            if dispensado(excecoes, fonte["id"], k, [linha["id"]]):
                continue
            cmin, cmax = moldura_catalogo(linha)
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
            else:
                difere = (abs(cmin - lmin) > TOLERANCIA_MESES
                          or abs(cmax - lmax) > TOLERANCIA_MESES)
            if difere:
                achados.append({
                    "tipo": "DIVERGENTE-moldura", "gravidade": 2, "chave": k,
                    "ids": [linha["id"]],
                    "detalhe": f"lei {lmin:g}–{lmax:g} × catálogo {cmin:g}–{cmax:g} "
                               f"(meses); texto: {(disp.pena_texto or '')[:90]}",
                })
            elif (pena["tipo"] and linha.get("tipo_pena")
                  and pena["tipo"].lower() not in linha["tipo_pena"].lower()):
                achados.append({
                    "tipo": "DIVERGENTE-tipo", "gravidade": 2, "chave": k,
                    "ids": [linha["id"]],
                    "detalhe": f"lei {pena['tipo']} × catálogo {linha['tipo_pena']}",
                })

    # 2) O que a lei tem com pena própria e o catálogo não registra.
    for d in dispositivos:
        if d.chave in do_catalogo or dispensado(excecoes, fonte["id"], d.chave):
            continue
        if d.situacao != "vigente":
            continue
        pena = ler_pena(d.pena_texto or "")
        if not pena or pena["so_multa"]:
            continue  # sem pena privativa própria não é linha do catálogo
        achados.append({
            "tipo": "AUSENTE", "gravidade": 1, "chave": d.chave,
            "ids": [],
            "detalhe": f"{(d.epigrafe or d.texto or '')[:70]} — "
                       f"{(d.pena_texto or '')[:70]}",
            "vigencia_pendente": d.vigencia_pendente,
        })

    for a in achados:
        a["fonte"] = fonte["id"]
    return achados


def montar_relatorio(por_fonte: dict[str, list[dict]]) -> str:
    total = sum(len(v) for v in por_fonte.values())
    hoje = date.today().isoformat()
    linhas = [f"# Conferidor — {hoje}", ""]
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

    relatorio = montar_relatorio(por_fonte)
    destino = Path(args.saida)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"{date.today().isoformat()}.md").write_text(relatorio, encoding="utf-8")
    (destino / f"{date.today().isoformat()}.json").write_text(
        json.dumps(por_fonte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total = sum(len(v) for v in por_fonte.values())
    print(relatorio if total <= 40 else
          f"{total} achados — relatório em {destino}/{date.today().isoformat()}.md")
    return 3 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
