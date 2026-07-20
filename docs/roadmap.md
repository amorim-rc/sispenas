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
(cobertura). A primeira teve um grande avanço na v1.1.Z — as 42 contradições internas
foram todas conferidas contra o Planalto e resolvidas —; a segunda ainda é o trabalho maior.

### O que se sabe hoje

| Indicador | Valor |
|---|---|
| Tipos penais catalogados | 1.042 |
| Dispositivos distintos | 902 |
| Diplomas com registro no catálogo | 48 (65 vigentes inventariados) |
| **Denominador** (preceitos secundários vigentes) | **1.172** |
| Contradições internas | **0** |
| Campos ainda `derivado_auto` | maioria |

O denominador vem de `data/diplomas.json` (Fase 1, concluída na v1.1.2): cada
diploma com preceito penal teve seu intervalo de artigos delimitado e seus
preceitos vigentes contados no texto compilado do Planalto. A unidade é o
**preceito secundário** (cada cominação de pena); o catálogo desdobra incisos,
então os números não se comparam 1:1 — mas agora a lacuna de cada bloco é
mensurável:

| Bloco | Preceitos vigentes | Registros no catálogo | Situação |
|---|---|---|---|
| CPM (DL 1.001/69) | 351 | 69 | **maior lacuna do catálogo** |
| CE (Lei 4.737/65) | 61 | 26 | grande lacuna |
| CP, Parte Especial (arts. 121–361) | 337 | 551 | conferência dispositivo a dispositivo (Fase 2) |
| LCP (DL 3.688/41) | 47 | 57 | **completa na v1.1.2** (47/47 artigos vigentes) |
| Lei 9.279/96 (propriedade industrial) | 12 | 12 | **completa na v1.1.2** |
| Loterias (DL 6.259/44) | 13 | 4 | lacuna |
| Lei das Eleições (9.504/97) | 10 | 5 | lacuna |
| Sem nenhum registro | — | — | Lei Geral do Esporte (14.597/23), serviços postais (6.538/78), atividades nucleares (6.453/77), DL 201/67, planejamento familiar (9.263/96), entre outros — ver `data/diplomas.json` |

:::note[O denominador existe, e é revisável]
1.172 preceitos vigentes em 65 diplomas é o número **medido** hoje; a Fase 2
(conferência dispositivo a dispositivo) pode ajustá-lo — preceitos cominados em
linha corrida dentro de parágrafos são fáceis de subcontar. Todo ajuste manual
está documentado campo a campo em `data/diplomas.json`.
:::

### Fonte da verdade

**`planalto.gov.br`** é a fonte normativa; nenhum tipo entra ou se altera sem conferência
contra o **texto compilado** oficial (o que traz as alterações posteriores). Doutrina e
jurisprudência entram só onde a lei é ambígua, e sempre citadas. O relatório de qualidade
já emite, em cada contradição, o link do diploma onde resolvê-la.

### Fase 1 — Estabelecer o universo (o denominador)

Antes de conferir ou incluir qualquer coisa, saber **o que precisa existir**.

- [x] Inventário de **diplomas com preceito penal** em vigor: Parte Especial do CP, LCP,
      CPM e a legislação extravagante (v1.1.2 — 65 diplomas vigentes, 10 revogados
      registrados).
- [x] Para cada diploma, delimitar o **intervalo de artigos penais** (ex.: CDC, arts.
      61–80; falência, arts. 168–178).
- [x] Produzir `data/diplomas.json`: diploma, intervalo, situação (vigente/revogado),
      norma revogadora, artigos esperados (`scripts/inventario_diplomas.py`).
- [x] **Meta da fase:** um número defensável para "quantos tipos penais existem" —
      **1.172 preceitos secundários vigentes**, medidos no texto compilado do Planalto.

### Fase 2 — Conferência dispositivo a dispositivo

Cada artigo, parágrafo, inciso e alínea conferido contra o Planalto.

