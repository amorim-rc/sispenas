---
id: roadmap
title: Roadmap
sidebar_position: 5
---

# Roadmap

## Como este roadmap usa o versionamento semântico

O SISPENAS segue o [Semantic Versioning 2.0.0](https://semver.org/lang/pt-BR/) —
`MAIOR.MENOR.CORREÇÃO` — com uma leitura explícita do que cada posição significa
**neste projeto**. Sem essa convenção, "v1.1" e "v2.0" viram apenas rótulos de ordem.

O SISPENAS tem dois públicos que dependem de estabilidade, e são eles que definem a
**API pública** para efeito de versionamento:

1. quem consome os **dados abertos** (`static/data/crimes.json`) e os cita em pesquisa;
2. quem referencia **URLs** (`/pesquisa/tipos?tipo=N`) em artigos e pareceres.

| Posição | Incrementa quando | Exemplos |
|---|---|---|
| **MAIOR** (`X.0.0`) | Quebra de compatibilidade para esses públicos: remoção ou renomeação de campo do JSON, **mudança de significado de campo ou do conjunto de dados**, reatribuição de `id`, remoção de rota sem redirecionamento. | Passar a incluir tipos revogados; dosimetria por fases; separar `crimes.json` em vários arquivos. |
| **MENOR** (`1.Y.0`) | Funcionalidade nova mantendo compatibilidade: **acrescentar** campo ao JSON, nova tela, novo benefício, nova rota. | A v1.1.0 acrescentou `resultado_morte` e a Busca por benefício sem remover nada. |
| **CORREÇÃO** (`1.1.Z`) | Correção sem funcionalidade nova: erro de dosimetria, dado errado no catálogo, defeito de interface. | Corrigir a pena de um artigo; ajustar contraste. |

:::note[Correção de dado é `CORREÇÃO`, não `MENOR`]
Resolver uma das contradições do catálogo muda o resultado de uma consulta — mas
corrige um erro, não acrescenta capacidade. Vai em `1.1.Z`. Já **acrescentar um campo**
que não existia (`resultado_morte`) é `MENOR`, ainda que motivado por um erro: consumidores
do JSON ganham informação sem perder nenhuma.
:::

## v1.2.0 — Catálogo de benefícios versionado em dados

Concluir o caminho aberto pela v1.1.0: tirar os benefícios do código e colocá-los em
**JSON versionado**, como já ocorre com `crimes.json`. É pré-requisito da v2.0.0 —
sem isso, o crawler saberia atualizar tipos penais, mas não benefícios.

- [ ] Serializar `BeneficioDef` para `data/beneficios.json` (metadados, requisitos,
      vedações, parâmetros), mantendo em código apenas as funções de avaliação
- [ ] Vocabulário de **predicados declarativos** (`penaMax <= X`, `semViolencia`,
      `naoReincidente`) para dispensar código nos benefícios simples
- [ ] **Vigência temporal**: qual redação de cada benefício valia em cada data (art. 112
      da LEP antes e depois da Lei 13.964/2019; saída temporária antes e depois da Lei
      14.843/2024) — hoje o sistema só conhece o direito vigente
- [ ] Aplicar a **lei mais benéfica** (art. 5º, XL, CF) quando houver sucessão de leis
- [ ] CI de validação do catálogo de benefícios (frações em [0,1], fundamento citado)
- [ ] Permalink de simulação: URL que carrega os parâmetros editados

---

## v1.3.0 — Cobertura completa e acervo histórico

Meta em duas partes, **nesta ordem**:

### 1. Completude dos tipos vigentes

Fechar as lacunas apontadas pelo denominador, acompanhadas na página
[Completude do catálogo](/docs/completude) (gerada de `data/diplomas.json` +
`data/crimes.json` por `scripts/gerar_completude.py`):

- [ ] CPM (351 preceitos × 69 registros) — a maior lacuna
- [ ] Código Eleitoral (61 × 26)
- [ ] Loterias — DL 6.259/44 (13 × 4) e Lei das Eleições — 9.504/97 (10 × 5)
- [ ] Os 16 diplomas ainda **sem nenhum registro** (Lei Geral do Esporte,
      serviços postais, atividades nucleares, DL 201/67 etc.)
- [x] LCP e Lei 9.279/96 (concluídas na v1.1.2)

### 2. Acervo histórico — tipos revogados, alterados e não recepcionados

Reunir **todos os tipos penais que deixaram de valer ou mudaram**, para
histórico completo — o que hoje nenhuma ferramenta oferece de forma
estruturada, e que interessa diretamente à pesquisa acadêmica (ultratividade da
lei mais benéfica; linha do tempo da descriminalização):

- [ ] **Aba extra** em Pesquisa ▸ **Acervo histórico**, com a lista de tipos
      **por categoria**: `revogado` · `alterado` · `nao_recepcionado` — no
      mesmo formato da lista de tipos vigentes
- [ ] **Tela de detalhe por tipo**: apenas o **texto original** e o que houve
      com ele — alteração, revogação ou não recepção —, **quando** houve e
      **por qual dispositivo** (com link para o tipo sucessor, quando houver)
- [ ] **Dataset separado**: `data/historico.json` (fonte) →
      `static/data/historico.json` (derivado), com ids próprios — **nunca
      misturado a `crimes.json`**
- [ ] Fonte: os textos anteriores do Planalto (as redações revogadas ficam
      riscadas nos compilados — a mesma extração da Fase 1); os 10 diplomas
      revogados/não recepcionados já estão inventariados em
      `data/diplomas.json`
- [ ] Ponto de partida já conhecido: adultério (art. 240), sedução (217),
      rapto (219–222), ECA art. 233, LCP arts. 25*, 27, 39, 60, 61 e 65, Lei
      de Imprensa, LSN, Estatuto do Torcedor, e as redações **alteradas**
      registradas nas conferências (LCP art. 50 §2º, Maria da Penha art. 24-A…)

:::note[Por que o acervo em dataset separado é MENOR, e não MAIOR]
O invariante dos dados abertos — *todo registro de `crimes.json` é direito
vigente* — permanece intacto: o acervo vive em arquivo e rota próprios, e quem
calcula estatísticas sobre o catálogo vigente não é afetado. Nova aba + novo
arquivo = funcionalidade compatível (MENOR). O que continua sendo **v2.0.0** é
fundir os dois mundos: `revogado_em`/`vigente_desde` dentro do dataset
principal, alimentados pelo crawler do DOU.
:::

**Execução:** o acervo só começa **depois** da completude dos vigentes — a
mesma extração que fecha as lacunas é a que colhe os textos históricos, e um
acervo montado sobre catálogo incompleto herdaria os buracos.

---

## v2.0.0 — Atualização automática da legislação (crawler do DOU)

Manter o catálogo atualizado com segurança jurídica, a partir do **Diário Oficial da
União**. O pipeline de dados da v1.1.0 já foi desenhado para receber isto: fonte editável
separada do derivado, invariantes de `id`, validação estrita na CI e relatório de
qualidade.

**Por que MAIOR e não menor:** o crawler precisa registrar revogações, e apagar o registro
não é opção (a URL `?tipo=N` morreria). Tipos revogados passam a conviver no arquivo — o
que **desmente o invariante** de que todo registro é direito vigente. Nenhum campo é
removido, mas toda estatística feita por terceiros passa a estar errada em silêncio. Isso
é quebra de contrato, ainda que o esquema pareça intacto.

**Pré-requisito — catálogo completo.** A virada para a v2.0.0 só acontece quando o
catálogo de **tipos penais e de benefícios** estiver completo e conferido. Toda a busca de
completude e conferência (a [Completude do catálogo](/docs/completude) dos
tipos e a v1.2.0 dos benefícios) fica na linha `1.y.z`, por não quebrar contrato: são
correções e acréscimos sobre o esquema atual. O crawler é o que **muda o significado** do
conjunto de dados (passa a conter revogados) — e automatizar a atualização de um catálogo
ainda incompleto ou não conferido multiplicaria o erro em vez de o corrigir.

### Arquitetura

```
GitHub Actions (cron semanal)
   → Crawler do DOU (Imprensa Nacional / in.gov.br)
   → Filtro por seção e palavras-chave penais (pena, reclusão, detenção, revoga, art.)
   → Agente de IA classifica: cria / altera / revoga tipo penal?
   → Gera proposta de alteração em data/crimes.json  (fonte, nunca o derivado)
   → Abre Pull Request (NUNCA commita direto no main)
   → CI valida: transform_data.py --estrito + invariantes de id + npm run verificar
   → Revisão humana obrigatória (competência jurídica) antes do merge
   → regen-data.yml regenera static/data/crimes.json
```

### Tarefas

- [ ] Coletor do DOU (fonte oficial `in.gov.br`), com paginação e cache
- [ ] Normalizador de texto (extrair artigo, pena mín/máx, modalidade)
- [ ] Classificador (IA) de impacto penal com citação rastreável à fonte
- [ ] Gerador de diff estruturado sobre `data/crimes.json`, **append-only em `id`**
- [ ] Abertura automática de PR + changelog
- [ ] Trilha de auditoria (data da norma, link do DOU, responsável pela revisão)
- [ ] **Curadoria assistida**: o crawler não infere `perdao_judicial_previsto`; deve
      sinalizar candidatos para decisão humana

### Pendências de compatibilidade

- [ ] `revogado_em` / `vigente_desde` por tipo penal: hoje o catálogo só representa o
      direito vigente, e um crawler que acompanha o DOU **precisa** representar revogações
      sem apagar o registro (senão a URL `?tipo=N` morre)
- [ ] `fonte` e `atualizado_em` por registro, para rastrear a origem da informação

### Acervo histórico — integração com o catálogo principal

A **primeira entrega** do acervo (aba própria + dataset separado
`historico.json`) é a [v1.3.0](#v130--cobertura-completa-e-acervo-histórico).
O que fica para a
v2.0.0 é a **fusão dos dois mundos**, que o crawler exige:

- [ ] Campos `revogado_em`, `revogado_por` (norma) e `vigente_desde` **no
      dataset principal**; um tipo revogado pelo crawler **nunca é apagado** —
      muda de estado, preserva o `id` e a URL
- [ ] O crawler passa a **alimentar o acervo**: revogação detectada no DOU
      gera proposta tanto no catálogo vigente quanto no histórico
- [ ] Linha do tempo da descriminalização: o que saiu do Código, quando e por
      qual norma
- [ ] **Ultratividade da lei penal mais benéfica** (art. 5º, XL, CF; art. 2º,
      par. único, CP): a lei revogada continua a reger o fato praticado sob sua
      vigência quando for mais benéfica — daí o acervo não ser mera
      curiosidade, e sim direito aplicável

:::note[Por que a fusão é v2.0.0]
Enquanto o acervo vive em arquivo separado (v1.3.0), o invariante *todo
registro de `crimes.json` é direito vigente* segue de pé. Trazer
`revogado_em` para o dataset principal — e conviver com revogados no mesmo
arquivo — é o que desmente esse invariante e quebra as estatísticas de
terceiros em silêncio: MAIOR, junto com o crawler, para que uma mudança pague
o custo de compatibilidade da outra.
:::

---

## v2.1.0 — Processo penal e jurisprudência

Estender a atualização automática ao **Direito Processual Penal**, que rege boa parte dos
benefícios. Depende da vigência temporal da v1.2.0.

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares ou
      vedações (ex.: Súmula 536 STJ)
- [ ] Alertas quando decisão vinculante invalidar uma regra implementada

---

## v3.0.0 — Dosimetria completa

Hoje o sistema parte da pena cominada. Uma referência em dosimetria precisa percorrer as
três fases do art. 68 do CP.

- [ ] **Circunstâncias judiciais** (art. 59) — pena-base
- [ ] **Agravantes e atenuantes** (arts. 61 a 66) — 2ª fase
- [ ] **Causas de aumento e diminuição** — 3ª fase, hoje ausentes do cálculo
- [ ] **Concurso de crimes**: material (art. 69), formal (art. 70), continuidade (art. 71)
- [ ] Súmula 231, STJ (atenuante não reduz abaixo do mínimo) como regra explícita

---

## v3.1.0 — Plataforma de pesquisa de políticas públicas

Reservado para quando houver **quebra de contrato** dos dados abertos — provável ao
introduzir dosimetria por fases e vigência temporal, que reestruturam o esquema.

- [ ] Cruzamento exaustivo tipos × benefícios (matriz de elegibilidade)
- [ ] Simulação legislativa em lote ("aumentar em 2 anos a pena dos crimes patrimoniais")
- [ ] Séries temporais do endurecimento/abrandamento penal
- [ ] Exportação para pesquisa (CSV, JSON, API versionada)
- [ ] Esquema versionado dos dados abertos, com política de depreciação

---

## Melhorias transversais (sem versão fixa)

- [ ] **Acessibilidade**: navegação por teclado na tabela, `aria-live` nos contadores que
      mudam com a simulação, foco visível consistente
- [ ] **Busca textual** tolerante a acentos e erros de digitação
- [ ] **Exportar** o resultado da busca por benefício em CSV
- [ ] **Comparar dois benefícios** lado a lado sobre o mesmo catálogo
- [ ] Testes de regressão da dosimetria com casos reais de jurisprudência
- [ ] Dashboards analíticos (distribuição de penas, hediondos por década)

---

## Contribuição

Prioridades, em ordem:

1. **Resolver as contradições do catálogo** (v1.1.Z) — é o que impede a citação acadêmica
2. Revisão dos campos derivados (multa, menor potencial ofensivo)
3. Expansão e correção do catálogo
4. Refinamento das regras de benefícios conforme jurisprudência consolidada

Veja [Catálogo de tipos penais](/docs/catalogo-tipos-penais) para o fluxo de correção.
