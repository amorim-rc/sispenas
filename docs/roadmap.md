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
| **MAIOR** (`X.0.0`) | **Salto na natureza do produto**: reestruturação funcional, arquitetural ou procedimental — o sistema passa a fazer algo de outra ordem, não apenas mais do mesmo. | Deixar de ser um catálogo mantido à mão e passar a ser conferido sozinho contra a fonte oficial; estender a cobertura ao processo penal e à jurisprudência. |
| **MENOR** (`X.Y.0`) | O que já existe, com **acréscimos, alterações e remoções** de registros e telas — a natureza do produto permanece. | Acrescentar campo ao JSON, nova tela, novo benefício; incluir ou remover tipos penais. |
| **CORREÇÃO** (`X.Y.Z`) | Correção sem funcionalidade nova: erro de dosimetria, dado errado no catálogo, defeito de interface. | Corrigir a pena de um artigo; ajustar contraste. |

:::note[Correção de dado é `CORREÇÃO`, não `MENOR`]
Resolver uma das contradições do catálogo muda o resultado de uma consulta — mas
corrige um erro, não acrescenta capacidade. Vai em `1.1.Z`. Já **acrescentar um campo**
que não existia (`resultado_morte`) é `MENOR`, ainda que motivado por um erro: consumidores
do JSON ganham informação sem perder nenhuma.
:::

---

## v2.0.0 — Catálogo conferido automaticamente

O catálogo foi montado por acréscimo, e a defasagem só aparecia por acaso. A v2.0.0
troca isso por um **conferidor semanal**: toda segunda-feira o sistema baixa os textos
compilados dos ~60 diplomas no `planalto.gov.br`, estrutura cada dispositivo, lê as
molduras e confronta com o catálogo — abrindo uma **issue** com o que divergir.

É determinístico de ponta a ponta: sem IA, sem inferência: onde não há certeza, há
relatório para decisão humana. Acuidade jurídica continua sendo o valor central.

### O que já está pronto

- [x] Registro de fontes (`data/fontes.json`): 62 diplomas, 69 rótulos, nenhum órfão
- [x] Coletor com detecção de codificação e **sentinela de frescor** por diploma
- [x] Parser estrutural do texto compilado (dispositivo, pena, situação, anotação)
- [x] Extrator de moldura compartilhado com o catálogo, para que os dois lados leiam
      a mesma pena do mesmo jeito
- [x] Differ com lista de **exceções** (o que já foi julgado não volta toda semana)
- [x] Checador de **vigência** (vacatio legis e produção de efeitos diferida) e
      detector de **revogação total** de diploma
- [x] Rodada semanal automática, com issue no repositório
- [x] **PR automático** para o que é mecânico e inequívoco — corrigir moldura ou tipo
      de pena de linha existente, um diploma por rodada, um PR aberto por vez.
      Criação e remoção de linha seguem humanas: exigem decidir se o dispositivo é
      linha, modificador ou nada
- [x] **Watcher do DOU** (filtro textual, sem IA): citação dos diplomas monitorados e
      vocabulário penal, para encontrar **lei penal nova autônoma** — o único caso
      invisível a quem só relê os diplomas que já conhece
- [x] Revogações e registros indevidos encontrados até aqui: retirados do catálogo e
      registrados no [acervo histórico](/docs/acervo-historico) com o id anterior

### O que falta

- [ ] Trilha de auditoria por registro: `fonte` e `atualizado_em`
- [ ] Rotina de revogação: hoje cada achado de dispositivo revogado é tratado à mão,
      porque remover implica decidir o destino da URL pública

:::note[Por que MAIOR]
Não é o tamanho da mudança, é a **natureza** dela: o catálogo deixa de ser um acervo
mantido à mão, que só revelava defasagem por acaso, e passa a ser continuamente
confrontado com a fonte oficial. Muda o procedimento (a conferência vira rotina
semanal, não expedição), muda a arquitetura (entra um pipeline de coleta, parsing e
diferença) e muda o que o produto promete: não mais "conferimos quando olhamos", e sim
"vigiamos toda semana". É salto de ordem, não incremento.
:::

:::caution[Consequência a resolver: a URL de um tipo removido]
`id` é URL pública, citada em pareceres e trabalhos. Remover um tipo revogado deixa
`?tipo=N` sem destino. A v2.2.0 é a saída: o registro **migra** para o acervo histórico
e a rota antiga passa a apontar para lá — o leitor encontra o que procurava, com a
informação de que foi revogado, em vez de um erro.
:::

