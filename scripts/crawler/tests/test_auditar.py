# -*- coding: utf-8 -*-
"""Testes da auditoria de classificação (hediondez, ação penal, nome).

Aqui não há fixture de HTML: o que se testa é a REGRA — a tabela do rol, o
casamento por dispositivo e as decisões de não acusar. O acesso ao texto
compilado é substituído por dublês, porque a rodada semanal já exercita a
leitura real.
"""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "scripts"))
import auditar  # noqa: E402


def registro(**campos):
    base = {"id": 1, "lei": "CP", "artigo": "Art. 121, caput", "crime": "Homicídio",
            "hediondo": "Não", "acao": "Pública Incondicionada"}
    return {**base, **campos}


class TestHediondez:
    """A tabela é a lei transcrita; o teste garante que a leitura dela não muda."""

    def _achados(self, catalogo, monkeypatch, impressao="igual"):
        tabela = json.loads((RAIZ / "data" / "hediondos.json").read_text(encoding="utf-8"))
        monkeypatch.setattr(auditar, "_impressao", lambda *a, **k: tabela["impressao_do_texto"]
                            if impressao == "igual" else "outra")
        return auditar.auditar_hediondez(catalogo)

    def test_qualificado_e_hediondo_e_simples_nao(self, monkeypatch):
        achados = self._achados([
            registro(id=1, artigo="Art. 121, §2º, I", hediondo="Sim"),
            registro(id=2, artigo="Art. 155, caput", hediondo="Não"),
        ], monkeypatch)
        assert not [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]

    def test_acusa_o_que_esta_no_rol_e_marcado_como_nao(self, monkeypatch):
        """O roubo com restrição da liberdade entrou no rol em 2019 (Pacote
        Anticrime); o catálogo trazia "Não" desde antes."""
        achados = self._achados([registro(id=9, artigo="Art. 157, §2º, V")], monkeypatch)
        div = [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]
        assert len(div) == 1 and div[0]["para"] == "Sim"
        assert "8.072" in div[0]["fundamento"]

    def test_acusa_o_que_esta_marcado_sim_e_fora_do_rol(self, monkeypatch):
        achados = self._achados([registro(id=9, artigo="Art. 171, caput",
                                          crime="Estelionato", hediondo="Sim")], monkeypatch)
        div = [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]
        assert len(div) == 1 and div[0]["para"] == "Não"

    def test_trafico_privilegiado_e_excecao_jurisprudencial(self, monkeypatch):
        """O §4º do art. 33 não é equiparado (STF, HC 118.533) — e a exceção tem
        de vencer a regra do tráfico, não o contrário."""
        achados = self._achados([
            registro(id=9, lei="Lei 11.343/06", artigo="Art. 33, §4º", hediondo="Não"),
        ], monkeypatch)
        assert not [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]

    def test_condicional_nao_acusa_em_nenhuma_direcao(self, monkeypatch):
        """Onde a hediondez depende do caso — organização criminosa direcionada a
        crime hediondo —, tanto Sim quanto Não podem estar certos."""
        achados = self._achados([
            registro(id=9, lei="Lei 12.850/13", artigo="Art. 2º", hediondo="Sim"),
            registro(id=10, lei="Lei 12.850/13", artigo="Art. 2º, §1º", hediondo="Não"),
        ], monkeypatch)
        assert not [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]
        assert [a for a in achados if a["tipo"] == "DEPENDE-DO-CASO"]

    def test_cpm_fica_fora_do_alcance(self, monkeypatch):
        achados = self._achados([
            registro(id=9, lei="CPM (DL 1.001/69)", artigo="Art. 205", hediondo="Sim"),
        ], monkeypatch)
        assert not [a for a in achados if a["tipo"] == "HEDIONDEZ-DIVERGENTE"]
        assert [a for a in achados if a["tipo"] == "FORA-DE-ALCANCE"]

    def test_mudanca_no_rol_alerta_antes_de_qualquer_achado(self, monkeypatch):
        """Se a Lei 8.072 mudar, a tabela envelheceu — e os achados dela passam a
        valer menos que o alerta."""
        achados = self._achados([registro()], monkeypatch, impressao="diferente")
        alerta = [a for a in achados if a["tipo"] == "ROL-ALTERADO"]
        assert alerta and alerta[0]["gravidade"] == 3


