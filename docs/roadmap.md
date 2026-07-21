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
| **MAIOR** (`X.0.0`) | Quebra de compatibilidade para esses públicos: remoção ou renomeação de campo do JSON, **mudança de significado de campo ou do conjunto de dados**, reatribuição de `id`, remoção de rota sem redirecionamento. | Passar a incluir tipos revogados; separar `crimes.json` em vários arquivos. |
| **MENOR** (`1.Y.0`) | Funcionalidade nova mantendo compatibilidade: **acrescentar** campo ao JSON, nova tela, novo benefício, nova rota. | A v1.1.0 acrescentou `resultado_morte` e a Busca por benefício sem remover nada. |
| **CORREÇÃO** (`1.1.Z`) | Correção sem funcionalidade nova: erro de dosimetria, dado errado no catálogo, defeito de interface. | Corrigir a pena de um artigo; ajustar contraste. |

:::note[Correção de dado é `CORREÇÃO`, não `MENOR`]
Resolver uma das contradições do catálogo muda o resultado de uma consulta — mas
corrige um erro, não acrescenta capacidade. Vai em `1.1.Z`. Já **acrescentar um campo**
que não existia (`resultado_morte`) é `MENOR`, ainda que motivado por um erro: consumidores
do JSON ganham informação sem perder nenhuma.
:::

## v1.2.0 — Dosimetria completa (cálculo por fases)

Hoje o sistema parte da **pena cominada** e deixa as circunstâncias do réu mexerem só nos
benefícios, não na pena. A v1.2.0 percorre as três fases do art. 68 do CP e faz o cálculo
**deslocar a moldura** — revelando, para cada tipo penal, quantos **cenários de condenação**
a lei comporta.

**Modelo em camadas.** O dispositivo continua sendo a **linha canônica** (URL estável); as
circunstâncias entram como **modificadores combináveis** aplicados na consulta, sem inflar a
lista nem tocar o esquema de `crimes.json`. É por isso que a virada é MENOR, não MAIOR: o
cálculo vive numa camada de simulação (novo `data/modificadores.json` + lógica de cliente),
sobre os mesmos dados abertos.

### 1ª fase — pena-base
- [ ] **Circunstâncias judiciais** (art. 59): culpabilidade, antecedentes, conduta social,
      motivos, consequências. Hoje só filtram benefícios; passam a poder deslocar a
      pena-base dentro da moldura.

### 2ª fase — agravantes e atenuantes (arts. 61–66)
- [ ] Agravantes e atenuantes como modificadores, com a **Súmula 231 do STJ** explícita
      (atenuante não reduz abaixo do mínimo — assimetria que a 3ª fase não tem).

### 3ª fase — causas de aumento e diminuição
- [ ] **Causas de aumento/diminuição genéricas** — as que valem para vários tipos e **não**
      estão no preceito de cada um (art. 141 na honra, art. 226 nos sexuais, art. 327 nos
      crimes contra a administração…) — como modificadores em `data/modificadores.json`
      (dispositivo, fração/quantum, escopo de aplicação).
- [ ] **Contabilização controlada** (decisão de projeto): as causas de aumento **embutidas**
      no artigo do crime (§4º/§6º/§7º do art. 121, por exemplo) permanecem como **linhas** —
      são preceitos primários da lei, com URL própria e moldura já calculada. Um modificador
      só é **oferecido** a um tipo quando aquela causa de aumento **não** está no rol de
      preceitos derivados dele, evitando dupla contagem no número de cenários.

### Concurso
- [ ] **Concurso de crimes** — combinador de linhas: material (art. 69, soma das penas),
      formal (art. 70) e continuidade (art. 71, uma pena com aumento).
- [ ] **Concurso de pessoas** — seletor de **papel do agente** (autor / partícipe). A
      **participação de menor importância** (art. 29, §1º) aplica a redução de 1/6 a 1/3 à
      mesma moldura, fechando a lacuna do agente com participação reduzida. A **cooperação
      dolosamente distinta** (art. 29, §2º) resolve-se apontando para o tipo menos grave —
      que já tem a própria linha —, sem criar variante combinatória nova.

### Consumo
- [ ] No detalhe do tipo, os modificadores aplicáveis viram **toggles** que deslocam a
      moldura e **recalculam os benefícios ao vivo** — conectando o que hoje são dois fios
      separados (a simulação de pena e as circunstâncias do réu).
