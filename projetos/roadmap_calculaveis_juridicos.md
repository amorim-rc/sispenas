# Roadmap — Calculáveis Jurídicos (algo-calc)

## Visão Geral

Plataforma SaaS de calculadoras jurídicas para advogados, com foco em automação de cálculos repetitivos que hoje consomem horas de trabalho manual. Modelo freemium com geração de PDF para download.

---

## 1. Validação das Ideias

### Classificação por Viabilidade × Demanda × Complexidade

| # | Calculável | Demanda | Complexidade | Prioridade | Notas |
|---|-----------|---------|-------------|-----------|-------|
| **TRIBUTÁRIO** |||||
| T1 | Exclusão ICMS do PIS/COFINS | Altíssima | Alta | P1 | "Tese do século" (RE 574.706). Mercado enorme de escritórios executando. Precisa de upload de NFs (XML ou manual) |
| T2 | Simulador Simples × Presumido × Real | Alta | Média | P1 | Todo contador/advogado tributarista precisa. Dados: faturamento, folha, despesas dedutíveis |
| T3 | Revisão de ITBI | Média | Baixa | P2 | Compara valor venal × valor declarado × valor da guia. Simples mas nicho |
| T4 | Apuração de ganho de capital | Alta | Média | P2 | Progressividade (15-22,5%), isenções (único imóvel < R$440k, reinvestimento 180 dias) |
| **TRABALHO** |||||
| L1 | Calculadora de cartão de ponto | Altíssima | Média | P0 | Dor gigante — advogados fazem manualmente em Excel. Upload de espelho de ponto |
| L2 | Simulador de passivo trabalhista | Alta | Alta | P2 | Estima risco financeiro total. Útil para departamentos jurídicos |
| L3 | Reflexos em cascata | Altíssima | Alta | P1 | HE → DSR → FGTS+40% → Férias+1/3 → 13º → INSS. Diferencial competitivo forte |
| **PREVIDENCIÁRIO** |||||
| P1 | Regras de transição (EC 103/2019) | Altíssima | Média | P1 | 5 regras: pedágio 50%, pedágio 100%, idade mínima progressiva, pontos, idade mínima |
| P2 | Liquidação de atrasados | Alta | Alta | P2 | Correção mês a mês com juros + índices (INPC, Selic pós-12/2021) |
| P3 | Conversor tempo especial→comum | Alta | Baixa | P1 | Multiplicadores: 1.4 (homem) e 1.2 (mulher) para 25 anos; variações para 15 e 20 |
| **IMOBILIÁRIO** |||||
| I1 | Lei do Distrato (13.786/2018) | Média | Baixa | P2 | Patrimônio de afetação (50% devolução) vs sem (75%). Dedução de fruição |
| I2 | Revisional de aluguel | Média | Média | P3 | Índices (IGP-M, IPCA, IVAR) + defasagem do valor de mercado |
| I3 | Simulador SAC vs PRICE | Alta | Baixa | P1 | Clássico, simples de implementar, atrai tráfego orgânico (SEO) |
| **FAMÍLIA E SUCESSÕES** |||||
| F1 | Simulador de partilha | Alta | Média | P2 | Meação (50%) + herança (legítima × disponível). Regimes de bens × ordem de vocação |
| F2 | Calculadora de ITCMD | Alta | Média | P2 | Alíquotas por estado (4-8%), faixas progressivas em SP/RJ, isenções |
| F3 | Execução de alimentos atrasados | Alta | Média | P1 | Juros 1% a.m. + correção (INPC ou índice do TJ) + multa 10% (Art. 523 CPC) |
| **CIVIL GERAL** |||||
| C1 | Multa rescisória proporcional | Média | Baixa | P3 | Art. 413 CC — proporcionaliza a multa ao % cumprido do contrato |
| C2 | Atualizador universal de débitos | Altíssima | Alta | P0 | KILLER FEATURE. Índices de todos os TJs, INPC, IPCA, Selic. Tabela de evolução para petição |

