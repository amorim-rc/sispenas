# -*- coding: utf-8 -*-
"""Detecção de revogação TOTAL de um diploma (F4).

A armadilha que custou caro na revisão manual: a **Lei 7.802/89** (agrotóxicos)
foi inteiramente revogada pela Lei 14.785/2023, e a página da lei antiga **não
anuncia isso** em lugar nenhum do articulado — o scan de anotações "(Revogado
pela Lei…)" artigo a artigo é cego a esse caso. Só apareceu porque a lei nova
era conhecida.

Três verificações, em ordem de custo (o LexML foi testado na F0 e descartado:
a página por URN não traz o metadado, e a API SRU está atrás de challenge):

1. **Banner no topo** — quando existe, o Planalto o imprime antes do articulado;
2. **Watcher do DOU** (F7) — a lei revogadora nova cita o diploma revogado, e é
   por ali que o caso futuro chega;
3. **Envelhecimento** — diploma sem nenhuma alteração há muitos anos vira
   lembrete de conferência manual esporádica. Não é sinal de revogação: é
   admissão de que este módulo não tem como saber.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Só o topo do documento: mais abaixo, "Revogado pela Lei" é anotação de artigo,
# não do diploma inteiro.
TOPO_CHARS = 3000
_BANNER = re.compile(
    r"(Revogad[oa]s?\s+(?:tacitamente\s+)?pel[ao]\s+"
    r"(?:Lei|Lei Complementar|Decreto-Lei|Medida Provis[óo]ria)[^)\n]{0,60})", re.I)
_VIGENCIA_ENCERRADA = re.compile(r"(Vig[êe]ncia\s+encerrada|Revogada\s+em)", re.I)


@dataclass
class Revogacao:
    revogado: bool
    indicio: str | None = None


def detectar(texto_do_topo: str) -> Revogacao:
    """Procura, no início do documento, o aviso de revogação do diploma."""
    topo = (texto_do_topo or "")[:TOPO_CHARS]
    m = _BANNER.search(topo) or _VIGENCIA_ENCERRADA.search(topo)
    return Revogacao(bool(m), m.group(1).strip() if m else None)


def envelhecido(ultimo_ano: int | None, hoje_ano: int, limite: int = 15) -> bool:
    """Diploma sem alteração há mais de `limite` anos.

    Não indica revogação — indica que nenhum sinal automático o alcança, e que
    uma conferência humana esporádica vale a pena. A Lei 7.802/89 estava assim
    quando foi revogada por completo.
    """
    if ultimo_ano is None:
        return True
    return (hoje_ano - ultimo_ano) > limite
