# -*- coding: utf-8 -*-
"""Testes de vigência e de revogação total (F4).

Os dois casos que a revisão manual encontrou na marra estão aqui: a lei com
vacatio de 180 dias (15.190/2025) e a que produz efeitos em data futura
(LC 224/2025). Corrigir o catálogo antes dessas datas publicaria como vigente
o que ainda não era.
"""
from datetime import date
from pathlib import Path

import pytest

import revogacao
from vigencia import Vigencia, analisar, ler_publicacao, url_da_lei

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def texto(nome: str) -> str:
    return (FIXTURES / f"{nome}.txt").read_text(encoding="utf-8")


class TestVigencia:
    def test_vacatio_de_180_dias(self):
        """Lei 15.190/2025: publicada em 8/8/2025, em vigor só em ~5/2/2026.
        Foi a que quase entrou cedo demais no catálogo."""
        v = analisar(texto("vigencia-15190-vacatio180"))
        assert v.publicacao == date(2025, 8, 8)
        assert v.inicio == date(2026, 2, 4)
        assert not v.vigente_em(date(2025, 12, 1))
        assert v.vigente_em(date(2026, 7, 30))

    def test_vigencia_imediata(self):
        v = analisar(texto("vigencia-15410-imediata"))
        assert v.publicacao == date(2026, 5, 20)
        assert v.inicio == date(2026, 5, 20)
        assert v.vigente_em(date(2026, 5, 20))
        assert not v.vigente_em(date(2026, 5, 19))

    def test_producao_de_efeitos_diferida(self):
        """LC 224/2025 entra em vigor na publicação, mas os dispositivos só
        produzem efeitos depois — o que vale para o catálogo é a segunda data."""
        v = analisar(texto("vigencia-lc224-efeitos"))
        assert v.publicacao == date(2025, 12, 26)
        assert v.inicio == date(2026, 1, 1) or v.incerta

    def test_cabecalho_com_ordinal(self):
        assert ler_publicacao("LEI Nº 9.999, DE 1º DE MARÇO DE 2024") == date(2024, 3, 1)

    def test_sem_clausula_assume_vigente(self):
        """Na dúvida o achado APARECE: suprimir por engano é pior que reportar
        a mais, já que o relatório passa por revisão humana."""
        v = analisar("Texto qualquer sem cláusula.")
        assert v.incerta and v.vigente_em(date(2026, 7, 30))


class TestUrlDaLei:
    def test_lei_ordinaria(self):
        assert url_da_lei("Lei nº 15.410", 2026).endswith("/2026/lei/L15410.htm")

    def test_lei_complementar(self):
        assert "lcp/Lcp224" in url_da_lei("Lei Complementar nº 224", 2025)

    def test_ignora_lei_antiga(self):
        """Alteração de 2015 já está em vigor: não vale gastar requisição."""
        assert url_da_lei("Lei nº 13.146", 2015) is None


class TestRevogacaoTotal:
    def test_banner_no_topo(self):
        achado = revogacao.detectar(
            "LEI Nº 7.802, DE 11 DE JULHO DE 1989 "
            "(Revogada pela Lei nº 14.785, de 2023) Dispõe sobre agrotóxicos")
        assert achado.revogado and "14.785" in achado.indicio

    def test_anotacao_de_artigo_nao_conta(self):
        """"Revogado pela Lei" no meio do articulado é anotação de dispositivo,
        não do diploma — por isso a busca se limita ao topo."""
        corpo = "x" * 4000 + " Art. 32 (Revogado pela Lei nº 11.106, de 2005)"
        assert not revogacao.detectar(corpo).revogado

    @pytest.mark.parametrize("ultimo, esperado", [(2023, False), (1998, True), (None, True)])
    def test_envelhecimento(self, ultimo, esperado):
        assert revogacao.envelhecido(ultimo, 2026) is esperado