### Legenda de Prioridade
- **P0** = MVP (lançamento) — máxima demanda × complexidade viável
- **P1** = Sprint 2 (1-2 meses pós-MVP)
- **P2** = Sprint 3-4
- **P3** = Backlog (validar demanda antes)

---

## 2. Expansões e Ideias Novas

### Expansões sobre as ideias originais

| Área | Expansão | Justificativa |
|------|----------|---------------|
| Tributário | **Exclusão ISS da base PIS/COFINS** | "Tese filhote" da exclusão do ICMS — mesmo motor de cálculo, mercado crescente |
| Tributário | **Recuperação de créditos PIS/COFINS sobre insumos** | Pós-STJ (REsp 1.221.170). Mesmo público-alvo do T1 |
| Tributário | **Calculadora de DIFAL** (diferencial de alíquota) | E-commerce → muita demanda pós-EC 87/2015 |
| Trabalho | **Cálculo de rescisão completa** | FGTS + multa 40% + aviso prévio proporcional + férias + 13º proporcional. Complementa L1 |
| Trabalho | **Simulador de acordo extrajudicial** (Art. 855-B CLT) | Quanto oferecer vs passivo projetado. Útil para empresas |
| Previdenciário | **Revisão da vida toda** (Tema 1102 STF) | Recalcular RMI com contribuições anteriores a 07/1994. Altíssima demanda |
| Previdenciário | **Planejamento de contribuição** | "Quanto contribuir por mês para aposentar com valor X em data Y" |
| Imobiliário | **Cálculo de usucapião** | Prazo × modalidade × requisitos checklist. Simples mas atrai tráfego |
| Família | **Cálculo de alimentos** (fixação) | Trinômio necessidade-possibilidade-proporcionalidade. Mais qualitativo |
| Civil | **Calculadora de juros abusivos** (revisional bancária) | Compara taxa contratada vs taxa média BACEN. Mercado enorme |
| Civil | **Danos morais — parâmetros STJ** | Tabelamento por tipo de dano (negativação, morte, etc.). Orientativo |

### Ideias 100% novas

| # | Ideia | Demanda | Complexidade | Justificativa |
|---|-------|---------|-------------|---------------|
| N1 | **Calculadora de precatórios** (atualização + deságio de mercado) | Alta | Média | Quem compra/vende precatórios precisa disso. Mercado bilionário |
| N2 | **Simulador de custas processuais** (por tribunal) | Altíssima | Média | Todo advogado precisa antes de ajuizar. Tabelas de cada TJ |
| N3 | **Calculadora de honorários sucumbenciais** | Alta | Baixa | Art. 85 CPC: 10-20% sobre o proveito econômico. Rápido de fazer |
| N4 | **Contador de prazos processuais** (dias úteis, recesso, suspensões) | Altíssima | Média | Integra com feriados nacionais + estaduais + recessos. Crítico para advocacia |
| N5 | **Simulador de recuperação judicial** (plano de pagamento) | Média | Alta | Deságio + prazo + carência. Nicho lucrativo |
| N6 | **Calculadora de desapropriação** (justa indenização + juros compensatórios) | Média | Média | Juros compensatórios 12% a.a. + correção + honorários sobre a diferença |

---

## 3. Roadmap de Execução

### Fase 0 — MVP (Semanas 1-3)
> **Objetivo:** Lançar com 2-3 calculadoras de altíssima demanda para validar produto

| Calculável | Escopo MVP | Entregável |
|-----------|-----------|-----------|
| **C2 — Atualizador de débitos** | 5 índices (IPCA, INPC, Selic, IGP-M, TJSP) + juros 1% a.m. ou Selic | Tabela de evolução + PDF |
| **L1 — Cartão de ponto** | Input manual de horários (entrada/saída × 30 dias) → HE 50%, 100%, noturno | Resumo + PDF |
| **I3 — SAC vs PRICE** | Valor, entrada, taxa, prazo → comparativo com gráficos | Comparativo visual + PDF |

