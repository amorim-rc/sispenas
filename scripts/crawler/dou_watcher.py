# -*- coding: utf-8 -*-
"""Filtro semanal do Diário Oficial, Seção 1 — sem IA (F7).

O conferidor releu os 62 diplomas de `data/fontes.json` e é cego para uma coisa
só: **lei penal nova e autônoma**, que ainda não está em página nenhuma que ele
vigie. Este módulo cobre exatamente esse ponto cego, e nada além dele.

Como funciona, em três passos:

1. **Só atos normativos.** A Seção 1 publica ~330 atos por dia, e mais de 90%
   são portaria e despacho, que não criam crime (legalidade estrita: só lei em
   sentido formal). Restam ~5 por semana — poucos o bastante para baixar o
   texto INTEGRAL de cada um, em vez de filtrar pelo resumo truncado que a
   listagem traz.
2. **Dois filtros, união e não interseção**: (A) cita um diploma monitorado —
   o padrão vem de `fontes.json`, então crescer o registro é crescer o watcher;
   (B) tem vocabulário penal ("reclusão", "detenção", "pena de", "revoga"…).
3. **Saída para leitura humana.** Uma seção na issue semanal, com o que casou.
   Nada entra em lugar nenhum automaticamente.

**Falso positivo é aceitável; falso negativo, não.** Uma lei tributária que
menciona "pena de multa" entrar na lista custa dez segundos de leitura; uma lei
penal nova passar batida custa meses de catálogo desatualizado. Por isso o
filtro é largo e a lista, curta.

Uso:
    python scripts/crawler/dou_watcher.py                    # 8 dias até hoje
    python scripts/crawler/dou_watcher.py --data 2026-06-12 --dias 3
    python scripts/crawler/dou_watcher.py --saida crawler/relatorios

Saídas: 0 = nada a olhar; 2 = erro de execução; 3 = há candidatas.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
FONTES = RAIZ / "data" / "fontes.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tempo import hoje  # noqa: E402

RELATORIOS = RAIZ / "crawler" / "relatorios"

LISTAGEM = "https://www.in.gov.br/leiturajornal?secao={secao}&data={data}"
ARTIGO = "https://www.in.gov.br/web/dou/-/{slug}"
# Sem Accept/Accept-Language de navegador o in.gov.br devolve 403 — só o
# User-Agent não basta (o Planalto, no baixar.py, se contenta com o UA).
CABECALHOS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}
PAUSA = 1.2                      # s entre requisições: ~15 por rodada

# Seção 1 e sua edição EXTRA — é na extra que sai a lei sancionada às pressas.
SECOES = ("do1", "do1e")

# Espécies que podem criar ou revogar crime. Decreto e portaria não podem
# (art. 5º, XXXIX, da Constituição), e é o que faz o volume desabar.
ESPECIES = re.compile(
    r"^(Lei|Lei\s+Complementar|Lei\s+Delegada|Medida\s+Provis[óo]ria|"
    r"Decreto-Lei|Emenda\s+Constitucional)$", re.IGNORECASE)

VOCABULARIO = [
    "reclusão", "detenção", "prisão simples", "pena de", "pena –", "pena -",
    "pena:", "revoga", "passa a vigorar acrescido", "passa a vigorar acrescida",
    "código penal", "crime", "contravenção", "tipifica",
]

_PARAMS = re.compile(r'<script[^>]*id="params"[^>]*>(.*?)</script>', re.S)
_TEXTO_DOU = re.compile(r'<div[^>]*class="[^"]*texto-dou[^"]*"[^>]*>(.*?)</div>\s*</div>',
                        re.S)
_TAG = re.compile(r"(?s)<[^>]+>")


# ── Rede ────────────────────────────────────────────────────────────────────
def baixar(url: str, tentativas: int = 2) -> str | None:
    """HTML da página, ou None quando a data não tem edição (404/500)."""
    for tentativa in range(tentativas):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=CABECALHOS), timeout=60) as r:
                bruto = r.read()
            # O in.gov.br anuncia UTF-8 e cumpre; o fallback existe porque o
            # acervo oficial brasileiro tem histórico de misturar codificação.
            try:
                return bruto.decode("utf-8")
            except UnicodeDecodeError:
                return bruto.decode("cp1252", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 500):
                return None      # dia sem edição daquela seção
            if tentativa + 1 == tentativas:
                raise
        except (urllib.error.URLError, TimeoutError):
            if tentativa + 1 == tentativas:
                raise
        time.sleep(PAUSA * 3)
    return None


def _limpar(html: str) -> str:
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(_TAG.sub(" ", html))).strip()


def listar(dia: date, secao: str) -> list[dict]:
    """Atos publicados naquele dia e seção (o JSON que a própria página carrega)."""
    pagina = baixar(LISTAGEM.format(secao=secao, data=dia.strftime("%d-%m-%Y")))
    if not pagina:
        return []
    m = _PARAMS.search(pagina)
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("jsonArray", []) or []
    except json.JSONDecodeError:
        return []


def texto_integral(slug: str) -> str:
    """Texto do ato. Vazio quando a página não abre — o resumo cobre a falta."""
    pagina = baixar(ARTIGO.format(slug=slug))
    if not pagina:
        return ""
    m = _TEXTO_DOU.search(pagina)
    return _limpar(m.group(1)) if m else ""


# ── Filtros ─────────────────────────────────────────────────────────────────
def padrao_dos_diplomas(fontes: list[dict]) -> tuple[re.Pattern, dict[str, str]]:
    """Expressão que reconhece a citação de qualquer diploma monitorado.

    Os números saem da URL do compilado, não do rótulo: `del2848compilado.htm`
    dá 2848, `l10.826compilado.htm` dá 10826, `lcp64.htm` dá 64. É o único campo
    que TODO diploma tem e que carrega o número — rótulos como "CP" ou "ECA"
    não carregam.
    """
    numeros: dict[str, str] = {}
    for f in fontes:
        base = f["url"].rsplit("/", 1)[-1]
        base = re.sub(r"(compilado|orig)?\.html?$", "", base, flags=re.I)
        m = re.search(r"(\d[\d.]*)", base)
        if not m:
            continue
        numeros[m.group(1).replace(".", "").lstrip("0")] = f["id"]

    # "Lei nº 9.605", "Lei 9605", "Decreto-Lei nº 2.848" — a espécie na frente é
    # o que impede casar número de processo, de CNPJ ou de valor.
    alternativas = "|".join(
        rf"{n[:-3]}\.?{n[-3:]}" if len(n) > 3 else n
        for n in sorted(numeros, key=len, reverse=True))
    padrao = re.compile(
        r"(?:Leis?|Lei\s+Complementar|Decretos?-Leis?|Decreto-Lei)\s*"
        r"(?:n[ºo°.\s]*)?\s*(" + alternativas + r")\b", re.IGNORECASE)
    return padrao, numeros


def vocabulario_penal(texto: str) -> list[str]:
    baixo = texto.lower()
    return [t for t in VOCABULARIO if t in baixo]


def triar(itens: list[dict], padrao: re.Pattern, numeros: dict[str, str],
          buscar_texto=texto_integral) -> list[dict]:
    """Atos normativos que casam o filtro A (citação) ou o B (vocabulário)."""
    candidatas: list[dict] = []
    for item in itens:
        if not ESPECIES.match((item.get("artType") or "").strip()):
            continue
        resumo = " ".join(filter(None, [item.get("title"), item.get("content")]))
        integral = buscar_texto(item.get("urlTitle", "")) or ""
        texto = f"{resumo} {integral}"

        citados = sorted({numeros[m.group(1).replace(".", "").lstrip("0")]
                          for m in padrao.finditer(texto)
                          if m.group(1).replace(".", "").lstrip("0") in numeros})
        termos = vocabulario_penal(texto)
        if not citados and not termos:
            continue
        candidatas.append({
            "titulo": (item.get("title") or "").strip(),
            "especie": (item.get("artType") or "").strip(),
            "data": item.get("pubDate") or "",
            "url": ARTIGO.format(slug=item.get("urlTitle", "")),
            "diplomas_citados": citados,
            "termos": termos[:8],
            "integral": bool(integral),
            "ementa": (item.get("content") or "")[:300],
        })
    return candidatas


# ── Relatório ───────────────────────────────────────────────────────────────
def montar_relatorio(candidatas: list[dict], inicio: date, fim: date) -> str:
    L = [f"## DOU — normas possivelmente penais ({inicio:%d/%m} a {fim:%d/%m})", ""]
    if not candidatas:
        L += ["Nenhum ato normativo da Seção 1 casou o filtro penal nesta janela.", ""]
        return "\n".join(L) + "\n"

    L += [
        f"**{len(candidatas)}** ato(s) normativo(s) a olhar. O filtro é largo de "
        "propósito: perder lei penal nova custa caro, ler um falso positivo custa "
        "dez segundos.", "",
        "Se alguma criar ou alterar crime em diploma que o conferidor ainda não "
        "vigia, acrescente o diploma em `data/fontes.json` — dali em diante ele "
        "passa a ser conferido toda semana.", "",
    ]
    for c in candidatas:
        L.append(f"### {c['titulo']}")
        L.append("")
        L.append(f"- {c['especie']}, {c['data']} — <{c['url']}>")
        if c["diplomas_citados"]:
            L.append(f"- **Cita diploma monitorado:** {', '.join(c['diplomas_citados'])}")
        if c["termos"]:
            L.append(f"- **Vocabulário penal:** {', '.join(c['termos'])}")
        if not c["integral"]:
            L.append("- ⚠️ texto integral não pôde ser lido; a triagem usou só a ementa")
        L.append(f"- Ementa: {c['ementa']}")
        L.append("")
    return "\n".join(L) + "\n"


def rodar(fim: date, dias: int) -> list[dict]:
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    padrao, numeros = padrao_dos_diplomas(fontes)

    itens: list[dict] = []
    vistos: set[str] = set()
    for i in range(dias):
        dia = fim - timedelta(days=i)
        for secao in SECOES:
            for item in listar(dia, secao):
                slug = item.get("urlTitle") or ""
                if slug in vistos:
                    continue
                vistos.add(slug)
                itens.append(item)
            time.sleep(PAUSA)
    return triar(itens, padrao, numeros)


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Filtra o DOU em busca de lei penal nova.")
    p.add_argument("--data", help="fim da janela (AAAA-MM-DD); padrão: hoje")
    p.add_argument("--dias", type=int, default=8,
                   help="tamanho da janela; 8 cobre a semana e o atraso do cron")
    p.add_argument("--saida", default=str(RELATORIOS))
    args = p.parse_args()

    fim = date.fromisoformat(args.data) if args.data else hoje()
    inicio = fim - timedelta(days=args.dias - 1)
    candidatas = rodar(fim, args.dias)

    relatorio = montar_relatorio(candidatas, inicio, fim)
    destino = Path(args.saida)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"dou-{fim.isoformat()}.md").write_text(relatorio, encoding="utf-8")
    (destino / f"dou-{fim.isoformat()}.json").write_text(
        json.dumps(candidatas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(relatorio)
    return 3 if candidatas else 0


if __name__ == "__main__":
    raise SystemExit(main())
