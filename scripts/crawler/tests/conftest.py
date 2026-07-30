# -*- coding: utf-8 -*-
"""Deixa `scripts/crawler` importável e carrega as fixtures de HTML."""
import sys
from pathlib import Path

import pytest

CRAWLER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CRAWLER))
FIXTURES = CRAWLER / "fixtures"


@pytest.fixture
def carregar():
    """carregar('cp-art121') -> HTML congelado daquele trecho do Planalto."""
    def _ler(nome: str) -> str:
        return (FIXTURES / f"{nome}.html").read_text(encoding="utf-8")
    return _ler
