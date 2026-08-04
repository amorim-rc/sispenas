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

from dou_watcher import (classificar, montar_relatorio, padrao_dos_diplomas, triar,
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


class TestNiveis:
    """O corte que fez a lista encolher, medido contra 14 dias reais de Seção 1.

    O filtro largo devolvia SEIS candidatas em 3.569 atos, e nenhuma trazia
    preceito secundário: uma lei sobre saúde mental na criança (por alterar o
    ECA), uma sobre fundo garantidor (pela palavra "revoga"), uma sobre
    honorários de advogado (por citar o Estatuto da OAB). Ler seis textos por
    semana sem achar nada é o jeito mais rápido de parar de ler."""

    def test_preceito_secundario_sem_diploma_monitorado_e_o_ponto_cego(self):
        nivel, _ = classificar("Art. 2º Constitui crime … Pena - reclusão, de 20 a 40 anos.",
                               "Tipifica os crimes de domínio social estruturado", [])
        assert nivel == "novo"

    def test_preceito_secundario_em_diploma_monitorado_e_antecedencia(self):
        nivel, _ = classificar("… passa a vigorar acrescida do seguinte art. 40-A. "
                               "Pena - reclusão, de 5 a 15 anos.", "Altera a Lei 11.343",
                               ["drogas-11343"])
        assert nivel == "monitorado"

    def test_alterar_diploma_monitorado_sem_pena_e_descartado(self):
        """Caso real: a Lei 15.413/2026 altera o ECA para dispor sobre saúde
        mental. Nada de penal — e o conferidor vê a página do ECA toda semana."""
        nivel, porque = classificar(
            "Altera a Lei nº 8.069, de 1990, para dispor sobre o direito da criança "
            "e do adolescente à saúde mental. … passa a vigorar acrescida",
            "dispõe sobre saúde mental", ["eca"])
        assert nivel == "descartado"
        assert "sem preceito penal" in porque

    def test_palavra_solta_sem_diploma_e_descartado(self):
        """"revoga" e "crime" aparecem em lei de fundo garantidor e de fundo
        penitenciário. Sozinhas não dizem nada."""
        for texto in ("Revoga a Lei nº 14.042, de 2020, para autorizar a União",
                      "destinação de recursos do Fundo para Aparelhamento … combate ao crime"):
            assert classificar(texto, "", [])[0] == "descartado"

    def test_revogacao_de_dispositivo_em_diploma_monitorado_sobe_de_nivel(self):
        """Revogar um tipo penal não deixa "Pena -" no texto do ato. Sem esta
        regra, a supressão de um crime passaria pelo corte."""
        nivel, _ = classificar("Revogam-se os arts. 12 e 13 da Lei nº 7.716, de 1989.",
                               "", ["racismo-7716"])
        assert nivel == "monitorado"

    def test_ementa_salva_o_nivel_1_quando_a_integra_nao_abre(self):
        """Se o texto integral não pôde ser lido, a ementa que anuncia o crime
        basta — falso negativo aqui custa meses de catálogo desatualizado."""
        nivel, _ = classificar("", "Tipifica o crime de perseguição digital", [])
        assert nivel == "novo"


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

    def test_descartado_e_nomeado_e_nao_escondido(self):
        """O corte não pode virar cegueira: o princípio do módulo é que falso
        negativo não se tolera. Quem foi descartado aparece em uma linha, com o
        motivo — três segundos de leitura, e o corte fica auditável."""
        from datetime import date
        padrao, numeros = montar_filtro()
        achadas = triar(carregar_itens(), padrao, numeros, buscar_texto=lambda _: "")
        texto = montar_relatorio(achadas, date(2026, 5, 15), date(2026, 5, 22))
        assert "Descartados" in texto
        assert "Sentinelas a conferir" in texto
