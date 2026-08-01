# -*- coding: utf-8 -*-
"""A data de Brasília — a única que o projeto usa para nomear rodada.

O runner do GitHub Actions roda em UTC, e `date.today()` lá é a data UTC. Na
rodada agendada (05:00 de Brasília, 08:00 UTC) as duas coincidem; numa execução
manual do fim da tarde, não: às 21:00 do dia 31 já é dia 1º em UTC, e a issue
saiu datada de amanhã. Como o relatório, o nome do arquivo e o título da issue
precisam bater entre si, a data vem daqui — e o workflow usa `TZ=America/Sao_Paulo`
pelo mesmo motivo.

Brasília é UTC−3 fixo desde que o horário de verão acabou (2019), então o
deslocamento constante basta e não é preciso base de fusos.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

BRASILIA = timezone(timedelta(hours=-3))


def hoje() -> date:
    """A data corrente em Brasília, independente do fuso da máquina."""
    return datetime.now(BRASILIA).date()