---

## v2.1.0 — Catálogo de benefícios versionado em dados

Concluir o caminho aberto pela v1.1.0: tirar os benefícios do código e colocá-los em
**JSON versionado**, como já ocorre com `crimes.json`. Enquanto isso não existe, o
conferidor sabe vigiar tipos penais, mas não benefícios.

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

## v2.2.0 — Acervo histórico

Reunir **todos os tipos penais que deixaram de valer ou mudaram**, para histórico
completo — o que hoje nenhuma ferramenta oferece de forma estruturada, e que interessa
diretamente à pesquisa acadêmica (ultratividade da lei mais benéfica; linha do tempo da
descriminalização). O conferidor alimenta esta aba: revogação que ele detectar entra
aqui, em vez de desaparecer.

- [ ] **Aba própria** em Pesquisa ▸ **Acervo histórico**, com a lista de tipos **por
      categoria**: `revogado` · `alterado` · `nao_recepcionado` — no mesmo formato da
      lista de tipos vigentes
- [ ] **Tela de detalhe por tipo**: o **texto original** e o que houve com ele — alteração,
      revogação ou não recepção —, **quando** houve e **por qual dispositivo** (com link
      para o tipo sucessor, quando houver)
- [ ] **Dataset separado**: `data/historico.json` (fonte) → `static/data/historico.json`
      (derivado), com ids próprios
- [ ] Fonte: os textos anteriores do Planalto (as redações revogadas ficam no compilado —
      a mesma extração do conferidor); os 10 diplomas revogados/não recepcionados já estão
      inventariados em `data/diplomas.json`, e os casos já identificados estão listados em
      [Acervo histórico](/docs/acervo-historico)
- [ ] Ponto de partida já conhecido: adultério (art. 240), sedução (217), rapto (219–222),
      ECA art. 233, LCP arts. 27, 39, 60, 61 e 65, Lei de Imprensa, LSN, Estatuto do
      Torcedor, o art. 19 (vetado) da Lei 9.807/99 e as redações **alteradas** registradas
      nas conferências (art. 121, §2º VI — feminicídio; Maria da Penha art. 24-A…)

---

## v2.3.0 — Melhorias técnicas e de usabilidade

- [ ] **Acessibilidade**: navegação por teclado na tabela, `aria-live` nos contadores que
      mudam com a simulação, foco visível consistente
- [ ] **Busca textual** tolerante a acentos e erros de digitação
- [ ] **Exportar** o resultado da busca por benefício em CSV
- [ ] **Comparar dois benefícios** lado a lado sobre o mesmo catálogo
- [ ] Testes de regressão da dosimetria com casos reais de jurisprudência
- [ ] Dashboards analíticos (distribuição de penas, hediondos por década)

---

## v3.0.0 — Processo penal, jurisprudência e pesquisa de políticas públicas

A virada de paradigma: o sistema deixa de ser um catálogo de **direito material** e passa
a cobrir também o **processo penal** e a **jurisprudência** que regem, na prática, os
benefícios — e a servir de plataforma de pesquisa sobre a legislação, não só de consulta.
Só faz sentido depois que o direito material estiver consolidado e mantido sozinho.

### Processo penal e jurisprudência

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares ou
      vedações (ex.: Súmula 536 STJ)
- [ ] Alertas quando decisão vinculante invalidar uma regra implementada

### Plataforma de pesquisa

- [ ] Cruzamento exaustivo tipos × benefícios (matriz de elegibilidade)
- [ ] Simulação legislativa em lote ("aumentar em 2 anos a pena dos crimes patrimoniais")
- [ ] Séries temporais do endurecimento/abrandamento penal
- [ ] Exportação para pesquisa (CSV, JSON, API versionada)
- [ ] Esquema versionado dos dados abertos, com política de depreciação

:::note[Por que MAIOR]
Outro salto de natureza: o sistema deixa de responder "o que a lei comina para este
crime" e passa a responder "o que se aplica a este caso, nesta data, segundo a lei e os
tribunais". Limiares passam a depender de vigência temporal e de tese vinculante, e a
ferramenta de consulta vira plataforma de pesquisa. É expansão de paradigma e de
cobertura ao mesmo tempo.
:::
