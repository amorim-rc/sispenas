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
| **MAIOR** (`X.0.0`) | Quebra de compatibilidade para esses públicos: remoção ou renomeação de campo do JSON, mudança de significado de campo existente, reatribuição de `id`, remoção de rota sem redirecionamento. | Migrar o catálogo para um esquema novo; separar `crimes.json` em vários arquivos. |
| **MENOR** (`1.Y.0`) | Funcionalidade nova mantendo compatibilidade: **acrescentar** campo ao JSON, nova tela, novo benefício, nova rota. | A v1.1.0 acrescentou `resultado_morte` e a Busca por benefício sem remover nada. |
| **CORREÇÃO** (`1.1.Z`) | Correção sem funcionalidade nova: erro de dosimetria, dado errado no catálogo, defeito de interface. | Corrigir a pena de um artigo; ajustar contraste. |

:::note Correção de dado é `CORREÇÃO`, não `MENOR`
Resolver uma das 48 contradições do catálogo muda o resultado de uma consulta — mas
corrige um erro, não acrescenta capacidade. Vai em `1.1.Z`. Já **acrescentar um campo**
que não existia (`resultado_morte`) é `MENOR`, ainda que motivado por um erro: consumidores
do JSON ganham informação sem perder nenhuma.
:::

**Versões anteriores.** O roadmap original numerava por ordem de intenção, não por
compatibilidade: o crawler do DOU figurava como "v1.1.0" e a plataforma de pesquisa como
"v2.0.0" sem que nenhuma das duas quebrasse contrato. A numeração abaixo foi refeita
segundo a tabela acima.

---

## v1.0.0 — SISPENAS sobre Docusaurus

Plataforma de pesquisa com ferramenta interativa e documentação integrada.

- [x] Catálogo de 1.061 registros de 65 diplomas
- [x] Migração para **Docusaurus** (navegação, docs e SEO)
- [x] Modelagem de **multa como dimensão independente** (reclusão/detenção + multa)
- [x] Filtros combinados por modalidade de pena, hediondez, elemento, violência, ação penal
- [x] **Cálculo dinâmico de benefícios penais** ao selecionar um tipo
- [x] **Simulação de alteração legislativa** (ajuste de pena → recálculo em tempo real)
- [x] Dados abertos (JSON) + licença MIT com atribuição

---

## v1.1.0 (atual) — Busca por benefício e catálogo declarativo

Inversão do percurso de pesquisa, reescrita do motor de benefícios como **registro de
dados** e primeira auditoria sistemática da integração catálogo ↔ benefícios.

### Interface

- [x] **Landing page** com o texto institucional "Sobre o SISPENAS"
- [x] Navbar: *Sobre o SISPENAS*, *Pesquisa* ▾, *Documentação* ▾, *Roadmap*
- [x] **Busca por tipo penal** em `/pesquisa/tipos` (fluxo direto, preservado)
- [x] **Busca por benefício** em `/pesquisa/beneficios` — benefício → requisitos, vedações,
      patamares editáveis → **tipos penais afetados**, com delta de alcance
- [x] Correções de contraste no modo escuro; redirecionamento das URLs da v1.0.0

### Motor de benefícios

- [x] **Registro declarativo** (`BeneficioDef`): metadados, requisitos, vedações,
      parâmetros editáveis com fundamento legal e função pura de avaliação
- [x] Catálogo ampliado de **13 para 22 benefícios**
- [x] Correção: substituição por PRD nos **crimes culposos** independe do quantum da pena
      (art. 44, I, parte final) — antes documentado, não implementado

### Integridade dos dados

- [x] `avaliavel` — exclui das estatísticas os **22 registros sem pena própria** (notas de
      referência, agravantes); com pena zero, satisfaziam qualquer teto e eram contados
      como "cabíveis"
- [x] `resultado_morte` no catálogo — antes era um interruptor global da simulação
- [x] `perdao_judicial_previsto` — lista curada de dispositivos; o perdão não se infere do
      elemento culposo nem se estende por analogia
- [x] Detecção de **duplicatas** e de **duplicatas divergentes** (contradições)
- [x] Relatório `static/data/qualidade.json` a cada regeneração
- [x] Invariantes duros de `id` (é a URL pública; append-only)
- [x] `npm run verificar` + validação estrita do catálogo na CI

---

## v1.1.Z — Correções conhecidas (em aberto)

Erros já identificados, sem funcionalidade nova. Prioridade máxima: são o que separa o
SISPENAS de ser citável como referência.

- [ ] **Resolver as 48 duplicatas divergentes** — mesmo dispositivo com penas ou hediondez
      conflitantes (ex.: `CP, Art. 127` com 16–64 **vs.** 24–120 meses). Enquanto não
      resolvidas, ambas as versões são exibidas e sinalizadas.
- [ ] **Deduplicar os 365 registros repetidos** (878 dispositivos distintos em 1.061
      registros) — decidir entre fundir ou distinguir por incisos.
- [ ] Revisão jurídica individual dos campos `derivado_auto` (multa, menor potencial)
- [ ] Revisar `resultado_morte` nos casos ambíguos (ex.: `CP, Art. 158, §3º`, que remete a
      lesão grave **e** morte no mesmo registro)
- [ ] Catalogar as hipóteses de perdão judicial ausentes (art. 140, §1º; art. 176, par.
      único; CTB art. 291 c/c CP 121, §5º)

---

## v1.2.0 — Catálogo de benefícios versionado em dados

Concluir o caminho aberto pela v1.1.0: tirar os benefícios do código e colocá-los em
**JSON versionado**, como já ocorre com `crimes.json`. É o pré-requisito do v1.3.0 —
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

## v1.3.0 — Atualização automática da legislação (crawler do DOU)

Manter o catálogo atualizado com segurança jurídica, a partir do **Diário Oficial da
União**. O pipeline de dados da v1.1.0 já foi desenhado para receber isto: fonte editável
separada do derivado, invariantes de `id`, validação estrita na CI e relatório de
qualidade.

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

---

## v1.4.0 — Processo penal e jurisprudência

Estender a atualização automática ao **Direito Processual Penal**, que rege boa parte dos
benefícios. Depende da vigência temporal da v1.2.0.

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares ou
      vedações (ex.: Súmula 536 STJ)
- [ ] Alertas quando decisão vinculante invalidar uma regra implementada

---

## v1.5.0 — Dosimetria completa

Hoje o sistema parte da pena cominada. Uma referência em dosimetria precisa percorrer as
três fases do art. 68 do CP.

- [ ] **Circunstâncias judiciais** (art. 59) — pena-base
- [ ] **Agravantes e atenuantes** (arts. 61 a 66) — 2ª fase
- [ ] **Causas de aumento e diminuição** — 3ª fase, hoje ausentes do cálculo
- [ ] **Concurso de crimes**: material (art. 69), formal (art. 70), continuidade (art. 71)
- [ ] Súmula 231, STJ (atenuante não reduz abaixo do mínimo) como regra explícita

---

## v2.0.0 — Plataforma de pesquisa de políticas públicas

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
