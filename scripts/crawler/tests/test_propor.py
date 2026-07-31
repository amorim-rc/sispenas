# -*- coding: utf-8 -*-
"""Testes do orquestrador do PR semanal (F6b).

Sem rede e sem tocar no repositório: o que se testa aqui é a montagem — versão,
corpo do PR e entrada de changelog —, porque é onde um erro passa despercebido
até virar release publicada. A escolha do diploma e a aplicação no catálogo são
exercitadas contra os snapshots reais nas rodadas do workflow.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # scripts/
import propor  # noqa: E402


@pytest.fixture
def escolha():
    """Uma rodada com uma correção e uma linha nova, no formato dos geradores."""
    antes = {"id": 42, "artigo": "Art. 155, §4º", "crime": "Furto qualificado",
             "pena_min": 24, "pena_max": 96, "tipo_pena": "Reclusão",
             "obs": "2 a 8 anos reclusão"}
    depois = dict(antes, pena_min=24, pena_max=120, tipo_pena="Reclusão",
                  obs="2 a 10 anos reclusão")
    return {
        "fonte": {"id": "cp", "rotulos": ["CP"], "url": "https://exemplo/cp.htm"},
        "correcoes": [{"id": 42, "antes": antes, "depois": depois,
                       "evidencia": "Pena - reclusão, de dois a dez anos"}],
        "novas": [{"linha": {"id": 1700, "artigo": "Art. 155, §5º",
                             "crime": "Furto de veículo", "pena_min": 36,
                             "pena_max": 96, "tipo_pena": "Reclusão",
                             "elemento": "Doloso"},
                   "achado": {"tipo": "AUSENTE", "detalhe": "dispositivo com pena própria"},
                   "herdado": ["acao"], "caput_id": 7}],
        "humanos": [{"chave": "Art. 180|caput", "tipo": "REVOGADO",
                     "detalhe": "a lei marca como revogado"}],
        "total": 2,
    }


class TestVersao:
    def test_correcao_de_dado_sobe_o_patch(self):
        assert propor.proxima_versao("1.3.0") == "1.3.1"
        assert propor.proxima_versao("1.3.9") == "1.3.10"

    def test_bump_que_nao_pega_derruba_o_processo(self, tmp_path):
        """O bump por substituição de texto já falhou em silêncio neste
        repositório — três entradas anunciaram versões que nunca saíram. Aqui,
        não casar é erro fatal, nunca "seguir com o arquivo intacto"."""
        alvo = tmp_path / "package.json"
        alvo.write_bytes(b'{\r\n  "version": "9.9.9"\r\n}\r\n')
        with pytest.raises(SystemExit):
            propor._substituir_versao(alvo, r'"version":\s*"{v}"', "1.3.0", "1.3.1")

    def test_bump_preserva_o_crlf_do_arquivo(self, tmp_path):
        """Reescrever em LF trocaria a quebra de linha do arquivo inteiro e o
        diff do PR mostraria cinquenta linhas no lugar de uma."""
        alvo = tmp_path / "package.json"
        alvo.write_bytes(b'{\r\n  "name": "sispenas",\r\n  "version": "1.3.0"\r\n}\r\n')
        propor._substituir_versao(alvo, r'"version":\s*"{v}"', "1.3.0", "1.3.1")
        bruto = alvo.read_bytes()
        assert b'"version": "1.3.1"' in bruto
        assert bruto.count(b"\r\n") == 4 and b"\n\n" not in bruto.replace(b"\r\n", b"")


class TestCorpoDoPR:
    def test_cada_mudanca_leva_a_evidencia_da_lei(self, escolha):
        corpo = propor.corpo_pr(escolha, "1.3.1")
        assert "https://exemplo/cp.htm" in corpo          # o texto conferido
        assert "Pena - reclusão, de dois a dez anos" in corpo
        assert "24–96 meses" in corpo and "24–120 meses" in corpo
        assert "?tipo=42" in corpo                        # onde conferir publicado

    def test_linha_nova_declara_o_que_foi_herdado(self, escolha):
        """Do texto saem seis campos; o resto herda do caput. A revisão precisa
        saber onde olhar primeiro."""
        corpo = propor.corpo_pr(escolha, "1.3.1")
        assert "Herdado do caput" in corpo and "acao" in corpo

    def test_o_que_nao_e_mecanico_aparece_como_pendente(self, escolha):
        corpo = propor.corpo_pr(escolha, "1.3.1")
        assert "Fora do automático" in corpo and "REVOGADO" in corpo


class TestEntradaDeChangelog:
    def test_entrada_valida_e_atrelada_a_versao_do_pr(self, escolha, monkeypatch,
                                                      tmp_path):
        monkeypatch.setattr(propor, "ENTRADAS", tmp_path)
        destino, ts = propor.entrada_changelog(escolha, "1.3.1", "2026-08-03")
        assert destino.name == "2026-08-03-conferidor-cp.ts"
        assert destino.parent.name == "2026"
        assert "version: 'v1.3.1'" in ts
        assert "id: '2026-08-03-conferidor-cp'" in ts
        assert "tipo: 'correcao'" in ts
        # body é texto puro: sem markdown, sem backtick (contrato do ChangelogEntry)
        corpo = ts.split("body: [")[1].split("],")[0]
        assert "`" not in corpo and "**" not in corpo

    def test_id_nao_colide_no_mesmo_dia(self, escolha, monkeypatch, tmp_path):
        monkeypatch.setattr(propor, "ENTRADAS", tmp_path)
        (tmp_path / "2026").mkdir()
        (tmp_path / "2026" / "2026-08-03-conferidor-cp.ts").write_text("já existe")
        destino, ts = propor.entrada_changelog(escolha, "1.3.1", "2026-08-03")
        assert destino.name == "2026-08-03-conferidor-cp-2.ts"
        assert "id: '2026-08-03-conferidor-cp-2'" in ts

    def test_so_linhas_novas_e_novidade(self, escolha, monkeypatch, tmp_path):
        monkeypatch.setattr(propor, "ENTRADAS", tmp_path)
        escolha["correcoes"] = []
        _, ts = propor.entrada_changelog(escolha, "1.4.0", "2026-08-03")
        assert "tipo: 'novidade'" in ts


def test_meta_do_pr_tem_ramo_e_titulo(escolha, monkeypatch, tmp_path):
    """O workflow lê este JSON para nomear o ramo e o PR — se mudar de formato,
    o passo de abertura falha calado."""
    monkeypatch.setattr(propor, "ENTRADAS", tmp_path / "entries")
    monkeypatch.setattr(propor, "corrigir", type("X", (), {"aplicar": staticmethod(lambda p: None)}))
    monkeypatch.setattr(propor, "criar", type("X", (), {"aplicar": staticmethod(lambda p: None)}))
    monkeypatch.setattr(propor, "subir_versao", lambda v: None)
    meta = propor.aplicar(escolha, "1.3.1", "2026-08-03", tmp_path / "saida")
    assert meta["ramo"] == "conferidor/cp-2026-08-03"
    assert meta["fonte"] == "cp" and meta["versao"] == "1.3.1"
    assert (tmp_path / "saida" / "corpo.md").exists()
    gravado = json.loads((tmp_path / "saida" / "meta.json").read_text(encoding="utf-8"))
    assert gravado["correcoes"] == 1 and gravado["novas"] == 1
