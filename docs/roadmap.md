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

:::info[Quebra de *invariante* também é MAIOR]
O que quebra compatibilidade não é só remover campo — é **desmentir uma premissa** de quem
consome os dados. Hoje vale um invariante não escrito: *todo registro do catálogo é
direito vigente*. Quem calcula estatísticas conta com isso.

O crawler do DOU precisa registrar **revogações** (art. 28 da Lei de Drogas, por exemplo,
pode ser descriminalizado a qualquer momento), e apagar o registro não é opção: a URL
`?tipo=N` morreria. Ele terá de conviver com tipos revogados no arquivo — e, no instante
em que o primeiro entrar, toda estatística feita por terceiros passa a estar
silenciosamente errada, sem que nenhum campo tenha sido removido.

Por isso o crawler é **v2.0.0**, não uma versão menor: ele muda o que o conjunto de dados
*significa*. É também a razão de `revogado_em` e `vigente_desde` serem pré-requisito dele,
e não um detalhe posterior.
:::

**Versões anteriores.** O roadmap original numerava por ordem de intenção, não por
compatibilidade — o crawler figurava como "v1.1.0" sem que isso tivesse relação com
contrato. As versões já entregues saíram daqui e viraram
[Release notes](/release-notes), com o detalhamento de cada uma.

---

## v1.1.Z — Correções e patches desta release

Correções de dado e ajustes, sem funcionalidade nova. Concluído nesta release:

- [x] **42 contradições internas resolvidas** — cada dispositivo conferido contra o texto
      compilado do Planalto. O catálogo não tem mais nenhuma. A CI trava em
      `--max-contradicoes=0`, então nenhuma nova entra.
- [x] **Lei 15.397/2026 aplicada a furto e roubo** — penas-base, incisos novos (§2º IX/X do
      roubo, §§6º-7º do furto), latrocínio (24-30) e §1º-A (serviços essenciais).
- [x] **Deduplicação** dos registros repetidos que sustentavam as contradições.

Patches previstos para os próximos ciclos desta linha (`1.1.z`):

- [ ] Revisão dos campos ainda `derivado_auto` (multa, menor potencial ofensivo)
- [ ] `resultado_morte` nos poucos dispositivos que reúnem lesão grave **e** morte no mesmo
      registro (ex.: `CP, Art. 158, §3º`) — desambiguar como já feito no art. 127 e no §3º
      da Lei de Tortura
- [ ] Catalogar as hipóteses de perdão judicial cujo tipo ainda não existe no catálogo
      (art. 140, §1º; art. 176, par. único; CTB art. 291)
- [ ] Social card próprio (`og:image`)

---

## Conferência integral do catálogo

O SISPENAS quer ser referência em dosimetria. Isso exige duas coisas: saber que **o que
está no catálogo está certo** (conferência) e que **o que existe na lei está no catálogo**
(cobertura). Ambas avançaram muito na linha `1.1.z`: as 42 contradições internas foram
resolvidas (v1.1.Z), o denominador foi estabelecido (v1.1.2) e a **cobertura dos diplomas
vigentes foi concluída** — o Código Penal Militar, última e maior lacuna, foi conferido na
v1.1.5. O acompanhamento vive na página [Completude do catálogo](/docs/completude).

### O que se sabe hoje

| Indicador | Valor |
|---|---|
| Tipos penais catalogados | **1.473** |
| Diplomas com tipo penal vigente cobertos | todos os inventariados |
| **Denominador** (preceitos secundários vigentes) | 1.172 |
| Contradições internas | **0** |

Todo diploma com preceito penal vigente tem agora seus dispositivos no catálogo,
conferidos contra o texto compilado do Planalto. Como o catálogo **desdobra**
cada artigo em seus tipos (caput, §§, incisos e alíneas com pena própria), os
1.473 tipos superam os 1.172 preceitos primários — e é assim que deve ser: um
artigo pode conter vários tipos penais autônomos.

:::note[A cobertura não é um ponto final]
"Todos os diplomas cobertos" significa que a conferência dispositivo a
dispositivo não localizou preceito faltante — não uma prova de exaustão. O
denominador real não é conhecido com certeza, e uma revisão futura pode
reabrir um diploma (a situação de cada um na [Completude](/docs/completude)
carrega essa ressalva, o "concluído ❓"). Falta ainda **desmembrar incisos que
são tipos distintos mesmo compartilhando a mesma pena**.
:::

:::warning[Revisão cautelar antes do crawler do DOU (v2.0.0)]
Parte dos campos do catálogo foi preenchida por **heurística** na cobertura em
massa — em especial `violencia`, `grave_ameaca`, `tipo de ação penal` e
`tentativa` nos crimes do CPM. Antes de construir o crawler, esses campos
precisam de uma **revisão dispositivo a dispositivo**, para que a linha de base
que o crawler compara esteja apropriadamente registrada. Um crawler que compara
contra dados heurísticos propaga o erro.
:::

### Fonte da verdade

**`planalto.gov.br`** é a fonte normativa; nenhum tipo entra ou se altera sem conferência
contra o **texto compilado** oficial (o que traz as alterações posteriores). Doutrina e
jurisprudência entram só onde a lei é ambígua, e sempre citadas. O relatório de qualidade
já emite, em cada contradição, o link do diploma onde resolvê-la.