- [ ] A busca por benefício reporta o **alcance em duas unidades**: por **dispositivo** (o
      crime) e por **cenário de condenação** (a moldura resultante) — tornando o número
      comparável ao das ~1.529 unidades do artigo original de 2008.

---

## v1.3.0 — Catálogo de benefícios versionado em dados

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

## v1.4.0 — Cobertura completa e acervo histórico

### 1. Verificação da possibilidade de lacunas

A cobertura dos tipos vigentes **não tem mais lacuna apontada** — todo dispositivo com
preceito penal em vigor foi conferido contra o texto compilado do Planalto (ver
[Completude do catálogo](/docs/completude)). Esta parte deixa de ser "fechar lacunas
conhecidas" e passa a ser **procurar lacunas ainda não vistas**:

- [ ] Reexecutar o inventário contra o índice temático do Planalto + LexML, à caça de
      diplomas com preceito penal **fora** do inventário atual.
- [ ] Revisar as exclusões deliberadas (penas cominadas por remissão quebrada, causas de
      aumento genéricas) à luz da v1.2.0.
- [ ] **Revisão cautelar das heurísticas** — violência, grave ameaça, ação penal e
      tentativa preenchidas na cobertura em massa (sobretudo no CPM) — antes que o crawler
      as use como linha de base.

### 2. Acervo histórico — tipos revogados, alterados e não recepcionados

Reunir **todos os tipos penais que deixaram de valer ou mudaram**, para histórico
completo — o que hoje nenhuma ferramenta oferece de forma estruturada, e que interessa
diretamente à pesquisa acadêmica (ultratividade da lei mais benéfica; linha do tempo da
descriminalização):

- [ ] **Aba própria** em Pesquisa ▸ **Acervo histórico**, com a lista de tipos **por
      categoria**: `revogado` · `alterado` · `nao_recepcionado` — no mesmo formato da lista
      de tipos vigentes
- [ ] **Tela de detalhe por tipo**: o **texto original** e o que houve com ele — alteração,
      revogação ou não recepção —, **quando** houve e **por qual dispositivo** (com link
      para o tipo sucessor, quando houver)
- [ ] **Dataset separado**: `data/historico.json` (fonte) → `static/data/historico.json`
      (derivado), com ids próprios — **nunca misturado a `crimes.json`**
- [ ] Fonte: os textos anteriores do Planalto (as redações revogadas ficam riscadas nos
      compilados — a mesma extração da conferência); os 10 diplomas revogados/não
      recepcionados já estão inventariados em `data/diplomas.json`, e os casos já
      identificados estão listados em [Acervo histórico](/docs/acervo-historico)
- [ ] Ponto de partida já conhecido: adultério (art. 240), sedução (217), rapto (219–222),
      ECA art. 233, LCP arts. 27, 39, 60, 61 e 65, Lei de Imprensa, LSN, Estatuto do
      Torcedor, o art. 19 (vetado) da Lei 9.807/99 e as redações **alteradas** registradas
      nas conferências (art. 121, §2º VI — feminicídio; Maria da Penha art. 24-A…)

:::note[Por que o acervo em dataset separado é MENOR, e não MAIOR]
O invariante dos dados abertos — *todo registro de `crimes.json` é direito vigente* —
permanece intacto: o acervo vive em arquivo e rota próprios, e quem calcula estatísticas
sobre o catálogo vigente não é afetado. Nova aba + novo arquivo = funcionalidade
compatível (MENOR). O que continua sendo **v2.0.0** é fundir os dois mundos:
`revogado_em`/`vigente_desde` dentro do dataset principal, alimentados pelo crawler do DOU.
:::

---

## v2.0.0 — Atualização automática da legislação (crawler do DOU)

Manter o catálogo atualizado com segurança jurídica, a partir do **Diário Oficial da
União**. O pipeline de dados da v1.1.0 já foi desenhado para receber isto: fonte editável
separada do derivado, invariantes de `id`, validação estrita na CI e relatório de
qualidade. É também a **release de salto técnico na estrutura do repositório** — e por isso
incorpora as melhorias transversais que antes não tinham versão fixa.

**Por que MAIOR e não menor:** o crawler precisa registrar revogações, e apagar o registro
não é opção (a URL `?tipo=N` morreria). Tipos revogados passam a conviver no arquivo — o
que **desmente o invariante** de que todo registro é direito vigente. Nenhum campo é
removido, mas toda estatística feita por terceiros passa a estar errada em silêncio. Isso
é quebra de contrato, ainda que o esquema pareça intacto.