**Infraestrutura MVP:**
- Landing page + 3 calculadoras
- Sem login (acesso livre)
- PDF gerado client-side (jsPDF)
- Deploy gratuito (Vercel/Netlify)

### Fase 1 — Expansão + Monetização (Semanas 4-8)
> **Objetivo:** Adicionar as calculadoras mais complexas + sistema de assinatura

| Calculável | Escopo |
|-----------|--------|
| **L3 — Reflexos em cascata** | HE → DSR → FGTS → Férias → 13º → INSS. Motor de cascata genérico |
| **T2 — Simples × Presumido × Real** | Faturamento anual + despesas → comparativo tributário |
| **P1 — Regras de transição** | Idade + tempo contribuição → 5 cenários + data mais cedo |
| **P3 — Conversor tempo especial** | Períodos especiais → tempo convertido → quanto falta |
| **F3 — Execução de alimentos** | Valor × meses + correção + juros + multa Art. 523 |
| **T1 — Exclusão ICMS (simplificado)** | Input manual: valor NF, ICMS destacado, PIS/COFINS recolhido → crédito |

**Infraestrutura Fase 1:**
- Auth (login social Google/email)
- Histórico de cálculos do usuário
- PDF estilizado com marca d'água
- Plano gratuito (3 cálculos/mês) + Plano Pro

### Fase 2 — Plataforma Completa (Semanas 9-16)
> **Objetivo:** Cobertura ampla + funcionalidades premium

| Calculável | Escopo |
|-----------|--------|
| **C2 expandido** — todos os índices de todos os TJs | Scraping ou API de índices oficiais |
| **L2 — Passivo trabalhista** | Cenários (melhor/pior caso) + provisão contábil |
| **T1 completo** — upload de XMLs de NF-e | Parser de NF-e → cálculo automático em lote |
| **T4 — Ganho de capital** | Progressividade + isenções + GCAP simplificado |
| **P2 — Liquidação de atrasados** | Mês a mês com índices oficiais + Selic pós-2021 |
| **F1 — Simulador de partilha** | Regime de bens + herdeiros + bens → distribuição |
| **F2 — ITCMD** | Alíquotas por estado (27 UFs) + simulação |
| **I1 — Lei do Distrato** | % devolução + fruição + correção |
| **N2 — Custas processuais** | Tabelas de pelo menos 5 TJs principais |
| **N4 — Prazos processuais** | Calendário com dias úteis + feriados + recessos |

**Infraestrutura Fase 2:**
- Dashboard completo do usuário
- API de índices econômicos atualizada automaticamente
- Geração de petição-template em .docx
- White-label para escritórios (subdomínio próprio)

### Fase 3 — Enterprise + IA (Semanas 17+)
> **Objetivo:** Monetização B2B + diferenciação por IA

- Multi-tenant para escritórios (gestão de processos + cálculos integrados)
- OCR para upload de documentos (cartão de ponto escaneado, NFs em PDF)
- IA para sugestão de teses (com base nos dados inseridos)
- Integração com PJe/PROJUDI (consulta de processos)
- App mobile
- N1, N3, N5, N6 e demais calculadoras do backlog

---

## 4. Modelos de Negócio

### Modelo Recomendado: Freemium + Assinatura

| Plano | Preço | Inclui |
|-------|-------|--------|
| **Gratuito** | R$ 0 | 3 cálculos/mês, sem PDF, sem histórico |
| **Essencial** | R$ 29/mês | Cálculos ilimitados + PDF + histórico 30 dias |
| **Profissional** | R$ 79/mês | Tudo + todos os índices + petição-template + histórico ilimitado |
| **Escritório** | R$ 199/mês | Tudo + 5 usuários + marca própria no PDF + API |

