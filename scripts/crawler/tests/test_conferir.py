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
        # Sufixo duplo e sufixo depois do ordinal: as duas formas que o parser
        # antes achatava no artigo-base, deixando sem conferência a injúria
        # racial (Lei 7.716, art. 2º-A) e a violação de prerrogativa de advogado
        # (Lei 8.906, art. 7º-B).
        assert chave("Art. 359-M-A") == "Art. 359-M-A|caput"
        assert chave("Art. 2º-A") == "Art. 2-A|caput"
        assert chave("Art. 7º-B, caput") == "Art. 7-B|caput"
        # Hífen de pontuação não é sufixo.
        assert chave("Art. 13 - O resultado") == "Art. 13|caput"

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


class TestMoldurasDeChapeau:
    """O conferidor desce ao inciso quando o dispositivo não tem pena própria."""

    def test_desce_ao_inciso_quando_o_dispositivo_nao_tem_moldura(self, carregar):
        from parsear import parsear
        from conferir import molduras_de
        d = {x.chave: x for x in parsear(carregar("cp-art197-pena-por-inciso"))}
        molduras = molduras_de(d["Art. 197|caput"])
        assert [(m["min_meses"], m["max_meses"]) for m in molduras] == [(1.0, 12.0),
                                                                       (3.0, 12.0)]

    def test_pena_do_proprio_dispositivo_manda_sobre_a_do_inciso(self, carregar):
        """Onde o caput comina a pena e os incisos só qualificam a conduta, quem
        manda é o caput: descer ali produziria molduras que ninguém cominou."""
        from parsear import parsear
        from conferir import molduras_de
        d = {x.chave: x for x in parsear(carregar("lavagem-art1-redacao"))}
        molduras = molduras_de(d["Art. 1|caput"])
        assert len(molduras) == 1
        assert (molduras[0]["min_meses"], molduras[0]["max_meses"]) == (36.0, 120.0)

    def test_le_o_texto_do_inciso_quando_a_pena_vem_embutida(self, carregar):
        """No CP, art. 157, § 3º, a pena não é linha "Pena –": está dentro do
        inciso ("morte, a pena é de reclusão, de 24 a 30 anos"). É preciso ler o
        texto do inciso, não só a linha de pena dele."""
        from parsear import parsear
        from conferir import molduras_de
        d = {x.chave: x for x in parsear(carregar("cpm-art400-graus"))}
        molduras = molduras_de(d["Art. 400|caput"])
        assert len(molduras) == 2


class TestDistancia:
    """Só entram na conta as pontas que a LEI escreveu."""

    def test_ponta_aberta_nao_conta_como_zero(self):
        """A moldura de piso aberto (fórmula de graus do CPM) tem max_meses 0.
        Somá-lo como se fosse a pena punha o registro do art. 400 a 360 da
        moldura certa e a 96 da de outro crime — e o differ acusava divergência
        entre dispositivos que nada têm um com o outro."""
        from conferir import distancia
        piso = {"min_meses": 240.0, "max_meses": 0.0, "piso_apenas": True}
        outra = {"min_meses": 144.0, "max_meses": 360.0, "piso_apenas": False}
        assert distancia(piso, 240.0, 360.0) < distancia(outra, 240.0, 360.0)

    def test_teto_aberto_ignora_o_piso(self):
        from conferir import distancia
        teto = {"min_meses": 0.0, "max_meses": 60.0, "teto_apenas": True}
        assert distancia(teto, 12.0, 60.0) == 0.0

    def test_moldura_fechada_compara_as_duas_pontas(self):
        from conferir import distancia
        m = {"min_meses": 12.0, "max_meses": 48.0}
        assert distancia(m, 12.0, 48.0) == 0.0
        assert distancia(m, 6.0, 48.0) == 6.0


