# -*- coding: utf-8 -*-
"""Baixa os textos compilados do Planalto (F1 do conferidor).

Lê `data/fontes.json`, busca cada diploma e grava um snapshot **normalizado em
UTF-8** em `crawler/snapshots/<id>/<AAAA-MM-DD>.html`, com `meta.json` ao lado.

Por que normalizar na entrada: o Planalto serve o mesmo acervo em codificações
diferentes — a maioria em windows-1252 **sem** `<meta charset>`, e algumas
páginas (p.ex. a Lei 11.340) em **UTF-16 LE com BOM**. Decodificar errado não
quebra: corrompe em silêncio e faz a página parecer desatualizada (foi o que
gerou o falso "o Planalto serve cópia velha" na F0). A detecção fica aqui, uma
vez só, e todo o resto do pipeline lê UTF-8.

A **sentinela** de cada fonte é a prova de frescor/integridade: uma string que
tem de existir na página (a emenda mais recente já conferida, quando há). Se
faltar, o download é rejeitado em vez de alimentar o conferidor com texto velho
ou truncado.

Uso:
    python scripts/crawler/baixar.py --todas
    python scripts/crawler/baixar.py --fonte cp --fonte cpm
    python scripts/crawler/baixar.py --listar

Saídas: 0 = tudo certo; 2 = alguma fonte falhou (rede, HTTP ou sentinela).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parent.parent.parent
FONTES = RAIZ / "data" / "fontes.json"
SNAPSHOTS = RAIZ / "crawler" / "snapshots"

# UA de navegador: sem ele o Planalto recusa a conexão (verificado na F0).
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
CORTESIA_S = 1.2   # intervalo entre requisições
TENTATIVAS = 3
TIMEOUT_S = 60


def decodificar(bruto: bytes) -> tuple[str, str]:
    """(texto, codificação detectada). BOM > meta charset > windows-1252.

    O cp1252 é o fallback certo: quase todo o acervo antigo do Planalto vem
    nele, sem declarar. Nunca usa 'replace' silencioso na tentativa preferida —
    só no último recurso, para não perder a página inteira por um byte torto.
    """
    if bruto.startswith(b"\xff\xfe") or bruto.startswith(b"\xfe\xff"):
        # O Planalto às vezes acrescenta um byte solto ao fim do UTF-16 (um
        # espaço), o que quebra a decodificação estrita por "truncated data".
        # Descartar o byte ímpar final é seguro: é lixo de borda, não conteúdo.
        corpo = bruto[:-1] if len(bruto) % 2 else bruto
        return corpo.decode("utf-16"), "utf-16"
    if bruto.startswith(b"\xef\xbb\xbf"):
        return bruto.decode("utf-8-sig"), "utf-8-sig"

    cabeca = bruto[:4096].decode("latin-1", errors="replace")
    m = re.search(r'charset=["\']?([\w-]+)', cabeca, re.I)
    if m:
        try:
            return bruto.decode(m.group(1)), m.group(1).lower()
        except (LookupError, UnicodeDecodeError):
            pass
    try:
        return bruto.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return bruto.decode("windows-1252", errors="replace"), "windows-1252"


def normalizar(texto: str) -> str:
    """Texto comparável: entidades de espaço viram espaço, espaços colapsam."""
    t = texto.replace("&nbsp;", " ").replace("\xa0", " ")
    return re.sub(r"\s+", " ", t)


def buscar(url: str) -> bytes:
    """GET com UA de navegador, com repetição e espera progressiva."""
    ultimo: Exception | None = None
    for tentativa in range(1, TENTATIVAS + 1):
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "pt-BR,pt;q=0.9",
        })
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ultimo = e
            if tentativa < TENTATIVAS:
                time.sleep(2 * tentativa)
    raise RuntimeError(f"falha após {TENTATIVAS} tentativas: {ultimo}")


def baixar_fonte(fonte: dict, destino: Path) -> dict:
    """Baixa, valida a sentinela e grava snapshot + meta. Devolve o resultado."""
    bruto = buscar(fonte["url"])
    texto, codificacao = decodificar(bruto)
    plano = normalizar(texto)

    sentinela = fonte.get("sentinela") or ""
    ok = sentinela.lower() in plano.lower() if sentinela else True

    dir_fonte = destino / fonte["id"]
    dir_fonte.mkdir(parents=True, exist_ok=True)
    arquivo = dir_fonte / f"{date.today().isoformat()}.html"
    arquivo.write_text(texto, encoding="utf-8")

    meta = {
        "id": fonte["id"],
        "url": fonte["url"],
        "baixado_em": date.today().isoformat(),
        "bytes_origem": len(bruto),
        "codificacao": codificacao,
        "sha256": hashlib.sha256(bruto).hexdigest(),
        "sentinela": sentinela,
        "sentinela_ok": ok,
        "arquivo": arquivo.name,
    }
    (dir_fonte / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def main() -> int:
    p = argparse.ArgumentParser(description="Baixa os compilados do Planalto.")
    p.add_argument("--fonte", action="append", default=[], metavar="ID",
                   help="id da fonte (repetível)")
    p.add_argument("--todas", action="store_true", help="baixa todas as fontes")
    p.add_argument("--listar", action="store_true", help="lista as fontes e sai")
    p.add_argument("--saida", default=str(SNAPSHOTS), help="diretório de saída")
    args = p.parse_args()

    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    if args.listar:
        for f in fontes:
            print(f"{f['id']:28s} {len(f['rotulos'])} rótulo(s)  {f['url']}")
        return 0

    alvo = fontes if args.todas else [f for f in fontes if f["id"] in set(args.fonte)]
    if not alvo:
        print("Nada a fazer: use --todas ou --fonte ID (veja --listar).")
        return 1

    destino = Path(args.saida)
    falhas: list[tuple[str, str]] = []
    for i, f in enumerate(alvo, 1):
        try:
            meta = baixar_fonte(f, destino)
        except Exception as e:                     # rede, HTTP, gravação
            falhas.append((f["id"], str(e)))
            print(f"[{i:2d}/{len(alvo)}] ✗ {f['id']:28s} {e}")
        else:
            if meta["sentinela_ok"]:
                print(f"[{i:2d}/{len(alvo)}] ✓ {f['id']:28s} "
                      f"{meta['bytes_origem']:8d}B  {meta['codificacao']}")
            else:
                falhas.append((f["id"], f"sentinela ausente: {meta['sentinela']!r}"))
                print(f"[{i:2d}/{len(alvo)}] ✗ {f['id']:28s} "
                      f"sentinela ausente: {meta['sentinela']!r} ({meta['codificacao']})")
        if i < len(alvo):
            time.sleep(CORTESIA_S)

    print(f"\n{len(alvo) - len(falhas)}/{len(alvo)} fontes íntegras.")
    if falhas:
        print("Falhas:")
        for fid, motivo in falhas:
            print(f"  {fid}: {motivo}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
