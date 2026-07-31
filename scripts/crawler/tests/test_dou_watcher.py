# -*- coding: utf-8 -*-
"""Testes do watcher do DOU (F7) — sem rede.

A fixture `dou-2026-05-21.json` é um recorte REAL da listagem da Seção 1 do dia
em que saiu a Lei 15.410/2026 (a que acrescentou o inciso de violência doméstica
ao crime de tortura). Três itens, cada um travando uma decisão do filtro:

- a própria 15.410, que cita diploma monitorado;
- a Lei 15.409, cuja ementa não tem nada penal — o filtro não pode inventar;
- um despacho da ANEEL que diz "Revogar": vocabulário casado, espécie recusada.
  É o caso que garante que o watcher não afogue a issue em administrativo.
"""
import json
from pathlib import Path

from dou_watcher import (montar_relatorio, padrao_dos_diplomas, triar,
                         vocabulario_penal)

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
FONTES = Path(__file__).resolve().parents[3] / "data" / "fontes.json"


def carregar_itens():
    return json.loads((FIXTURES / "dou-2026-05-21.json").read_text(encoding="utf-8"))


def montar_filtro():
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))["fontes"]
    return padrao_dos_diplomas(fontes)


class TestPadraoDosDiplomas:
    """O padrão de citação nasce de `fontes.json` — crescer o registro é
    crescer o watcher, sem tocar no código."""

    def test_reconhece_diplomas_por_numero_com_e_sem_ponto(self):
        padrao, numeros = montar_filtro()
        assert padrao.search("altera a Lei nº 9.605, de 1998")
        assert padrao.search("altera a Lei 9605")
        assert padrao.search("o Decreto-Lei nº 2.848 (Código Penal)")

    def test_numero_solto_nao_casa(self):
        """Sem a espécie na frente, "9.605" é número de processo, de valor ou
        de portaria — casar isso encheria a issue de ruído."""
        padrao, _ = montar_filtro()
        assert not padrao.search("Processo nº 9.605/2026")
        assert not padrao.search("R$ 2.848,00")

    def test_mapeia_de_volta_para_o_id_da_fonte(self):
        _, numeros = montar_filtro()
        assert numeros["2848"] == "cp"
        assert numeros["11340"] == "maria-penha-11340"
        assert numeros["9455"] == "tortura-9455"


class TestVocabulario:
    def test_termos_penais(self):
        assert "reclusão" in vocabulario_penal("Pena - reclusão, de 2 a 5 anos")
        assert "revoga" in vocabulario_penal("Revogam-se os arts. 1º a 3º")

    def test_texto_sem_nada_penal(self):
        assert vocabulario_penal("Institui o Dia Nacional do Cooperativismo") == []


class TestTriagem:
    """Filtro largo, mas só sobre ato normativo."""

    def _triar(self, integral=""):
        padrao, numeros = montar_filtro()
        return triar(carregar_itens(), padrao, numeros, buscar_texto=lambda _: integral)

    def test_acha_a_lei_penal_da_semana(self):
        achadas = self._triar()
        titulos = [c["titulo"] for c in achadas]
        assert any("15.410" in t for t in titulos)
        lei = next(c for c in achadas if "15.410" in c["titulo"])
        assert "tortura-9455" in lei["diplomas_citados"]

    def test_ignora_despacho_mesmo_falando_em_revogar(self):
        """Espécie que não pode criar crime não entra: é o que mantém a lista
        com cinco itens por semana em vez de trezentos."""
        achadas = self._triar()
        assert not any("DESPACHO" in c["titulo"].upper() for c in achadas)

    def test_nao_inventa_candidata(self):
        """A Lei 15.409 (cadastro de condenados) não cita diploma monitorado nem
        traz vocabulário penal na ementa — sem o texto integral, fica de fora."""
        achadas = self._triar()
        assert not any("15.409" in c["titulo"] for c in achadas)

    def test_texto_integral_amplia_o_alcance(self):
        """O que a ementa esconde, o texto integral revela — por isso o watcher
        baixa a íntegra dos poucos atos normativos da semana."""
        achadas = self._triar(integral="Pena - reclusão, de 1 (um) a 4 (quatro) anos.")
        assert any("15.409" in c["titulo"] for c in achadas)


class TestRelatorio:
    def test_secao_vazia_diz_que_nao_ha_nada(self):
        from datetime import date
        texto = montar_relatorio([], date(2026, 5, 15), date(2026, 5, 22))
        assert "Nenhum ato normativo" in texto

    def test_lista_com_link_e_termos(self):
        from datetime import date
        padrao, numeros = montar_filtro()
        achadas = triar(carregar_itens(), padrao, numeros, buscar_texto=lambda _: "")
        texto = montar_relatorio(achadas, date(2026, 5, 15), date(2026, 5, 22))
        assert "15.410" in texto
        assert "in.gov.br/web/dou" in texto
        assert "tortura-9455" in texto
