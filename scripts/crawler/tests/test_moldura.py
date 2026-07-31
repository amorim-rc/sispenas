# -*- coding: utf-8 -*-
"""A moldura é a autoridade: como ela é escrita e como é exibida.

Desde a v1.2.17 quem define a pena publicada é `pena_min`/`pena_max`, e não mais
o texto do `obs`. Estes testes protegem as duas garantias que essa inversão
exige: **dias exibidos exatamente como a lei os comina** e **número inteiro
escrito como inteiro**.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from transform_data import (  # noqa: E402
    _faixa_de_meses, _rotulo_de_meses, validar_moldura,
)


class TestDias:
    """O mês do art. 11 do CP tem 30 dias — a conversão precisa voltar exata."""

    @pytest.mark.parametrize("dias", range(1, 30))
    def test_ida_e_volta_de_todo_valor_em_dias(self, dias):
        """Guardamos meses; exibimos dias. Nenhum valor pode deslizar no caminho:
        "dez dias" jamais pode virar "9 dias" por arredondamento."""
        meses = round(dias / 30, 4)
        assert _rotulo_de_meses(meses) == f"{dias} {'dia' if dias == 1 else 'dias'}"

    @pytest.mark.parametrize("meses, esperado", [
        (0.1667, "5 dias"),    # os três valores sub-mensais que o catálogo usa
        (0.3333, "10 dias"),   # LCP art. 31: "dez dias a dois meses"
        (0.5, "15 dias"),      # LCP art. 34: "quinze dias a três meses"
    ])
    def test_valores_do_catalogo(self, meses, esperado):
        assert _rotulo_de_meses(meses) == esperado

    def test_faixa_mista_preserva_as_duas_unidades(self):
        assert _faixa_de_meses(0.5, 3) == "15 dias a 3 meses"
        assert _faixa_de_meses(0.3333, 2) == "10 dias a 2 meses"


class TestFaixa:
    @pytest.mark.parametrize("mn, mx, esperado", [
        (24, 60, "2 a 5 anos"),
        (72, 240, "6 a 20 anos"),
        (3, 12, "3 meses a 1 ano"),      # unidades diferentes: escreve as duas
        (1, 6, "1 a 6 meses"),
        (12, 12, "1 ano"),               # extremos iguais ainda assim legíveis
        (320, 720, "26 anos e 8 meses a 60 anos"),  # moldura com aumento
        (0, 3, "até 3 meses"),           # pena só com teto (LCP, CE)
        (0, 0, "—"),                     # sem pena privativa
    ])
    def test_rotulo(self, mn, mx, esperado):
        assert _faixa_de_meses(mn, mx) == esperado

    def test_um_ano_nao_vira_um_anos(self):
        assert _rotulo_de_meses(12) == "1 ano"
        assert _faixa_de_meses(6, 12) == "6 meses a 1 ano"


class TestValidacao:
    """A CI reprova moldura mal escrita — a regra vale para quem edita à mão e
    para o gerador automático de correções."""

    def test_float_inteiro_e_reprovado(self):
        problemas = validar_moldura([{"id": 1, "pena_min": 24.0, "pena_max": 60}])
        assert len(problemas) == 1 and "deve ser inteiro" in problemas[0]

    def test_fracao_legitima_passa(self):
        """0,5 mês são 15 dias: fração de verdade, não descuido de digitação."""
        assert validar_moldura([{"id": 1, "pena_min": 0.5, "pena_max": 3}]) == []

    def test_minimo_maior_que_maximo(self):
        problemas = validar_moldura([{"id": 1, "pena_min": 60, "pena_max": 24}])
        assert any("maior que" in p for p in problemas)

    def test_catalogo_real_esta_limpo(self):
        """Roda contra o catálogo publicado: nenhuma moldura mal formada."""
        import json
        fonte = Path(__file__).resolve().parents[3] / "data" / "crimes.json"
        assert validar_moldura(json.loads(fonte.read_text(encoding="utf-8"))) == []