### Fase 1 — Estabelecer o universo (o denominador)

Antes de conferir ou incluir qualquer coisa, saber **o que precisa existir**.

- [x] Inventário de **diplomas com preceito penal** em vigor: Parte Especial do CP, LCP,
      CPM e a legislação extravagante (v1.1.2 — 63 diplomas vigentes, 10 revogados
      registrados).
- [x] Para cada diploma, delimitar o **intervalo de artigos penais** (ex.: CDC, arts.
      61–80; falência, arts. 168–178).
- [x] Produzir `data/diplomas.json`: diploma, intervalo, situação (vigente/revogado),
      norma revogadora, artigos esperados (`scripts/inventario_diplomas.py`).
- [x] **Meta da fase:** um número defensável para "quantos tipos penais existem" —
      **1.172 preceitos secundários vigentes**, medidos no texto compilado do Planalto.

### Fase 2 — Conferência dispositivo a dispositivo

Cada artigo, parágrafo, inciso e alínea conferido contra o Planalto.

- [x] Extrair o texto compilado de cada diploma (`scripts/inventario_diplomas.py`,
      `scripts/extrair_cpm.py`).
- [x] Para cada dispositivo: pena mín./máx., modalidade, ação penal, elemento,
      violência/grave ameaça, resultado morte — extraídos e catalogados (parte por
      heurística, ver a Revisão cautelar).
- [x] **Diff automático** contra o catálogo (`scripts/diff_tipos.py`): casa cada preceito
      do texto com o registro e aponta os sem correspondência.
- [x] Contradições internas resolvidas (v1.1.Z); registros herdados errados do CPM
      corrigidos em lugar (v1.1.5).
- [ ] Registrar a conferência por dispositivo: `conferido_em`, `fonte_url`, `conferido_por`
      — substituindo `derivado_auto` por procedência rastreável. **Precede o crawler.**
- [ ] **Portão:** a CI passa a exigir `conferido_em` nos dispositivos já conferidos; o
      número de não conferidos só pode cair.

### Fase 3 — Incluir o que falta ✅ concluída (v1.1.2 → v1.1.5)

- [x] Priorizar por **peso na pesquisa**: LCP e propriedade industrial (v1.1.2);
      loterias, Código Eleitoral e os 16 diplomas sem coleta (v1.1.3); desmembramento
      dos tipos dentro dos artigos da legislação civil e gaps do CP — rixa, ato obsceno,
      duplicata simulada etc. (v1.1.4); **CPM completo, paz e guerra (v1.1.5)**.
- [x] Cada inclusão segue C1–C8 do `CONTRIBUTING.md` — nada de nota de referência ou
      causa de aumento como tipo.
- [x] `id` append-only.
- [ ] **Pendente:** desmembrar incisos que são tipos distintos ainda que compartilhem a
      mesma pena (revisão detalhada, ver a Revisão cautelar acima).

### Fase 4 — Componentes legislativos além dos tipos penais

Há normas que **mudam o resultado do cálculo sem serem tipos penais**. Hoje o SISPENAS as
ignora, e é aí que ele mais se afasta da dosimetria real:

- [ ] **Causas de aumento e diminuição** (3ª fase do art. 68) — as removidas na v1.1.0
      voltam como entidade própria, não como tipos.
- [ ] **Agravantes e atenuantes** (arts. 61–66) — 2ª fase.
- [ ] **Qualificadoras** — distinguir da causa de aumento: alteram a moldura, não incidem
      sobre ela.
- [ ] **Concurso de crimes** (arts. 69–71).
- [ ] **Leis que alteram benefícios sem tipificar**: Lei 8.072/90 (hediondos), Lei
      9.099/95 (JECRIM), LEP, CPP.
- [ ] **Súmulas e teses vinculantes** que fixam limiares (Súmula 231 do STJ: atenuante não
      reduz abaixo do mínimo).

**Mapear** esses componentes é parte da busca de completude, ainda nesta linha `1.y.z`;
sua **modelagem completa** na dosimetria por fases é trabalho maior, previsto para depois.

### Método

Escala pede automação, mas o domínio não perdoa erro. O arranjo que respeita os dois:

1. **Extração automática** do texto oficial → proposta de diff estruturado.
2. **Classificação por IA**, obrigada a citar o dispositivo e a URL de origem.
3. **Revisão humana** com competência jurídica, dispositivo a dispositivo, antes do merge.
4. **Portões de CI** impedem regressão: convenções C1–C3 impostas, contradições só caem.

É a mesma arquitetura do crawler do DOU (v2.0.0) — a diferença é que aqui se varre o
acervo, e lá o fluxo diário. **Construir esta conferência é o que torna o crawler
possível**: sem uma linha de base conferida, não há como saber se o que ele propõe é
novidade ou erro.

:::note[Ordem de execução]
As fases 1 e 2 vêm **antes** do crawler (v2.0.0). Automatizar a atualização de um catálogo
que não se sabe correto multiplica o erro em vez de corrigi-lo.
:::

---

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
completude e conferência (a [Conferência integral](#conferência-integral-do-catálogo) dos
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
