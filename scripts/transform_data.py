#!/usr/bin/env python3
"""
Enriquece o catálogo de tipos penais (crimes.json).

Deriva campos estruturados a partir do texto legal para permitir filtros
combinados por modalidade de pena e cálculo de benefícios penais:

  - pena_privativa : Reclusão | Detenção | Prisão simples | Nenhuma
  - tem_multa      : bool  (multa cumulada OU alternativa OU isolada)
  - multa_regime   : cumulativa | alternativa | isolada | nenhuma
  - infracao_menor_potencial : bool (pena máx <= 2 anos -> JECRIM)

Todos os campos derivados são heurísticos (regex sobre `obs`/`artigo`) e
serão revisados individualmente. Correções finas ficam em CORRECOES (abaixo).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "crimes.json"
OUT = ROOT / "static" / "data" / "crimes.json"

PENA_PRIVATIVA_MAP = {
    "Reclusão": "Reclusão",
    "Detenção": "Detenção",
    "Prisão simples": "Prisão simples",
    "Multa": "Nenhuma",
    "—": "Nenhuma",
    "": "Nenhuma",
    None: "Nenhuma",
}

# padrões negativos que NÃO indicam pena de multa criminal
NEG_MULTA = re.compile(r"sem multa|multa reparat|reparação do dano", re.IGNORECASE)

# Correções manuais (revisão do usuário). Sobrepõem a heurística e retiram o
# registro da lista de casos ambíguos.
CORRECOES = {
    # Art. 227 CP (caput): a multa só incide na hipótese do §3º (fim de lucro);
    # o tipo-base não comina multa.
    176: {"tem_multa": False, "multa_regime": "nenhuma"},
    898: {"tem_multa": False, "multa_regime": "nenhuma"},
}


# ── Unidades de pena (dias / meses / anos) ──────────────────────────────────
# Fator de conversão para MESES (unidade canônica de cálculo). O CP conta o mês
# como 30 dias (Art. 11), então 1 dia = 1/30 mês e 1 ano = 12 meses.
UNIDADE_EM_MESES = {"dias": 1 / 30, "meses": 1.0, "anos": 12.0}
_NOMES_UNIDADE = {"dias": ("dia", "dias"), "meses": ("mês", "meses"), "anos": ("ano", "anos")}


def _norm_unidade(u: str) -> str:
    u = u.lower()
    if u.startswith("d"):
        return "dias"
    if u.startswith("a"):
        return "anos"
    return "meses"  # mês / mes / meses


def _rotulo(valor: float, unidade: str) -> str:
    inteiro = int(valor) if float(valor).is_integer() else valor
    sing, plur = _NOMES_UNIDADE[unidade]
    return f"{inteiro} {sing if inteiro == 1 else plur}"


def _meses(valor: float, unidade: str) -> float:
    return round(valor * UNIDADE_EM_MESES[unidade], 4)


_U = r"(dias?|meses|m[eê]s|anos?)"
RANGE_2U = re.compile(rf"(\d+)\s*{_U}\s*a\s*(\d+)\s*{_U}", re.IGNORECASE)
RANGE_1U = re.compile(rf"(\d+)\s*(?:a|-|–|—)\s*(\d+)\s*{_U}", re.IGNORECASE)
ABBR = re.compile(r"(\d+)\s*([dma])\s*(?:-|a|–|—)\s*(\d+)\s*([dma])", re.IGNORECASE)
_ABBR_U = {"d": "dias", "m": "meses", "a": "anos"}


def parse_pena_range(obs: str):
    """Extrai o primeiro intervalo de pena do texto -> (vmin, umin, vmax, umax).

    Reconhece "15 dias a 6 meses", "1-5 anos", "2 a 5 anos", "3m-1a". Retorna
    None se nada for encontrado. O primeiro match corresponde ao caput.
    """
    text = obs or ""
    m = RANGE_2U.search(text)
    if m:
        return int(m.group(1)), _norm_unidade(m.group(2)), int(m.group(3)), _norm_unidade(m.group(4))
    m = RANGE_1U.search(text)
    if m:
        u = _norm_unidade(m.group(3))
        return int(m.group(1)), u, int(m.group(2)), u
    m = ABBR.search(text)
    if m:
        return int(m.group(1)), _ABBR_U[m.group(2).lower()], int(m.group(3)), _ABBR_U[m.group(4).lower()]
    return None


def _rotulo_de_meses(meses: float) -> str:
    """Rótulo de fallback quando não há intervalo parseável (usa pena_* em meses)."""
    if meses <= 0:
        return "—"
    if meses < 1:
        return _rotulo(round(meses * 30), "dias")
    if float(meses).is_integer() and meses % 12 == 0:
        return _rotulo(int(meses // 12), "anos")
    return _rotulo(int(meses) if float(meses).is_integer() else round(meses, 1), "meses")


def derivar_pena(c: dict):
    """Define rótulos de exibição e valores canônicos em meses.

    Campos adicionados:
      pena_min_meses / pena_max_meses  -> float (unidade de cálculo)
      pena_min_rotulo / pena_max_rotulo -> str (exibição com unidade natural)
      pena_unidade_derivada -> bool (True se veio do parser do texto)
    """
    parsed = parse_pena_range(c.get("obs", ""))
    if parsed is not None:
        vmin, umin, vmax, umax = parsed
        c["pena_min_meses"] = _meses(vmin, umin)
        c["pena_max_meses"] = _meses(vmax, umax)
        c["pena_min_rotulo"] = _rotulo(vmin, umin)
        c["pena_max_rotulo"] = _rotulo(vmax, umax)
        c["pena_unidade_derivada"] = True
        if umin == umax:
            sing, plur = _NOMES_UNIDADE[umax]
            c["pena_faixa_rotulo"] = f"{vmin} a {vmax} {sing if vmax == 1 else plur}"
        else:
            c["pena_faixa_rotulo"] = f"{c['pena_min_rotulo']} a {c['pena_max_rotulo']}"
    else:
        mn = float(c.get("pena_min") or 0)
        mx = float(c.get("pena_max") or 0)
        c["pena_min_meses"] = round(mn, 4)
        c["pena_max_meses"] = round(mx, 4)
        c["pena_min_rotulo"] = _rotulo_de_meses(mn)
        c["pena_max_rotulo"] = _rotulo_de_meses(mx)
        c["pena_unidade_derivada"] = False
        if mx <= 0:
            c["pena_faixa_rotulo"] = "—"
        elif c["pena_min_rotulo"] == "—":
            c["pena_faixa_rotulo"] = f"até {c['pena_max_rotulo']}"
        else:
            c["pena_faixa_rotulo"] = f"{c['pena_min_rotulo']} a {c['pena_max_rotulo']}"


def detect_multa(obs: str, tipo_pena: str):
    """Retorna (tem_multa, regime, ambiguo, motivo)."""
    text = obs or ""
    low = text.lower()

    if tipo_pena == "Multa":
        return True, "isolada", False, ""

    has_word = "multa" in low
    if not has_word:
        return False, "nenhuma", False, ""

    ambiguo = False
    motivo = ""
    if NEG_MULTA.search(text):
        ambiguo = True
        motivo = "menção a multa possivelmente não-criminal (ex.: 'sem multa'/'multa reparatória')"

    # cumulativa: "e multa", "+ multa", ", multa", "dias-multa" (multa cumulada,
    # inclusive Lei 11.343/06: "reclusão + 500-1.500 dias-multa")
    if re.search(r"(?:\be\s+multa|\+[^.;]*multa|,\s*multa|e,?\s*multa|dias-multa)", low):
        return True, "cumulativa", ambiguo, motivo
    # alternativa: "ou multa"
    if re.search(r"\bou\s+multa", low):
        return True, "alternativa", ambiguo, motivo
    # menção genérica -> tratar como cumulativa mas marcar ambíguo
    ambiguo = True
    if not motivo:
        motivo = "menção a 'multa' sem conector claro (e/ou) — regime presumido"
    return True, "cumulativa", ambiguo, motivo


def main():
    crimes = json.loads(SRC.read_text(encoding="utf-8"))
    review_rows = []

    for c in crimes:
        tipo = c.get("tipo_pena")
        c["pena_privativa"] = PENA_PRIVATIVA_MAP.get(tipo, "Nenhuma")
        tem_multa, regime, ambiguo, motivo = detect_multa(c.get("obs"), tipo)
        correcao = CORRECOES.get(c["id"])
        if correcao is not None:
            tem_multa = correcao["tem_multa"]
            regime = correcao["multa_regime"]
            ambiguo = False
            c["multa_revisado"] = True
        c["tem_multa"] = tem_multa
        c["multa_regime"] = regime
        c["derivado_auto"] = True

        derivar_pena(c)
        pmax = c["pena_max_meses"]
        c["infracao_menor_potencial"] = bool(pmax and pmax <= 24)

        if ambiguo:
            review_rows.append(
                (c["id"], c["lei"], c["artigo"], c["crime"], regime, motivo, (c.get("obs") or "")[:120])
            )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(crimes, ensure_ascii=False, indent=1), encoding="utf-8")

    # Estatísticas
    from collections import Counter
    priv = Counter(c["pena_privativa"] for c in crimes)
    multa = Counter(c["multa_regime"] for c in crimes)
    print("pena_privativa:", dict(priv))
    print("multa_regime:", dict(multa))
    print("tem_multa=True:", sum(1 for c in crimes if c["tem_multa"]))
    print("ambiguos remanescentes:", len(review_rows))
    print("correções manuais aplicadas:", sum(1 for c in crimes if c.get("multa_revisado")))
    print("escrito em:", OUT)


if __name__ == "__main__":
    main()
