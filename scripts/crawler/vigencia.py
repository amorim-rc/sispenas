# -*- coding: utf-8 -*-
"""Quando a alteração passa a valer (F4).

Uma lei publicada não é uma lei em vigor. A revisão manual quase caiu nessa duas
vezes: a **Lei 15.190/2025** (licenciamento ambiental) só passou a valer 180 dias
depois de publicada, e a **LC 224/2025** produz efeitos a partir de 1º/01/2026.
Corrigir o catálogo antes disso seria publicar como vigente o que ainda não é —
o oposto do que o projeto promete.

Este módulo lê a cláusula final de vigência de uma lei e responde: **em que data
ela passa (ou passou) a valer?** Achados de norma ainda não vigente vão para uma
seção própria do relatório, com a data — não somem, mas também não viram patch.

As funções são puras (recebem texto). O download fica em `baixar.py`, para que
os testes rodem sem rede.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta

MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}
_EXTENSO_DIAS = {
    "trinta": 30, "sessenta": 60, "noventa": 90, "cento e oitenta": 180,
    "cento e vinte": 120, "um ano": 365, "dois anos": 730,
}

_PUBLICACAO = re.compile(
    rf"\bDE\s+(\d{{1,2}})\s*[ºo°]?\s+DE\s+({'|'.join(MESES)})\s+DE\s+(\d{{4}})", re.I)
_IMEDIATA = re.compile(r"entra em vigor na data (?:de sua|da) publica", re.I)
_VACATIO = re.compile(
    r"entra em vigor ap[óo]s decorridos?\s+(\d+)\s*(?:\([^)]*\))?\s*dias", re.I)
_VACATIO_EXTENSO = re.compile(
    rf"entra em vigor ap[óo]s decorridos?\s+({'|'.join(_EXTENSO_DIAS)})\s+dias", re.I)
_DATA_CERTA = re.compile(
    rf"(?:a partir de|em)\s+(\d{{1,2}})\s*[ºo°]?\s+de\s+({'|'.join(MESES)})\s+de\s+(\d{{4}})",
    re.I)


@dataclass
class Vigencia:
    publicacao: date | None
    inicio: date | None          # quando passa a valer
    clausula: str                # trecho que fundamentou a leitura
    incerta: bool = False        # não foi possível determinar com segurança

    def vigente_em(self, quando: date) -> bool:
        """Na dúvida, responde True: um achado suprimido por engano é pior que
        um achado a mais — o relatório é revisado por humano de qualquer modo."""
        return True if self.inicio is None else quando >= self.inicio


def ler_publicacao(texto: str) -> date | None:
    """Data do cabeçalho: "LEI Nº 15.190, DE 8 DE AGOSTO DE 2025"."""
    m = _PUBLICACAO.search(texto)
    if not m:
        return None
    try:
        return date(int(m.group(3)), MESES[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None


def analisar(texto: str) -> Vigencia:
    """Interpreta cabeçalho + cláusula de vigência de uma lei."""
    publicacao = ler_publicacao(texto)

    m = _VACATIO.search(texto) or _VACATIO_EXTENSO.search(texto)
    if m:
        bruto = m.group(1)
        dias = int(bruto) if bruto.isdigit() else _EXTENSO_DIAS[bruto.lower()]
        inicio = publicacao + timedelta(days=dias) if publicacao else None
        return Vigencia(publicacao, inicio, m.group(0), incerta=publicacao is None)

    # "produzirá efeitos a partir de 1º de janeiro de 2026" — a lei entra em
    # vigor na publicação, mas os dispositivos só valem na data indicada.
    if re.search(r"produzir[áa] efeitos", texto, re.I):
        md = _DATA_CERTA.search(texto)
        if md:
            try:
                inicio = date(int(md.group(3)), MESES[md.group(2).lower()],
                              int(md.group(1)))
                return Vigencia(publicacao, inicio, md.group(0))
            except ValueError:
                pass
        # Há produção de efeitos diferida, mas em termo que não sabemos ler
        # ("primeiro dia do quarto mês subsequente"): marcar como incerta.
        return Vigencia(publicacao, None, "produção de efeitos diferida",
                        incerta=True)

    if _IMEDIATA.search(texto):
        return Vigencia(publicacao, publicacao, _IMEDIATA.search(texto).group(0),
                        incerta=publicacao is None)

    return Vigencia(publicacao, None, "cláusula de vigência não localizada",
                    incerta=True)


def url_da_lei(norma: str, ano: int) -> str | None:
    """URL provável do texto da lei-reforma no Planalto.

    Só cobre 2023+ — que é o alcance de interesse: alteração antiga já está em
    vigor, e o custo de errar a URL de uma lei velha não se justifica.
    """
    m = re.search(r"([\d.]+)$", (norma or "").strip())
    if not m or ano < 2023:
        return None
    numero = m.group(1).replace(".", "")
    tipo = "lcp/Lcp" if "complementar" in (norma or "").lower() else "lei/L"
    if "complementar" in (norma or "").lower():
        return f"https://www.planalto.gov.br/ccivil_03/leis/{tipo}{numero}.htm"
    return (f"https://www.planalto.gov.br/ccivil_03/_ato2023-2026/{ano}/"
            f"{tipo}{numero}.htm")


def main() -> int:
    """CLI: `python scripts/crawler/vigencia.py "Lei nº 15.190" 2025`.

    Útil na triagem — antes de corrigir o catálogo por causa de uma lei nova,
    confirmar que ela já vale. O download fica aqui, e não nas funções puras,
    para que os testes rodem sem rede.
    """
    import argparse
    import sys
    from datetime import date as _date

    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    from baixar import buscar, decodificar, normalizar  # noqa: E402
    from parsear import paragrafos  # noqa: E402

    p = argparse.ArgumentParser(description="Diz desde quando uma lei vale.")
    p.add_argument("norma", help='ex.: "Lei nº 15.190"')
    p.add_argument("ano", type=int)
    args = p.parse_args()

    url = url_da_lei(args.norma, args.ano)
    if not url:
        print(f"Sem URL conhecida para {args.norma} ({args.ano}) — anterior a 2023?")
        return 1
    texto = normalizar(" ".join(x.texto for x in paragrafos(decodificar(buscar(url))[0])))
    v = analisar(texto)
    hoje = _date.today()
    print(f"{args.norma} ({args.ano})  {url}")
    print(f"  publicação : {v.publicacao}")
    print(f"  em vigor   : {v.inicio or '(indeterminado)'}"
          f"{'  ⚠ leitura incerta' if v.incerta else ''}")
    print(f"  cláusula   : {v.clausula[:100]}")
    print(f"  vale hoje? : {'SIM' if v.vigente_em(hoje) else 'NÃO — não corrigir ainda'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
