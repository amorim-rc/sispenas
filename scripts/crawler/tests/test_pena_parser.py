# -*- coding: utf-8 -*-
"""Testes do extrator de pena compartilhado (F3).

Cada caso veio de um texto REAL do Planalto que já enganou — ou enganaria — uma
leitura ingênua. O extrator é usado dos dois lados (catálogo e conferidor), então
um erro aqui vira divergência falsa no relatório semanal.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # scripts/
from pena_parser import ler_pena, parse_pena_range  # noqa: E402


@pytest.mark.parametrize("texto, minimo, maximo", [
    # CP de 1940 escreve a moldura por extenso.
    ("Pena - reclusão, de seis a vinte anos.", 72, 240),
    # Erro de digitação NO TEXTO OFICIAL (art. 121, § 2º-D): o parêntese fecha
    # depois da unidade — "40 (quarenta anos)". Apagar o parêntese inteiro
    # levaria a unidade junto e tornaria a moldura ilegível.
    ("Pena – reclusão, de 20 (vinte) a 40 (quarenta anos).", 240, 480),
    ("Pena – reclusão, de 2 (dois) a 5 (cinco) anos, e multa.", 24, 60),
    ("Pena - detenção, de três meses a um ano, e multa.", 3, 12),
    ("Pena – prisão simples, de quinze dias a três meses, ou multa.", 0.5, 3),
    # Dias-multa é pena pecuniária: não pode virar tempo de prisão.
    ("Pena - reclusão de 3 (três) a 10 (dez) anos e multa de 500 a 1.500 dias-multa.",
     36, 120),
    # Pena embutida na frase, sem linha "Pena –" (CPM, art. 290, § 5º).
    ("Tratando-se de tráfico de drogas, a pena será de reclusão de 5 (cinco) a "
     "15 (quinze) anos.", 60, 180),
])
def test_le_moldura(texto, minimo, maximo):
    lido = ler_pena(texto)
    assert lido is not None, texto
    assert (lido["min_meses"], lido["max_meses"]) == (minimo, maximo)


def test_pena_so_com_teto():
    """"até cinco anos" (CPM, art. 290) não declara mínimo — mas tem pena."""
    lido = ler_pena("Pena - reclusão, até cinco anos.")
    assert lido["teto_apenas"] is True
    assert (lido["min_meses"], lido["max_meses"]) == (0.0, 60.0)


def test_multa_em_reis_nao_e_pena_privativa():
    """A LCP comina "multa, de duzentos mil réis a dois contos de réis": há
    intervalo no texto, mas não há prisão. Confundir os dois foi o que produziu
    o registro errado do art. 32 no catálogo."""
    lido = ler_pena("Pena – multa, de duzentos mil réis a dois contos de réis.")
    assert lido["so_multa"] is True
    assert lido["tipo"] is None
    assert lido["max_meses"] == 0.0


def test_texto_sem_pena():
    assert ler_pena("Dirigir sem a devida habilitação:") is None
    assert ler_pena("") is None


def test_compatibilidade_com_o_catalogo():
    """`parse_pena_range` é o que o transform_data usa há versões; o refactor
    da F3 não pode ter mudado seu comportamento."""
    assert parse_pena_range("6 meses a 1 ano detenção") == (6, "meses", 1, "anos")
    assert parse_pena_range("1-5 anos reclusão") == (1, "anos", 5, "anos")
    assert parse_pena_range("2 a 5 anos") == (2, "anos", 5, "anos")
    assert parse_pena_range("sem faixa aqui") is None


class TestMultiplasMolduras:
    """Um preceito com duas penas são DOIS tipos penais, não um.

    O art. 254 do CP comina "reclusão, de três a seis anos… no caso de dolo, ou
    detenção, de seis meses a dois anos, no caso de culpa". Ler só uma delas
    apagaria a outra do catálogo; ler a errada trocaria a pena de uma pela da
    outra — foi o que quase entrou num PR automático.
    """

    def test_dolosa_e_culposa_no_mesmo_preceito(self):
        from pena_parser import ler_penas
        molduras = ler_penas(
            "Pena - reclusão, de três a seis anos, e multa, no caso de dolo, ou "
            "detenção, de seis meses a dois anos, no caso de culpa.")
        assert [(m["tipo"], m["min_meses"], m["max_meses"]) for m in molduras] == [
            ("reclusão", 36.0, 72.0), ("detenção", 6.0, 24.0)]

    def test_preceito_simples_devolve_uma(self):
        from pena_parser import ler_penas
        assert len(ler_penas("Pena – reclusão, de 2 (dois) a 5 (cinco) anos, e multa.")) == 1

    def test_a_moldura_do_caput_e_a_primeira(self):
        """`ler_pena` (singular) tem de devolver a pena do CAPUT — a que aparece
        primeiro —, e não a que casar primeiro num padrão mais específico."""
        lida = ler_pena(
            "Pena - reclusão, de três a seis anos, e multa, no caso de dolo, ou "
            "detenção, de seis meses a dois anos, no caso de culpa.")
        assert (lida["tipo"], lida["min_meses"], lida["max_meses"]) == ("reclusão", 36.0, 72.0)
