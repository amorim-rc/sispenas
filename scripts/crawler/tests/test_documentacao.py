# -*- coding: utf-8 -*-
"""Testes da saúde da documentação.

O que importa aqui é a REGRA de vencimento — prazo e dependência —, não o `git`.
As datas de commit são substituídas por um dublê, para o teste não depender do
histórico do repositório em que roda.
"""
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "scripts"))
import verificar_documentacao as vd  # noqa: E402

HOJE = date(2026, 8, 2)


def registro(**doc):
    base = {"arquivo": "CONTRIBUTING.md", "sobre": "convenções",
            "conferido_em": "2026-06-01", "depende_de": []}
    return {"cadencia_padrao_dias": 90, "documentos": [{**base, **doc}]}


def com_datas(monkeypatch, datas: dict):
    monkeypatch.setattr(vd, "commit_mais_recente",
                        lambda caminho: datas.get(caminho))


def test_documento_recente_e_sem_dependencia_mudada_esta_em_dia(monkeypatch):
    com_datas(monkeypatch, {"CONTRIBUTING.md": date(2026, 7, 30)})
    v = vd.avaliar(registro(depende_de=["scripts/transform_data.py"]), HOJE)[0]
    assert not v["vencido_por_prazo"] and not v["dependencias_mudaram"]


def test_dependencia_que_mudou_depois_vence_o_documento(monkeypatch):
    """O caso que motivou o verificador: a convenção C7 do CONTRIBUTING mandava
    escrever a pena no `obs`, e o `transform_data` já tinha invertido a regra —
    dentro do prazo, e errado."""
    com_datas(monkeypatch, {
        "CONTRIBUTING.md": date(2026, 7, 20),
        "scripts/transform_data.py": date(2026, 7, 28),
    })
    v = vd.avaliar(registro(depende_de=["scripts/transform_data.py"]), HOJE)[0]
    assert not v["vencido_por_prazo"]
    assert [d["arquivo"] for d in v["dependencias_mudaram"]] == ["scripts/transform_data.py"]


def test_editar_o_documento_conta_como_conferi_lo(monkeypatch):
    """Quem mexeu no texto o leu: a data efetiva é a do commit, e a dependência
    mudada ANTES dele deixa de pesar."""
    com_datas(monkeypatch, {
        "CONTRIBUTING.md": date(2026, 8, 1),
        "scripts/transform_data.py": date(2026, 7, 28),
    })
    v = vd.avaliar(registro(depende_de=["scripts/transform_data.py"]), HOJE)[0]
    assert v["conferido_em"] == "2026-08-01" and not v["dependencias_mudaram"]


def test_prazo_vencido_mesmo_sem_dependencia(monkeypatch):
    com_datas(monkeypatch, {"CONTRIBUTING.md": date(2026, 1, 10)})
    v = vd.avaliar(registro(conferido_em="2026-01-10"), HOJE)[0]
    assert v["vencido_por_prazo"] and v["dias"] > 90


def test_arquivo_que_sumiu_e_registro_orfao(monkeypatch):
    com_datas(monkeypatch, {})
    v = vd.avaliar(registro(arquivo="docs/nao-existe.md"), HOJE)[0]
    assert not v["existe"]
    assert "não existe" in vd.montar_relatorio([v])


def test_relatorio_diz_o_que_vencer_significa(monkeypatch):
    com_datas(monkeypatch, {"CONTRIBUTING.md": date(2026, 1, 10)})
    texto = vd.montar_relatorio(vd.avaliar(registro(conferido_em="2026-01-10"), HOJE))
    assert "não quer dizer que esteja errado" in texto


def test_registro_real_do_projeto_e_coerente():
    """Todo documento registrado existe, e todo .md explicativo está registrado."""
    import json
    registro_real = json.loads((RAIZ / "data" / "documentacao.json").read_text(encoding="utf-8"))
    declarados = {d["arquivo"] for d in registro_real["documentos"]}
    for arquivo in declarados:
        assert (RAIZ / arquivo).exists(), f"{arquivo} está no registro e não existe"
    # docs/ publicados: os gerados (completude, acervo) não entram, porque quem
    # os mantém é o gerador, não a prosa.
    gerados = {"docs/completude.md", "docs/acervo-historico.md"}
    publicados = {f"docs/{p.name}" for p in (RAIZ / "docs").glob("*.md")}
    assert not (publicados - gerados - declarados), "documento publicado fora do registro"