**Pré-requisito — catálogo completo.** A virada para a v2.0.0 só acontece quando o
catálogo de **tipos penais e de benefícios** estiver completo e conferido. Toda a busca de
completude e conferência (a [Completude do catálogo](/docs/completude) dos tipos e a
v1.3.0 dos benefícios) fica na linha `1.y.z`, por não quebrar contrato: são correções e
acréscimos sobre o esquema atual. O crawler é o que **muda o significado** do conjunto de
dados (passa a conter revogados) — e automatizar a atualização de um catálogo ainda
incompleto ou não conferido multiplicaria o erro em vez de o corrigir.

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

A **primeira entrega** do acervo (aba própria + dataset separado `historico.json`) é a
[v1.4.0](#v140--cobertura-completa-e-acervo-histórico). O que fica para a v2.0.0 é a
**fusão dos dois mundos**, que o crawler exige:

- [ ] Campos `revogado_em`, `revogado_por` (norma) e `vigente_desde` **no dataset
      principal**; um tipo revogado pelo crawler **nunca é apagado** — muda de estado,
      preserva o `id` e a URL
- [ ] O crawler passa a **alimentar o acervo**: revogação detectada no DOU gera proposta
      tanto no catálogo vigente quanto no histórico
- [ ] Linha do tempo da descriminalização: o que saiu do Código, quando e por qual norma
- [ ] **Ultratividade da lei penal mais benéfica** (art. 5º, XL, CF; art. 2º, par. único,
      CP): a lei revogada continua a reger o fato praticado sob sua vigência quando for
      mais benéfica — daí o acervo não ser mera curiosidade, e sim direito aplicável

### Melhorias técnicas transversais (salto de estrutura)

Sendo a release que reestrutura tecnicamente o repositório, a v2.0.0 absorve as melhorias
que antes flutuavam sem versão:

- [ ] **Acessibilidade**: navegação por teclado na tabela, `aria-live` nos contadores que
      mudam com a simulação, foco visível consistente
- [ ] **Busca textual** tolerante a acentos e erros de digitação
- [ ] **Exportar** o resultado da busca por benefício em CSV
- [ ] **Comparar dois benefícios** lado a lado sobre o mesmo catálogo
- [ ] Testes de regressão da dosimetria com casos reais de jurisprudência
- [ ] Dashboards analíticos (distribuição de penas, hediondos por década)

:::note[Por que a fusão é v2.0.0]
Enquanto o acervo vive em arquivo separado (v1.4.0), o invariante *todo registro de
`crimes.json` é direito vigente* segue de pé. Trazer `revogado_em` para o dataset
principal — e conviver com revogados no mesmo arquivo — é o que desmente esse invariante e
quebra as estatísticas de terceiros em silêncio: MAIOR, junto com o crawler, para que uma
mudança pague o custo de compatibilidade da outra.
:::

---

## v3.0.0 — Processo penal e jurisprudência

Estender a atualização automática ao **Direito Processual Penal**, que rege boa parte dos
benefícios — um salto em relação ao conteúdo originalmente planejado, possível uma vez que
o direito material já está consolidado e mantido pelo crawler.

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares ou
      vedações (ex.: Súmula 536 STJ)
- [ ] Alertas quando decisão vinculante invalidar uma regra implementada

---

## v4.0.0 — Plataforma de pesquisa de políticas públicas

Avanços técnicos mais refinados, possíveis uma vez que o conteúdo está consolidado e
sendo automaticamente atualizado e/ou depreciado — podendo inclusive incorporar melhorias
sobre o conteúdo dedicado ao Processo Penal. Reservado para quando houver **quebra de
contrato** dos dados abertos, provável ao introduzir a vigência temporal em escala e o
esquema versionado que reestruturam o conjunto de dados.

- [ ] Cruzamento exaustivo tipos × benefícios (matriz de elegibilidade)
- [ ] Simulação legislativa em lote ("aumentar em 2 anos a pena dos crimes patrimoniais")
- [ ] Séries temporais do endurecimento/abrandamento penal
- [ ] Exportação para pesquisa (CSV, JSON, API versionada)
- [ ] Esquema versionado dos dados abertos, com política de depreciação
