# -*- coding: utf-8 -*-
"""Testes do parser estrutural (F2).

As fixtures são trechos REAIS do Planalto, congelados. Cada teste corresponde a
uma armadilha levantada na revisão manual (v1.2.2–v1.2.13) ou na F0 — o objetivo
não é cobrir linhas, é impedir que essas armadilhas voltem em silêncio.
"""
import pytest

from parsear import ler_anotacao, parsear, como_dicionarios


def por_marcador(dispositivos, artigo):
    return {d["marcador"]: d for d in dispositivos if d["artigo"] == artigo}


# ── Anotações ───────────────────────────────────────────────────────────────
@pytest.mark.parametrize("texto, acao, norma, ano", [
    ("(Incluído pela Lei nº 15.384, de 2026)", "incluido", "Lei nº 15.384", 2026),
    ("(Redação dada pela Lei nº 14.994, de 2024)", "redacao", "Lei nº 14.994", 2024),
    ("(Revogado pela Lei nº 11.106, de 2005)", "revogado", "Lei nº 11.106", 2005),
    ("(Incluído pela Lei Complementar nº 224, de 2025)",
     "incluido", "Lei Complementar nº 224", 2025),
    # Data por extenso, sem "de AAAA" isolado — o ano é o último grupo de 4.
    ("(Redação dada pela Lei nº 6.416, de 24.5.1977)", "redacao", "Lei nº 6.416", 1977),
])
def test_le_acao_norma_e_ano(texto, acao, norma, ano):
    a = ler_anotacao(texto)
    assert (a.acao, a.norma, a.ano) == (acao, norma, ano)


def test_vide_nao_e_alteracao():
    assert ler_anotacao("(Vide Lei nº 4.611, de 1965)").acao == "vide"


def test_texto_sem_anotacao():
    assert ler_anotacao("Matar alguem:") is None


# ── CP, art. 121: sufixos, revogados e crime novo ───────────────────────────
def test_cp121_marcadores_exatos(carregar):
    d = por_marcador(como_dicionarios(parsear(carregar("cp-art121"))), "Art. 121")
    assert list(d) == ["caput", "§ 1º", "§ 2º", "§ 2º-A", "§ 2º-B", "§ 2º-C",
                       "§ 2º-D", "§ 3º", "§ 4º", "§ 5º", "§ 6º", "§ 7º"]


def test_cp121_caput(carregar):
    d = por_marcador(como_dicionarios(parsear(carregar("cp-art121"))), "Art. 121")
    assert "Matar alguem" in d["caput"]["texto"]
    assert "seis a vinte anos" in d["caput"]["pena_texto"]
    assert d["caput"]["epigrafe"] == "Homicídio simples"


def test_cp121_revogados_pela_14994(carregar):
    d = por_marcador(como_dicionarios(parsear(carregar("cp-art121"))), "Art. 121")
    for marcador in ("§ 2º-A", "§ 7º"):
        assert d[marcador]["situacao"] == "revogado"
        assert d[marcador]["anotacao"]["norma"] == "Lei nº 14.994"


def test_cp121_orgcrim_ultraviolenta_com_pena_propria(carregar):
    """§ 2º-D tem pena PRÓPRIA (20 a 40) — por isso virou linha no catálogo.

    O texto oficial traz um erro de digitação — "de 20 (vinte) a 40 (quarenta
    anos)", com o parêntese fechando no lugar errado. Serve de aviso ao extrator
    de pena da F3: confiar nos ALGARISMOS, nunca no número por extenso.
    """
    d = por_marcador(como_dicionarios(parsear(carregar("cp-art121"))), "Art. 121")
    disp = d["§ 2º-D"]
    assert disp["situacao"] == "vigente"
    assert disp["anotacao"] == {"acao": "incluido", "norma": "Lei nº 15.358", "ano": 2026}
    assert "de 20 (vinte) a 40 (quarenta" in disp["pena_texto"]