### Alternativas de monetização complementar

1. **Pay-per-use com créditos:** R$ 2-5 por cálculo complexo (ex: exclusão ICMS com 100+ NFs)
2. **Curso/mentoria integrado:** "Como usar a calculadora para peticionar" → upsell educacional
3. **Afiliação com contadores/fintechs:** Lead generation para serviços complementares
4. **White-label B2B:** Vender o motor de cálculo para plataformas jurídicass (Jusbrasil, Themis, etc.)

### Projeção de receita (conservadora)

| Mês | Usuários free | Assinantes | MRR |
|-----|--------------|-----------|-----|
| 3 | 500 | 15 (3%) | R$ 1.200 |
| 6 | 2.000 | 80 (4%) | R$ 4.500 |
| 12 | 8.000 | 400 (5%) | R$ 25.000 |
| 24 | 30.000 | 1.500 (5%) | R$ 90.000 |

---

## 5. Arquitetura Técnica — Baixo Custo

### Stack Recomendada (custo R$0 até ~1.000 usuários ativos)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Gratuito)                    │
│  Next.js (ou Astro) → Deploy: Vercel (free tier)         │
│  - SSG para landing/SEO                                  │
│  - CSR para calculadoras (lógica no browser)             │
│  - PDF: jsPDF + html2canvas (client-side, zero server)   │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│               BACKEND/AUTH (Gratuito até 50k MAU)        │
│  Supabase (free tier):                                   │
│  - Auth (Google, email/password)                         │
│  - PostgreSQL 500MB (histórico de cálculos)              │
│  - Row Level Security (privacidade)                      │
│  - Edge Functions (serverless, para índices)             │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              PAGAMENTOS (só cobra taxa por transação)     │
│  Stripe ou Mercado Pago                                  │
│  - Sem custo fixo                                        │
│  - Taxa: 2.49-3.99% por transação                        │
└─────────────────────────────────────────────────────────┘
```

### Custo mensal estimado

| Componente | Custo (até 1k users) | Custo (1k-10k users) |
|-----------|---------------------|---------------------|
| Vercel (hosting) | R$ 0 | R$ 0 (free tier cobre) |
| Supabase (auth + DB) | R$ 0 | R$ 125/mês (Pro) |
| Domínio (.com.br) | R$ 40/ano | R$ 40/ano |
| **Total** | **~R$ 3/mês** | **~R$ 130/mês** |

### Sobre login sem servidor tradicional

Você **não precisa** de servidor próprio para auth. Supabase/Firebase oferecem:
- Login com Google/email (zero código de backend)
- Banco de dados PostgreSQL com API REST automática
- Row Level Security (cada usuário só vê seus dados)
- Tudo via SDK JavaScript direto do frontend

O único custo de "servidor" real surge quando você precisar de:
- Scraping de índices econômicos (cron job) → resolvido com Supabase Edge Functions ou GitHub Actions (gratuito)
- Processamento pesado de XMLs de NF-e → resolvido com serverless (Vercel Functions)

### Privacidade de dados

Opção de **zero-storage**: os cálculos rodam 100% no browser, o resultado só existe enquanto a aba está aberta. O PDF é gerado client-side. Nenhum dado financeiro toca o servidor. O banco só guarda metadados (data do cálculo, tipo, resultado numérico) para histórico — e o usuário pode deletar a qualquer momento (LGPD compliance by design).

---

## 6. xlsx vs Site Direto — Recomendação

### Resposta curta: **Vá direto ao site para 90% dos casos.**

### Quando usar xlsx primeiro:
| Cenário | Exemplo | Motivo |
|---------|---------|--------|
| Lógica com muitas variáveis interdependentes | Reflexos em cascata (L3) | Testar a cascata célula por célula antes de codificar |
| Precisa validar com dados reais do cliente | Exclusão ICMS (T1) com NFs reais | Excel permite colar dados e ver resultado instantâneo |
| Fórmula juridicamente controversa | Liquidação de atrasados (P2) | Diferentes tribunais usam métodos diferentes — validar com advogado antes |

### Quando ir direto ao site:
| Cenário | Exemplo | Motivo |
|---------|---------|--------|
| Fórmula determinística e bem definida | SAC vs PRICE (I3), Ganho de capital (T4) | Não há ambiguidade, código direto |
| Calculadora simples (< 5 inputs) | Conversor tempo especial (P3), Multa proporcional (C1) | Mais rápido codificar que montar planilha |
| Precisa de UI interativa | Regras de transição (P1) — slider de idade/tempo | Excel não mostra isso bem |
| Precisa de gráficos/visualização | Simulador SAC vs PRICE, passivo trabalhista | Chart.js > gráficos do Excel |

### Fluxo recomendado com o Devin:

```
1. Definir inputs/outputs + fórmula jurídica (em texto/pseudocódigo)
2. Eu implemento direto no site (JS/TS)
3. Você testa com dados reais
4. Iteramos até convergir
```

A planilha só entra quando a fórmula é tão complexa que você precisa "debugar célula por célula" (reflexos em cascata, exclusão ICMS com dezenas de NFs). Nos demais casos, o ciclo "texto → código → teste" é mais rápido.

---

## 7. Sequência de Desenvolvimento Sugerida

```
Semana 1:   Infraestrutura (Next.js + Supabase + deploy)
Semana 2:   C2 (Atualizador de débitos) — KILLER FEATURE, atrai tráfego
Semana 3:   L1 (Cartão de ponto) + I3 (SAC vs PRICE)
            → LANÇAMENTO MVP (3 calculadoras + landing page)
