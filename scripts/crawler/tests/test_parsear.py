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


# ── Sufixo de letra: depois do ordinal, e em dobro ──────────────────────────
def test_sufixo_depois_do_ordinal_nao_cola_no_artigo_base(carregar):
    """"Art. 2º-A" da Lei 7.716 é a injúria racial, não o art. 2º.

    O marcador ordinal vem ANTES da letra, e o parser antigo o consumia primeiro:
    lia "Art. 2" e devolvia "-A Injuriar alguém…" como corpo do art. 2º — que, no
    compilado, está vetado. Consequência a jusante: a majorante do parágrafo
    único aparecia na auditoria como "art. 2º, parágrafo único", identificador
    que a lei não tem, e a revisão jurídica teve de levantar a suspeita à mão.
    """
    ds = como_dicionarios(parsear(carregar("racismo-art2a")))
    artigos = {d["artigo"] for d in ds}
    assert {"Art. 2", "Art. 2-A"} <= artigos
    assert "Injuriar alguém" in por_marcador(ds, "Art. 2-A")["caput"]["texto"]
    assert "Injuriar" not in (por_marcador(ds, "Art. 2")["caput"]["texto"] or "")
    pu = por_marcador(ds, "Art. 2-A")["parágrafo único"]
    assert "aumentada de metade" in pu["texto"]


def test_sufixo_duplo_e_artigo_proprio(carregar):
    """"Art. 359-M-B" não é o "Art. 359-M" com corpo começando em "B.".

    O golpe de Estado (359-M) e a redução por contexto de multidão (359-M-B) são
    dispositivos diferentes; colados, a redução virava parte do tipo.
    """
    ds = como_dicionarios(parsear(carregar("cp-art359m")))
    artigos = {d["artigo"] for d in ds}
    assert {"Art. 359-M", "Art. 359-M-A", "Art. 359-M-B"} <= artigos
    assert "Tentar depor" in por_marcador(ds, "Art. 359-M")["caput"]["texto"]
    assert "contexto de multidão" in por_marcador(ds, "Art. 359-M-B")["caput"]["texto"]


@pytest.mark.parametrize("texto, artigo, comeco", [
    # Hífen como PONTUAÇÃO, seguido de artigo definido: não é sufixo. O parser
    # antigo criava "Art. 13-O" e comia o "O" do texto.
    ("Art. 13 - O resultado, de que depende a existência do crime", "Art. 13", "O resultado"),
    ("Art. 100 - A ação penal é pública", "Art. 100", "A ação penal"),
    # Ordinal em minúscula ("Art. 4o") continua sendo ordinal.
    ("Art. 4o Poderá ser ajuizada ação cautelar", "Art. 4", "Poderá ser ajuizada"),
    # Sufixo legítimo, colado ao número.
    ("Art. 121-A. Matar mulher por razões da condição do sexo feminino", "Art. 121-A", "Matar mulher"),
])
def test_hifen_de_pontuacao_nao_vira_sufixo(texto, artigo, comeco):
    ds = como_dicionarios(parsear(f"<html><body><p>{texto}:</p></body></html>"))
    assert ds[0]["artigo"] == artigo
    assert ds[0]["texto"].startswith(comeco)


def test_artigo_vetado_nao_e_vigente(carregar):
    """O art. 359-O do CP — comunicação enganosa em massa — foi VETADO na Lei
    14.197/2021 e nunca promulgado. O compilado traz só "(VETADO)" no corpo.

    O parser já sabia marcar "vetado", mas o marcador nascia com a MESMA `ordem`
    do "vigente" que o precedia, e o desempate de `max` fica com o primeiro: o
    genérico vencia o específico. O artigo saía vigente, `ler_penas` não achava
    pena, o conferidor pulava o dispositivo — e o catálogo publicou por meses um
    crime que não existe, com reclusão de 1 a 5 anos."""
    ds = como_dicionarios(parsear(carregar("cp-art359o-vetado")))
    por = por_marcador(ds, "Art. 359-O")
    assert por["caput"]["situacao"] == "vetado"
    assert not (por["caput"]["texto"] or "").strip()
    # O vizinho, com pena própria, segue vigente.
    assert por_marcador(ds, "Art. 359-N")["caput"]["situacao"] == "vigente"