- [ ] Extrair o texto compilado de cada diploma do universo da Fase 1.
- [ ] Para cada dispositivo: pena mín./máx., modalidade, multa, ação penal, hediondez,
      elemento, tentativa, violência/grave ameaça, resultado morte.
- [ ] **Diff automático** contra o catálogo, classificando cada dispositivo em:
      `confere` · `diverge` · `ausente no catálogo` · `no catálogo mas não na lei`.
- [x] Contradições internas resolvidas (v1.1.Z) — passo já concluído para os 873
      dispositivos com registro divergente.
- [ ] Registrar a conferência por dispositivo: `conferido_em`, `fonte_url`, `conferido_por`
      — substituindo `derivado_auto` por procedência rastreável.
- [ ] **Portão:** a CI passa a exigir `conferido_em` nos dispositivos já conferidos; o
      número de não conferidos só pode cair.

### Fase 3 — Incluir o que falta

- [x] Priorizar por **peso na pesquisa**, não por facilidade: LCP e propriedade industrial
      primeiro, por serem as maiores lacunas conhecidas — **ambas completas na v1.1.2**.
      Próximas, em ordem de lacuna: CPM, Código Eleitoral, loterias, Lei das Eleições.
- [ ] Cada inclusão segue as convenções C1–C8 do `CONTRIBUTING.md` — nada de nota de
      referência ou causa de aumento como se fosse tipo (foi o erro corrigido na v1.1.0).
- [ ] `id` append-only: novos vão para o fim, a partir de 1112.

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

### Acervo histórico — tipos penais revogados

O mesmo mecanismo que permite ao crawler registrar revogações permite algo maior:
**preservar o que já foi crime no Brasil**. É um acervo grande e de valor próprio para a
pesquisa — a pergunta "o que deixou de ser crime, e quando?" é tão relevante quanto "o
que é crime hoje", e hoje nenhuma ferramenta a responde de forma estruturada.

Casos que o catálogo já encontra: o adultério (art. 240, revogado pela Lei 11.106/2005),
a sedução (art. 217) e o rapto (arts. 219 a 222), revogados pela Lei 12.015/2009; a Lei de
Imprensa (5.250/67), não recepcionada (ADPF 130); a Lei de Segurança Nacional (7.170/83),
substituída pela Lei 14.197/21; o ECA art. 233, revogado pela Lei de Tortura — removido na
v1.1.0 justamente por não haver onde registrá-lo.

- [ ] Aba própria: **Pesquisa ▸ Acervo histórico**, separada da busca vigente para que
      nenhum tipo revogado contamine estatística de direito vigente
- [ ] Campos `revogado_em`, `revogado_por` (norma) e `vigente_desde`; um tipo revogado
      **nunca é apagado** — muda de estado, preserva o `id` e a URL
- [ ] Padrão de exibição: aviso de revogação no topo, com a norma revogadora e o link
      para o tipo que a sucedeu, quando houver
- [ ] Linha do tempo da descriminalização: o que saiu do Código, quando e por qual norma
- [ ] **Ultratividade da lei penal mais benéfica** (art. 5º, XL, CF; art. 2º, par. único,
      CP): a lei revogada continua a reger o fato praticado sob sua vigência quando for
      mais benéfica — daí o acervo não ser mera curiosidade, e sim direito aplicável
- [ ] Fonte: textos revogados do Planalto (que mantém as redações anteriores) — a mesma
      extração da [Conferência integral](#conferência-integral-do-catálogo)

:::note[Por que o acervo é v2.0.0, e não antes]
Registrar revogados exige `revogado_em` e a separação vigente × revogado no consumo dos
dados. É exatamente a quebra de invariante que já move o crawler para MAIOR — fazer as
duas coisas na mesma versão é o desenho certo: uma paga o custo de compatibilidade da
outra.

Antes disso, na v1.1.Z, a [Conferência integral](#conferência-integral-do-catálogo) tem
de distinguir *ausente por lacuna* de *ausente por revogação* — dos 54 artigos faltantes
na Parte Especial do CP, boa parte é revogada, e essa triagem é a matéria-prima do acervo.
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