Semana 4:   Auth + histórico + PDF branded
Semana 5:   L3 (Reflexos em cascata) — validar com xlsx primeiro
Semana 6:   P1 (Regras de transição) + P3 (Conversor tempo especial)
Semana 7:   T2 (Simples × Presumido × Real)
Semana 8:   F3 (Execução de alimentos) + T1 simplificado
            → LANÇAMENTO PLANO PRO (monetização ativa)
Semana 9+:  Uma calculadora nova por semana, priorizando por demanda
```

---

## 8. Nome e Posicionamento

### Sugestões de nome para o produto:

| Nome | Domínio | Posicionamento |
|------|---------|---------------|
| **CalcJur** | calcjur.com.br | Direto, fácil de lembrar |
| **JuriCalc** | juricalc.com.br | Similar, mais "jurídico" |
| **algo-calc** | algocalc.com.br | Continua o branding algo-pen |
| **PetCalc** | petcalc.com.br | "Cálculos para sua petição" |
| **Quantus** | quantus.adv.br | Latim para "quanto" — sofisticado |

### Tagline sugerida:
> "Calculadoras jurídicas para advogados que valorizam seu tempo."

---

## 9. Concorrência e Diferencial

### Concorrentes existentes:
- **Cálculo Jurídico** (calculojuridico.com.br) — R$99-249/mês, foco trabalhista/previdenciário
- **JusBrasil Cálculos** — integrado ao ecossistema JusBrasil
- **CJFast** — focado em cálculos trabalhistas
- **Prev&Calc** — focado em previdenciário

### Seu diferencial:
1. **Preço agressivo** (R$29 vs R$99+ dos concorrentes)
2. **Cobertura multi-área** (tributário + trabalhista + previdenciário + imobiliário + família + civil num só lugar)
3. **Técnologia moderna** (UX superior, mobile-first, PDF instantâneo)
4. **Transparência da fórmula** (mostra o cálculo passo a passo, não é caixa-preta)
5. **Freemium real** (não trial de 7 dias — uso gratuito limitado permanente)
6. **Privacidade** (opção zero-storage, cálculos no browser)

---

*Documento gerado em 2026-06-07. Revisão contínua conforme validação de mercado.*