def test_veto_derrubado_continua_vigente(carregar):
    """A ordem inversa existe: "Art. 9º (VETADO)." seguido do artigo promulgado.
    Ali os dois marcadores estão em parágrafos DIFERENTES, e o posterior vence —
    é o art. 9º da Lei de Abuso de Autoridade, em pleno vigor."""
    ds = como_dicionarios(parsear(carregar("abuso-art9-veto-derrubado")))
    assert por_marcador(ds, "Art. 9")["caput"]["situacao"] == "vigente"


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


# ── Texto CITADO de outro diploma (F6b) ─────────────────────────────────────
# Os três testes abaixo travam o defeito que pôs 29 registros falsos no
# catálogo na v1.3.0. O compilado transcreve, embaixo do artigo alterador, a
# redação dada à lei alterada — e essa transcrição parecia dispositivo próprio.
def test_artigo_que_so_altera_outra_lei_e_citacao(carregar):
    d = {x.chave: x for x in parsear(carregar("citacao-12850"))}
    assert d["Art. 24|caput"].citacao          # "O art. 288 do CP passa a vigorar…"
    assert d["Art. 25|caput"].citacao


def test_artigo_transcrito_fora_de_sequencia_e_citacao(carregar):
    """Na Lei 12.850 os artigos vêm 24, 288, 25: o 288 é o artigo do Código
    Penal transcrito. Número que destoa e é seguido pela continuação da
    sequência é transcrição, não artigo do diploma."""
    d = {x.chave: x for x in parsear(carregar("citacao-12850"))}
    assert d["Art. 288|caput"].citacao
    assert d["Art. 288|caput"].pena_texto      # tem pena — e é justamente o risco
    assert not d["Art. 26|caput"].citacao      # a sequência própria continua limpa


def test_contravencao_revogada_mantem_o_texto(carregar):
    """A LCP não apaga o corpo do artigo revogado: põe "(Revogado pela Lei nº
    14.132, de 2021)" ao lado. A regra do corpo curto não via isso, e quatro
    contravenções revogadas entraram no catálogo como vigentes."""
    d = {x.chave: x for x in parsear(carregar("lcp-art65-revogado"))}
    assert d["Art. 65|caput"].situacao == "revogado"


# ── Pena que pertence ao INCISO, não ao dispositivo ─────────────────────────
# Quando o dispositivo é só chapeau, cada inciso traz a sua pena. Antes, as duas
# linhas "Pena" caíam no mesmo dispositivo e a de ordem maior vencia: sobrava a
# pena do ÚLTIMO inciso e a do primeiro sumia. Pior que silêncio — é leitura
# errada, e uma "correção" feita por ela trocaria a pena de um crime pela de
# outro.
def test_chapeau_com_pena_em_cada_inciso(carregar):
    """CP, art. 197: o caput constrange "mediante violência ou grave ameaça:" e
    os incisos I e II cominam penas DIFERENTES (1 mês–1 ano e 3 meses–1 ano)."""
    d = {x.chave: x for x in parsear(carregar("cp-art197-pena-por-inciso"))}
    art = d["Art. 197|caput"]
    assert art.pena_texto is None, "o chapeau não tem pena própria"
    penas = [i["pena_texto"] for i in art.incisos]
    assert "de um mês a um ano" in penas[0]
    assert "de três meses a um ano" in penas[1]


def test_chapeau_do_cpm_com_inciso_sem_pena_no_meio(carregar):
    """CPM, art. 400: o inciso II não comina pena — manda o juiz REDUZIR a do
    inciso I. A distribuição não pode empurrar a pena do III para ele."""
    d = {x.chave: x for x in parsear(carregar("cpm-art400-graus"))}
    art = d["Art. 400|caput"]
    assert art.pena_texto is None
    por_marca = {i["marcador"]: i.get("pena_texto") for i in art.incisos}
    assert "de doze a trinta anos" in por_marca["I"]
    assert por_marca["II"] is None
    assert "grau mínimo" in por_marca["III"]


def test_redacoes_sucessivas_da_mesma_pena_nao_se_distribuem(carregar):
    """Lei 9.613, art. 1º: o Planalto imprime a pena original depois do inciso
    VIII antigo e a redação da Lei 12.683 depois do "VIII - (revogado)" — que é
    outro inciso na estrutura. As duas cominam a MESMA coisa; distribuí-las
    inventaria um segundo crime de lavagem. A pena continua sendo do artigo, e
    vale a redação mais recente."""
    d = {x.chave: x for x in parsear(carregar("lavagem-art1-redacao"))}
    art = d["Art. 1|caput"]
    assert art.pena_texto is not None
    assert "3 (três) a 10 (dez) anos" in art.pena_texto
    assert not any(i.get("pena_texto") for i in art.incisos)
