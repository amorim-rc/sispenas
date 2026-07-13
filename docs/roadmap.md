---
id: roadmap
title: Roadmap
sidebar_position: 5
---

# Roadmap

## v1.0.0 (atual) — SISPENAS sobre Docusaurus

Plataforma de pesquisa com ferramenta interativa e documentação integrada.

- [x] Catálogo de 1.061 tipos penais de 65 diplomas
- [x] Migração para **Docusaurus** (navegação, docs e SEO)
- [x] Modelagem de **multa como dimensão independente** (reclusão/detenção + multa)
- [x] Filtros combinados por modalidade de pena, hediondez, elemento, violência, ação penal
- [x] **Cálculo dinâmico de benefícios penais** ao selecionar um tipo
- [x] **Simulação de alteração legislativa** (ajuste de pena → recálculo de benefícios em tempo real)
- [x] Dados abertos (JSON) + licença MIT com atribuição
- [ ] Revisão jurídica individual dos campos derivados
- [ ] Dashboards analíticos (distribuição de penas, hediondos por década)

---

## v1.1.0 — Atualização automática da legislação (crawler do DOU)

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

## v1.2.0 — Atualizações de Processo Penal

Estender o mesmo mecanismo de atualização automática para o **Direito Processual Penal**,
que rege boa parte dos benefícios (ANPP, transação, suspensão do processo, execução).

- [ ] Monitorar alterações do **CPP**, da **Lei 9.099/95** e da **LEP**
- [ ] Monitorar **súmulas e teses de repercussão geral** (STF/STJ) que alterem limiares
      ou vedações de benefícios (ex.: Súmula 536 STJ)
- [ ] Base versionada de **regras de benefícios** (patamares, frações, vedações) separada
      do código, para atualização sem redeploy
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

## Contribuição

Prioridades:

1. Revisão dos campos derivados (multa, menor potencial ofensivo)
2. Expansão e correção do catálogo
3. Refinamento das regras de benefícios conforme jurisprudência consolidada