class TestTravaDeCobertura:
    """O que o conferidor não garante não pode crescer em silêncio.

    Um registro que SAI da conferência não aparece como divergente: aparece
    como nada. Foi assim que três incisos do art. 151 do CP e os doze crimes do
    Código de Trânsito ficaram anos sem uma única comparação com a lei. Contar
    o silêncio é o que o torna visível — e travar a conta é o que impede a
    próxima lacuna do parser de reabrir o mesmo buraco.
    """

    def _limites(self, tmp_path, monkeypatch, limites):
        import json
        import conferir
        arq = tmp_path / "cobertura-limites.json"
        arq.write_text(json.dumps({"limites": limites}), encoding="utf-8")
        monkeypatch.setattr(conferir, "LIMITES", arq)

    def test_estavel_nao_reclama(self, tmp_path, monkeypatch):
        from conferir import conferir_limites
        self._limites(tmp_path, monkeypatch, {"ilegivel": 2, "pena_derivada": 85})
        assert conferir_limites({"ilegivel": 2, "pena_derivada": 85}) == ([], [])

    def test_crescer_e_regressao(self, tmp_path, monkeypatch):
        from conferir import conferir_limites
        self._limites(tmp_path, monkeypatch, {"ilegivel": 2})
        regressoes, _ = conferir_limites({"ilegivel": 5})
        assert len(regressoes) == 1
        assert "3 a mais" in regressoes[0]

    def test_encolher_convida_a_apertar(self, tmp_path, monkeypatch):
        from conferir import conferir_limites
        self._limites(tmp_path, monkeypatch, {"ilegivel": 2})
        regressoes, folgas = conferir_limites({"ilegivel": 0})
        assert regressoes == []
        assert "dá para baixar" in folgas[0]

    def test_motivo_nao_declarado_e_regressao(self, tmp_path, monkeypatch):
        """Um motivo novo que aparece sozinho é exatamente o caso perigoso: sem
        esta regra, bastaria o classificador inventar um rótulo para que uma
        leva de registros saísse da conferência por baixo de todos os tetos."""
        from conferir import conferir_limites
        self._limites(tmp_path, monkeypatch, {"ilegivel": 2})
        regressoes, _ = conferir_limites({"ilegivel": 2, "motivo_novo": 9})
        assert any("nem consta dos limites" in r for r in regressoes)

    def test_sem_arquivo_de_limites_nao_quebra(self, tmp_path, monkeypatch):
        import conferir
        monkeypatch.setattr(conferir, "LIMITES", tmp_path / "nao-existe.json")
        assert conferir.conferir_limites({"ilegivel": 99}) == ([], [])


class TestClassificacaoDoNaoConferido:
    """"Indeterminado" não é motivo: é a confissão de que ninguém sabe."""

    class _Disp:
        def __init__(self, texto="", pena_texto=""):
            self.texto, self.pena_texto = texto, pena_texto

    def test_pena_importada(self):
        from conferir import _por_referencia
        d = self._Disp(texto="Na mesma pena incorre quem:")
        assert _por_referencia(d, {}) == "pena_importada"

    def test_pena_derivada(self):
        from conferir import _por_referencia
        d = self._Disp(texto="A pena é aumentada de 1/3 (um terço) até a metade se")
        assert _por_referencia(d, {}) == "pena_derivada"

    def test_norma_explicativa_nao_e_preceito(self):
        from conferir import _por_referencia
        d = self._Disp(texto="Equipara-se à coisa móvel a energia elétrica ou qualquer "
                             "outra que tenha valor econômico")
        assert _por_referencia(d, {}) == "sem_preceito_proprio"

    def test_texto_com_pena_que_nao_foi_lida_e_o_alarme(self):
        from conferir import _por_referencia
        d = self._Disp(pena_texto="Pena - reclusão em fórmula que o parser não conhece")
        assert _por_referencia(d, {}) == "ilegivel"

    def test_registro_sem_pena_privativa_vem_antes_de_tudo(self):
        from conferir import _por_referencia
        d = self._Disp(pena_texto="Pena - reclusão, de 1 a 4 anos")
        assert _por_referencia(d, {"tem_pena_privativa": False}) == "sancao_nao_privativa"