class TestAcaoPenal:
    def _com_texto(self, texto, monkeypatch):
        class Falso:
            def __init__(self, t):
                self.texto, self.epigrafe, self.citacao, self.incisos = t, None, False, []
        monkeypatch.setattr(auditar, "dispositivos_de",
                            lambda fid: {"Art. 151|caput": Falso(texto)})
        return {"CP": "cp"}

    def test_representacao_no_artigo_indica_condicionada(self, monkeypatch):
        indice = self._com_texto("Devassar indevidamente o conteúdo de correspondência "
                                 "fechada. Somente se procede mediante representação.",
                                 monkeypatch)
        achados = auditar.auditar_acao_penal(
            [registro(id=5, artigo="Art. 151, caput")], indice)
        assert achados and achados[0]["para"] == "Pública Condicionada"

    def test_silencio_da_lei_e_regra_do_art_100(self, monkeypatch):
        indice = self._com_texto("Matar alguém.", monkeypatch)
        assert not auditar.auditar_acao_penal(
            [registro(id=5, artigo="Art. 151, caput")], indice)

    def test_grafias_diferentes_da_mesma_especie_nao_sao_divergencia(self, monkeypatch):
        """O catálogo escreve "Ação Penal Privada" e "Privada"; a auditoria
        compara espécie, não grafia."""
        indice = self._com_texto("Caluniar alguém. Somente se procede mediante queixa.",
                                 monkeypatch)
        for grafia in ("Privada", "Ação Penal Privada"):
            assert not auditar.auditar_acao_penal(
                [registro(id=5, artigo="Art. 151, caput", acao=grafia)], indice)


class TestNome:
    def _com(self, texto, monkeypatch):
        class Falso:
            def __init__(self, t):
                self.texto, self.epigrafe, self.citacao, self.incisos = t, None, False, []
        monkeypatch.setattr(auditar, "dispositivos_de",
                            lambda fid: {"Art. 350|caput": Falso(texto)})
        return {"CP": "cp"}

    def test_nome_de_outro_crime_e_suspeito(self, monkeypatch):
        """Caso real: o art. 338 do CP está registrado como "sonegação de
        contribuição previdenciária", que é o art. 337-A. O 338 é o reingresso
        de estrangeiro expulso — nenhuma palavra em comum."""
        indice = self._com("Reingressar no território nacional o estrangeiro que dele "
                           "foi expulso.", monkeypatch)
        achados = auditar.auditar_nomes(
            [registro(id=7, artigo="Art. 350",
                      crime="Sonegação de contribuição previdenciária")],
            indice)
        assert achados and achados[0]["tipo"] == "NOME-SUSPEITO"

    def test_nome_que_conversa_com_o_texto_passa(self, monkeypatch):
        """Uma palavra em comum basta: o catálogo descreve a conduta com outras
        palavras, e exigir mais transformaria nome legítimo em suspeito."""
        indice = self._com("Omitir, em documento público ou particular, declaração que "
                           "dele devia constar, para fins eleitorais, alterando a verdade "
                           "sobre fato juridicamente relevante.", monkeypatch)
        assert not auditar.auditar_nomes(
            [registro(id=7, artigo="Art. 350", crime="Falsidade ideológica eleitoral")],
            indice)

    def test_paragrafo_qualificado_nao_e_auditado(self, monkeypatch):
        """"Se resulta:" não descreve conduta — comparar produziria acusação
        inútil em todo parágrafo qualificado do catálogo."""
        class Falso:
            texto, epigrafe, citacao, incisos = "Se resulta:", None, False, []
        monkeypatch.setattr(auditar, "dispositivos_de",
                            lambda fid: {"Art. 129|§ 1º": Falso()})
        assert not auditar.auditar_nomes(
            [registro(id=7, artigo="Art. 129, §1º", crime="Lesão corporal grave")],
            {"CP": "cp"})
