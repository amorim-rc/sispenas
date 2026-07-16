---
id: roadmap
title: Roadmap
sidebar_position: 5
---

# Roadmap

## v1.0.0 — SISPENAS sobre Docusaurus

Plataforma de pesquisa com ferramenta interativa e documentação integrada.

- [x] Catálogo de 1.061 tipos penais de 65 diplomas
- [x] Migração para **Docusaurus** (navegação, docs e SEO)
- [x] Modelagem de **multa como dimensão independente** (reclusão/detenção + multa)
- [x] Filtros combinados por modalidade de pena, hediondez, elemento, violência, ação penal
- [x] **Cálculo dinâmico de benefícios penais** ao selecionar um tipo
- [x] **Simulação de alteração legislativa** (ajuste de pena → recálculo de benefícios em tempo real)
- [x] Dados abertos (JSON) + licença MIT com atribuição

---

## v1.1.0 (atual) — Busca por benefício e catálogo declarativo

Inversão do percurso de pesquisa e reescrita do motor de benefícios como **registro
de dados**, não como regras embutidas no código.

- [x] **Landing page** com o texto institucional "Sobre o SISPENAS"
- [x] Navbar reorganizada: *Sobre o SISPENAS*, *Pesquisa* ▾, *Documentação* ▾, *Roadmap*
- [x] **Busca por tipo penal** movida para `/pesquisa/tipos` (fluxo direto, preservado)
- [x] **Busca por benefício** (`/pesquisa/beneficios`) — fluxo inverso: benefício →
      requisitos, vedações e patamares → **tipos penais afetados**
- [x] **Registro declarativo de benefícios** (`BeneficioDef`): metadados, requisitos,
      vedações, parâmetros editáveis com fundamento legal e função pura de avaliação
- [x] **Edição de qualquer atributo do benefício** com recálculo imediato do catálogo
- [x] Indicador de **delta de alcance**: quantos tipos penais a alteração inclui/exclui
- [x] Catálogo ampliado de **13 para 22 benefícios** (perdão judicial, arrependimento
      posterior, desistência/arrependimento eficaz, colaboração premiada, prisão
      domiciliar, monitoração eletrônica, comutação, graça, unificação de penas)
- [x] Correção: substituição por PRD nos **crimes culposos** independe do quantum da
      pena (art. 44, I, parte final) — antes documentado, não implementado
- [x] `npm run verificar` — invariantes do motor + casos-âncora de direito penal
      contra o catálogo real, integrado à CI
- [x] Correções de contraste no **modo escuro**; redirecionamento das URLs da v1.0.0

### Lacunas conhecidas desta versão

- [ ] O catálogo não registra, tipo a tipo, o **resultado morte** — hoje é um controle
      global da simulação, e não um dado do tipo penal
- [ ] O catálogo não registra a **previsão expressa de perdão judicial** por tipo
- [ ] Revisão jurídica individual dos campos derivados
- [ ] Dashboards analíticos (distribuição de penas, hediondos por década)

---

## v1.2.0 — Catálogo de benefícios versionado em dados

Concluir o caminho aberto pela v1.1.0: tirar os benefícios do código e colocá-los em
**JSON versionado**, como já ocorre com `crimes.json`.

- [ ] Serializar `BeneficioDef` para `data/beneficios.json` (metadados, requisitos,
      vedações e parâmetros), mantendo em código apenas as funções de avaliação
- [ ] Vocabulário de **predicados de avaliação** declarativos (`penaMax <= X`,
      `semViolencia`, `naoReincidente`) para dispensar código em benefícios simples
- [ ] Campo `resultado_morte` e `perdao_judicial_previsto` no catálogo de tipos penais
- [ ] **Vigência temporal**: qual redação de cada benefício vigia em cada data
      (ex.: art. 112 da LEP antes e depois da Lei 13.964/2019)
- [ ] CI de validação do catálogo de benefícios (frações em [0,1], fundamentos citados)
- [ ] Permalink de simulação: URL que carrega os parâmetros editados

---

## v1.3.0 — Atualização automática da legislação (crawler do DOU)

Manter o catálogo atualizado com segurança jurídica, a partir do **Diário Oficial da
União (DOU)**.

### Arquitetura proposta

```
GitHub Actions (cron semanal)
   → Crawler do DOU (Imprensa Nacional / in.gov.br)
   → Filtro por seção e por palavras-chave penais (pena, reclusão, detenção, revoga, art.)
   → Agente de IA classifica: cria / altera / revoga tipo penal?
   → Gera proposta de alteração no crimes.json
   → Abre Pull Request (NUNCA commita direto no main)
   → CI valida (penas coerentes, sem duplicatas, hediondez, referências cruzadas)
   → Revisão humana obrigatória (competência jurídica) antes do merge
```

### Tarefas

- [ ] Coletor do DOU (fonte oficial `in.gov.br`), com paginação e cache
- [ ] Normalizador de texto (extrair artigo, pena mín/máx, modalidade)
- [ ] Classificador (IA) de impacto penal com citação rastreável à fonte
- [ ] Gerador de diff estruturado sobre `crimes.json`
- [ ] Abertura automática de PR + changelog
- [ ] CI de validação de dados (limites de pena, duplicatas, hediondez Lei 8.072/90)
- [ ] Trilha de auditoria (data da norma, link do DOU, responsável pela revisão)

---

## v1.4.0 — Atualizações de Processo Penal

Estender o mesmo mecanismo de atualização automática para o **Direito Processual Penal**,
que rege boa parte dos benefícios (ANPP, transação, suspensão do processo, execução).

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares
      ou vedações de benefícios (ex.: Súmula 536 STJ)
- [ ] Alertas quando uma decisão vinculante invalidar uma regra implementada
- [ ] Registro temporal: qual regra de benefício vigia em cada data

---

## v2.0.0 — Plataforma de pesquisa de políticas públicas

- [ ] Cruzamento exaustivo tipos × benefícios (matriz de elegibilidade)
- [ ] Simulação legislativa em lote ("aumentar em 2 anos a pena de todos os crimes contra o patrimônio")
- [ ] Séries temporais do endurecimento/abrandamento penal
- [ ] Exportação para pesquisa (CSV, JSON, API)
- [ ] Colaboração da comunidade jurídica (propostas de correção via PR)

---

## Melhorias transversais (sem versão fixa)

Itens de menor porte, incorporáveis a qualquer ciclo:

- [ ] **Acessibilidade**: navegação por teclado na tabela de resultados, `aria-live`
      nos contadores que mudam com a simulação, foco visível consistente
- [ ] **Busca textual** com tolerância a acentos e erros de digitação
- [ ] **Exportar resultado** da busca por benefício em CSV
- [ ] **Comparar dois benefícios** lado a lado sobre o mesmo catálogo
- [ ] Testes de regressão da dosimetria com casos reais de jurisprudência
- [ ] Concurso de crimes (material, formal, continuidade delitiva) na simulação

---

## Contribuição

Prioridades:

1. Revisão dos campos derivados (multa, menor potencial ofensivo)
2. Expansão e correção do catálogo
3. Refinamento das regras de benefícios conforme jurisprudência consolidada
