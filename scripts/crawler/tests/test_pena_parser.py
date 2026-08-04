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

class TestEspecieDePena:
    """Três classes de leitura que criaram "crime" onde não havia (v1.4.0)."""

    def test_pena_que_comeca_por_multa_e_so_multa(self):
        """O art. 254 do ECA é infração ADMINISTRATIVA: "Pena - multa …;
        duplicada em caso de reincidência a autoridade judiciária poderá
        determinar a suspensão da programação da emissora por até dois dias".
        Procurar a espécie antes de testar a multa lia "suspensão de dois dias"
        como pena privativa — e o catálogo ganhou "reclusão de até 2 dias"."""
        lida = ler_pena(
            "Pena - multa de vinte a cem salários de referência; duplicada em caso "
            "de reincidência a autoridade judiciária poderá determinar a suspensão "
            "da programação da emissora por até dois dias.")
        assert lida["so_multa"] is True
        assert lida["tipo"] is None

    def test_pagamento_de_dias_multa_e_pena_pecuniaria(self):
        """A fórmula de 1965 do Código Eleitoral: "Pena - pagamento de 250 a 300
        dias-multa". Não começa pela palavra "multa" — começa por "pagamento" —,
        e enquanto não era reconhecida `ler_penas` devolvia vazio: o conferidor
        PULAVA o dispositivo, e o registro ia para a conta dos indeterminados.

        Foi por esse silêncio que três artigos do CE publicaram pena privativa de
        liberdade — o 313 com reclusão de 2 a 6 anos, o 303 com detenção de 6
        meses a 2 anos e o 306 com 1 a 6 meses — para artigos que não cominam
        prisão nenhuma. Reconhecida a fórmula, o caso vira DIVERGENTE-moldura."""
        for texto in ("Pena - pagamento de 250 a 300 dias-multa.",
                      "Pena - pagamento de 15 a 30 dias-multa.",
                      "Pena – pagamento de 90 a 120 dias-multa."):
            lida = ler_pena(texto)
            assert lida is not None and lida["so_multa"] is True, texto
            assert lida["tipo"] is None

    def test_pagamento_de_dias_multa_junto_de_privativa_nao_e_so_multa(self):
        """A mesma lei escreve as duas formas. Onde há prisão, a moldura é dela:
        o art. 310 do CE comina "detenção até seis meses OU pagamento de 90 a 120
        dias-multa", e o art. 348, "reclusão de dois a seis anos e pagamento de
        15 a 30 dias-multa"."""
        lida = ler_pena("Pena - detenção até seis meses ou pagamento de 90 a 120 dias-multa.")
        assert lida["so_multa"] is False and lida["tipo"] == "detenção"
        assert lida["max_meses"] == 6.0
        lida = ler_pena("Pena - reclusão de dois a seis anos e pagamento de 15 a 30 dias-multa.")
        assert lida["so_multa"] is False and (lida["min_meses"], lida["max_meses"]) == (24.0, 72.0)

    def test_remissao_de_moldura_a_outra_lei_nao_e_pena_lida(self):
        """O art. 23-B da Lei 9.434/97 comina "as previstas no inciso XXIII do
        caput do art. 10 da Lei nº 6.437/1977" — que são sanções ADMINISTRATIVAS
        sanitárias. Não é pena criminal, e o parser não pode inventar uma."""
        assert ler_pena("Pena – as previstas no inciso XXIII do caput do art. 10 "
                        "da Lei nº 6.437, de 20 de agosto de 1977.") is None

    def test_multa_seguida_de_pena_privativa_continua_sendo_pena(self):
        """A ordem inversa existe e não pode ser confundida com só-multa."""
        lida = ler_pena("Pena - multa e detenção, de um a três anos.")
        assert lida["so_multa"] is False
        assert lida["tipo"] == "detenção"

    def test_especie_alternativa_e_uma_moldura_so(self):
        """O art. 306, § único, do CP comina "reclusão OU detenção, de um a três
        anos": uma moldura com duas espécies, não duas molduras. Separá-las fazia
        o differ acusar divergência de espécie e propor trocar reclusão por
        detenção num registro que estava certo."""
        from pena_parser import ler_penas
        molduras = ler_penas("Pena - reclusão ou detenção, de um a três anos, e multa.")
        assert len(molduras) == 1
        assert molduras[0]["tipos"] == ["reclusão", "detenção"]
        assert (molduras[0]["min_meses"], molduras[0]["max_meses"]) == (12.0, 36.0)

