# -*- coding: utf-8 -*-
"""Testes do differ (F3): normalização de dispositivo e lista de exceções.

Os dois defeitos travados aqui produziram, cada um, dezenas de achados falsos na
primeira rodada — e falso positivo é o que mata um alerta semanal: em duas ou
três semanas ninguém mais lê o relatório.
"""
from conferir import chave, dispensado, moldura_catalogo


class TestChave:
    """O catálogo e a lei escrevem o mesmo dispositivo de formas diferentes."""

    def test_caput(self):
        assert chave("Art. 121, caput") == "Art. 121|caput"
        assert chave("Art. 121") == "Art. 121|caput"

    def test_paragrafo_em_varias_grafias(self):
        assert chave("Art. 121, §2º") == "Art. 121|§ 2º"
        assert chave("Art. 121, § 2o") == "Art. 121|§ 2º"
        assert chave("Art. 121, §2º-D") == "Art. 121|§ 2º-D"

    def test_paragrafo_unico_abreviado(self):
        """O catálogo abrevia "par. único"; a lei escreve por extenso. Sem as
        duas formas, essas linhas caíam no caput e eram comparadas com a moldura
        errada — sozinho, este defeito gerava ~57 achados falsos."""
        esperado = "Art. 121-B|parágrafo único"
        assert chave("Art. 121-B, par. único, I") == esperado
        assert chave("Art. 121-B, parágrafo único") == esperado

    def test_inciso_herda_o_paragrafo(self):
        """A pena é do parágrafo; o inciso só especializa a conduta."""
        assert chave("Art. 121, §2º, I") == "Art. 121|§ 2º"
        assert chave("Art. 1º, a") == "Art. 1|caput"

    def test_artigo_com_sufixo(self):
        assert chave("Art. 121-A, caput") == "Art. 121-A|caput"
        assert chave("Art. 359-M-A") == "Art. 359-M|caput"

    def test_sem_artigo(self):
        assert chave("") is None
        assert chave("Parágrafo único") is None


class TestExcecoes:
    EXC = [
        {"fonte": "cp", "chave": "Art. 158|§ 3º", "ids": [1068, 1069]},
        {"fonte": "lcp", "chave": "Art. 40|caput"},
    ]

    def test_dispensa_por_id(self):
        assert dispensado(self.EXC, "cp", "Art. 158|§ 3º", [1068])
        assert dispensado(self.EXC, "cp", "Art. 158|§ 3º", [1069])

    def test_linha_nova_no_mesmo_artigo_continua_aparecendo(self):
        """Exceção com `ids` não pode silenciar o dispositivo inteiro: uma
        divergência nova ali precisa continuar sendo reportada."""
        assert not dispensado(self.EXC, "cp", "Art. 158|§ 3º", [116])

    def test_dispensa_o_dispositivo_inteiro_sem_ids(self):
        assert dispensado(self.EXC, "lcp", "Art. 40|caput")
        assert dispensado(self.EXC, "lcp", "Art. 40|caput", [520])

    def test_nao_vaza_entre_diplomas(self):
        """Mesmo número de artigo em diploma diferente não é o mesmo crime."""
        assert not dispensado(self.EXC, "cpm", "Art. 158|§ 3º", [1068])


def test_moldura_usa_os_campos_canonicos():
    """`pena_min`/`pena_max` são os valores CRUS da fonte; a aplicação calcula
    com `pena_*_meses`, derivados do obs. Comparar os crus acusava divergência
    em registros corretos."""
    linha = {"pena_min": 0, "pena_max": 3, "pena_min_meses": 0.5, "pena_max_meses": 3.0}
    assert moldura_catalogo(linha) == (0.5, 3.0)


def test_moldura_cai_para_os_campos_crus_quando_nao_ha_derivado():
    assert moldura_catalogo({"pena_min": 24, "pena_max": 60}) == (24.0, 60.0)