def test_cp_artigos_com_sufixo_sao_proprios(carregar):
    """121-A (feminicídio) e 121-B (vicaricídio) não podem colar no 121."""
    ds = como_dicionarios(parsear(carregar("cp-art121")))
    artigos = {d["artigo"] for d in ds}
    assert {"Art. 121", "Art. 121-A", "Art. 121-B"} <= artigos
    a121a = por_marcador(ds, "Art. 121-A")["caput"]
    assert a121a["anotacao"]["ano"] == 2024
    assert "20 (vinte) a 40 (quarenta) anos" in a121a["pena_texto"]


# ── Maria da Penha: versões sobrepostas SEM riscado ─────────────────────────
def test_mp24a_vale_a_redacao_mais_recente(carregar):
    """A pena de 2018 (detenção 3m-2a) aparece ANTES da de 2024 (reclusão 2-5),
    sem `<strike>`. Vale a anotação mais nova — é a regra que a F0 fixou."""
    d = por_marcador(como_dicionarios(parsear(carregar("mp-art24a"))), "Art. 24-A")
    pena = d["caput"]["pena_texto"]
    assert "reclusão" in pena and "2 (dois) a 5 (cinco) anos" in pena
    assert "detenção" not in pena
    assert d["caput"]["anotacao"]["norma"] == "Lei nº 14.994"


def test_mp24a_aumento_de_2026(carregar):
    d = por_marcador(como_dicionarios(parsear(carregar("mp-art24a"))), "Art. 24-A")
    assert d["§ 4º"]["anotacao"]["ano"] == 2026
    assert "monitoração" in d["§ 4º"]["texto"]


# ── Lei 9.605: parágrafos novos com letra ("§ 1º-B") ────────────────────────
def test_ambiental_art32_paragrafos_novos(carregar):
    d = por_marcador(como_dicionarios(parsear(carregar("amb-art32"))), "Art. 32")
    assert d["§ 1º-B"]["anotacao"]["ano"] == 2025   # tatuagem/piercing
    assert d["§ 1º-C"]["anotacao"]["ano"] == 2026   # desastre ambiental
    assert "detenção, de três meses a um ano" in d["caput"]["pena_texto"]


# ── CPM: pena só com teto e pena embutida no texto ─────────────────────────
def test_cpm290_pena_com_teto(carregar):
    """"até cinco anos" não tem mínimo explícito — o extrator da F3 precisa
    tratar isso como teto, não como ausência de pena."""
    d = por_marcador(como_dicionarios(parsear(carregar("cpm-art290"))), "Art. 290")
    assert "até cinco anos" in d["caput"]["pena_texto"]


def test_cpm290_pena_embutida_no_paragrafo(carregar):
    """O § 5º não tem linha "Pena –": a pena está na própria frase. O parser
    guarda o texto; caber  á à F3 procurar a pena ali quando `pena_texto` for
    nulo."""
    d = por_marcador(como_dicionarios(parsear(carregar("cpm-art290"))), "Art. 290")
    disp = d["§ 5º"]
    assert disp["pena_texto"] is None
    assert "reclusão de 5 (cinco) a 15 (quinze) anos" in disp["texto"]
    assert disp["anotacao"]["norma"] == "Lei nº 14.688"


# ── LCP: pena de multa em réis não é pena de prisão ─────────────────────────
def test_lcp32_pena_de_multa(carregar):
    """"multa, de duzentos mil réis a dois contos de réis" casaria um padrão de
    intervalo. O parser entrega o texto puro; o extrator da F3 tem de recusá-lo
    como pena privativa."""
    d = por_marcador(como_dicionarios(parsear(carregar("lcp-art32"))), "Art. 32")
    pena = d["caput"]["pena_texto"]
    assert "multa" in pena and "réis" in pena
    assert "detenção" not in pena and "reclusão" not in pena
