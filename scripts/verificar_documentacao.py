# -*- coding: utf-8 -*-
"""Saúde da documentação: quem envelheceu, e por quê.

A conferência semanal vigia o dado. Este script vigia a **prosa**, com a mesma
lógica: um documento não é confiável só porque existe — é confiável enquanto o
que ele descreve não mudou.

Duas perguntas, por documento:

1. **Passou da cadência?** Noventa dias, por padrão. É o piso: documento que
   ninguém relê há um trimestre merece uma olhada, mesmo que nada tenha mudado.
2. **Mudou algo de que ele fala?** Cada documento declara suas dependências em
   `data/documentacao.json`. Se um arquivo dependente foi commitado DEPOIS da
   última conferência, o documento vence — mesmo dentro do prazo.

A segunda pergunta é a que importa. Na revisão de 01/08/2026, a convenção C7 do
`CONTRIBUTING.md` ainda mandava escrever a pena no campo `obs`; a regra tinha
sido invertida meses antes, no `transform_data.py`, e o prazo do documento nem
havia corrido. Prazo é relógio; dependência é sinal.

Editar o documento conta como conferi-lo: a data efetiva é a maior entre o
`conferido_em` do registro e o último commit do próprio arquivo. Assim só há
escrituração manual quando alguém relê e **não** encontra o que corrigir.

Uso:
    python scripts/verificar_documentacao.py            # relatório
    python scripts/verificar_documentacao.py --md       # em markdown, p/ a issue

Saídas: 0 = tudo em dia; 2 = erro; 3 = há documento vencido.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "data" / "documentacao.json"


def commit_mais_recente(caminho: str) -> date | None:
    """Data do último commit que tocou o caminho (arquivo ou diretório)."""
    try:
        saida = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", caminho],
            cwd=RAIZ, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    bruto = saida.stdout.strip()
    if not bruto:
        return None
    return datetime.fromisoformat(bruto).date()


def avaliar(registro: dict, hoje: date | None = None) -> list[dict]:
    """Um veredito por documento, com o motivo do vencimento."""
    hoje = hoje or date.today()
    cadencia = registro.get("cadencia_padrao_dias", 90)
    veredito = []
    for doc in registro["documentos"]:
        arquivo = doc["arquivo"]
        declarado = date.fromisoformat(doc["conferido_em"])
        proprio = commit_mais_recente(arquivo)
        # Editar é conferir: quem mexeu no texto o leu.
        efetivo = max(declarado, proprio) if proprio else declarado

        atrasadas = []
        for dep in doc.get("depende_de", []):
            quando = commit_mais_recente(dep)
            if quando and quando > efetivo:
                atrasadas.append((dep, quando))

        dias = (hoje - efetivo).days
        limite = doc.get("cadencia_dias", cadencia)
        veredito.append({
            "arquivo": arquivo,
            "sobre": doc.get("sobre", ""),
            "conferido_em": efetivo.isoformat(),
            "dias": dias,
            "vencido_por_prazo": dias > limite,
            "dependencias_mudaram": [
                {"arquivo": d, "em": q.isoformat()} for d, q in sorted(atrasadas)],
            "existe": (RAIZ / arquivo).exists(),
        })
    return veredito


def desatualizados(veredito: list[dict]) -> list[dict]:
    return [v for v in veredito
            if v["vencido_por_prazo"] or v["dependencias_mudaram"] or not v["existe"]]


def montar_relatorio(veredito: list[dict]) -> str:
    vencidos = desatualizados(veredito)
    L = ["## Saúde da documentação", ""]
    if not vencidos:
        L += [f"Os {len(veredito)} documentos registrados estão em dia — nenhum passou "
              "da cadência e nenhuma dependência mudou desde a última conferência.", ""]
        return "\n".join(L) + "\n"

    L += [f"**{len(vencidos)}** de {len(veredito)} documento(s) a reler.", "",
          "> Vencer não quer dizer que esteja errado: quer dizer que ninguém confirmou "
          "que continua certo. Ao reler e nada mudar, atualize `conferido_em` em "
          "`data/documentacao.json`; ao corrigir, o próprio commit responde.", ""]
    for v in vencidos:
        L.append(f"### `{v['arquivo']}`")
        L.append("")
        if not v["existe"]:
            L += ["- ⚠️ **arquivo não existe** — registro órfão em `data/documentacao.json`", ""]
            continue
        L.append(f"- {v['sobre']}")
        L.append(f"- conferido pela última vez em {v['conferido_em']} ({v['dias']} dias)")
        if v["vencido_por_prazo"]:
            L.append("- **passou da cadência**")
        for dep in v["dependencias_mudaram"]:
            L.append(f"- **mudou depois disso:** `{dep['arquivo']}` (em {dep['em']})")
        L.append("")
    return "\n".join(L) + "\n"


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Verifica a saúde da documentação.")
    p.add_argument("--md", action="store_true", help="imprime o relatório em markdown")
    p.add_argument("--saida", help="grava o markdown neste arquivo")
    args = p.parse_args()

    registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
    veredito = avaliar(registro)
    relatorio = montar_relatorio(veredito)

    if args.saida:
        Path(args.saida).write_text(relatorio, encoding="utf-8")
    if args.md or args.saida:
        print(relatorio)
    else:
        for v in veredito:
            marca = "!" if (v["vencido_por_prazo"] or v["dependencias_mudaram"]) else "."
            print(f"{marca} {v['arquivo']:45s} {v['conferido_em']}  "
                  f"{v['dias']:4d}d  deps atrasadas: {len(v['dependencias_mudaram'])}")
    return 3 if desatualizados(veredito) else 0


if __name__ == "__main__":
    raise SystemExit(main())
