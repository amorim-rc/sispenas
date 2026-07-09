# Ecossistema de Automação para Advocacia Solo

**Projeto:** esteira ponta-a-ponta para captar, atender, peticionar, acompanhar e cobrar — operada por 1 advogado com apoio intensivo de IA.
**Data:** 2026-07-02 · Documento de arquitetura (v1, para validação e refinamento)

---

## 0. Leia antes de tudo — Guardrails éticos e legais (não são opcionais)

Automação em advocacia esbarra em regras da **OAB** e na **LGPD**. Ignorá-las coloca a OAB e o próprio negócio em risco. Trate esta seção como requisito de arquitetura, não como "detalhe jurídico".

| Tema | Regra prática | Impacto na arquitetura |
|------|---------------|------------------------|
| **Captação/publicidade** | Provimento 205/2021 + 94/2000 CFOAB: proibido mercantilizar a profissão, captar clientela, prometer resultado, usar "gatilhos" de marketing agressivo. Permitido marketing de conteúdo informativo e sóbrio. | O módulo de "captação" deve ser **inbound informativo** (conteúdo, calculadoras, SEO) — nunca disparo em massa/cold outreach ou promessa de êxito. Chatbot não pode "vender", só informar e agendar. |
| **Sigilo profissional** | Dados de cliente e do caso são sigilosos. IA de terceiros que "treina" com seus dados é problema. | Usar provedores com **zero data retention / no-training** (Anthropic API, OpenAI API com opt-out — não os chats de consumidor). Isolar dados por cliente. Criptografia. |
| **LGPD** | Base legal para tratar dados (execução de contrato + consentimento p/ gravação de reunião), direito de eliminação, registro de operações. | Consentimento explícito antes de gravar/transcrever reunião. Retenção definida. Trilha de auditoria. DPA assinado com cada fornecedor (Google, Anthropic, etc.). |
| **Responsabilidade profissional** | A peça é sua responsabilidade. IA redige rascunho; advogado revisa e assina. "Alucinação" de jurisprudência já gerou punições (inclusive nos EUA). | Todo output de IA é **rascunho com citações rastreáveis à fonte** (RAG com link), nunca peça final automática. Etapa obrigatória de revisão humana antes de protocolo. |
| **Honorários/publicidade de preço** | Tabela de honorários e captação por preço têm limites na OAB. | Evite "preços" agressivos no site jurídico (diferente do SaaS de calculadoras, que é produto, não advocacia). Separe as duas marcas. |

> **Decisão de marca:** mantenha o SaaS de calculadoras (`algo-calc`) e o **escritório** como marcas/entidades separadas. O SaaS pode fazer marketing como produto; o escritório segue as regras da OAB. O ecossistema deste documento é o do **escritório** (uso pessoal), com o SaaS podendo ser um funil de entrada.

---

## 1. Visão do ecossistema

A esteira transforma um lead em petição inicial revisável com o mínimo de trabalho manual, mantendo qualidade e conformidade. Sete módulos conectados por uma **camada de orquestração**:

```
                         ┌───────────────────────────────────────────────┐
                         │        CAMADA DE ORQUESTRAÇÃO (n8n)            │
                         │  eventos → workflows → chamadas de IA/APIs     │
                         └───────────────────────────────────────────────┘
   (1)          (2)              (3)            (4)                (5)
┌────────┐  ┌──────────┐   ┌───────────┐  ┌────────────┐   ┌──────────────┐
│Captação│→ │Qualificação│→│Agendamento│→ │Reunião +   │→  │Pipeline de IA│
│ /leads │  │+ chatbot   │ │(Calendar) │  │transcrição │   │→ Drive+peça  │
└────────┘  └──────────┘   └───────────┘  └────────────┘   └──────┬───────┘
                                                                   │
        ┌──────────────────────────────────────────────────────────┤
        ▼                          ▼                                ▼
┌──────────────┐         ┌────────────────────┐          ┌──────────────────┐
│(6) Base de    │         │(7) Prazos          │          │(8) Financeiro    │
│conhecimento   │         │processuais +       │          │(Sheets/DB) +     │
│jurídico (RAG) │         │notificação cliente │          │cobrança          │
└──────────────┘         └────────────────────┘          └──────────────────┘
```

A **jornada canônica do cliente** (o "happy path"):

1. Lead chega pelo site/calculadora/indicação → preenche formulário curto.
2. Chatbot qualifica (área, urgência, resumo do problema) em linguagem simples, sem prometer nada.
3. Se qualificado, oferece horários reais da sua agenda → agenda reunião no Google Calendar + gera link do Meet.
4. Reunião no Meet é **gravada/transcrita** (com consentimento).
5. Fim da reunião dispara o pipeline de IA: transcrição → estruturação dos fatos → criação de pasta no Drive → rascunho da **petição inicial** (fatos completos narrados) + **lista de teses** para o resto da peça → agenda reunião de revisão.
6. Você revisa fatos + teses com o cliente, ajusta, assina, protocola.
7. Sistema passa a monitorar prazos do processo e **notifica o cliente em linguagem simples** sobre andamentos; agenda reuniões que o cliente pedir.
8. Financeiro registra honorários, contrato, recebíveis; dispara cobranças.

---

## 2. Stack recomendada (visão geral)

Princípio: **serverless + no-code/low-code onde der, código só no núcleo jurídico-sensível**. Baixo custo fixo, escala por uso.

| Camada | Ferramenta principal | Alternativas | Por quê |
|--------|---------------------|--------------|---------|
| Orquestração | **n8n** (self-host no Railway/Fly, ou n8n Cloud) | Make.com, Zapier, Temporal (se for full-code) | Visual, 400+ integrações (Google, Drive, Calendar, WhatsApp), roda IA, self-host = dados seus |
| IA (LLM) | **Anthropic Claude API** (Sonnet p/ volume, Opus p/ peças complexas) | OpenAI GPT-4.x, Google Gemini | Qualidade de redação jurídica longa, no-training por padrão via API |
| Base de conhecimento (RAG) | **Vector DB** (Supabase pgvector ou Qdrant) + embeddings | Pinecone, Weaviate | Guarda doutrina/jurisprudência/teses com busca semântica e citação rastreável |
| Transcrição de reunião | **Recall.ai** (bot que entra no Meet) ou transcrição nativa Google Meet (Workspace Business) | Fireflies.ai, tl;dv, Whisper self-host | Recall.ai dá transcrição + diarização via API; Meet nativo é mais simples se já tem Workspace |
| Armazenamento/documentos | **Google Drive + Docs** (via API) | OneDrive, Notion | Você já vive no ecossistema Google; Docs permite peça editável |
| Agenda | **Google Calendar API** | Cal.com (self-host) para a página de agendamento pública | Cal.com resolve "escolher horário livre" sem expor sua agenda |
| CRM/pipeline de clientes | **Supabase (Postgres)** como fonte de verdade + view no Notion/Sheets | Pipedrive, HubSpot free | Barato, seu, RLS por cliente |
| Chatbot | **Widget no site** (React) + backend serverless chamando Claude + RAG | Chatwoot (self-host) + IA | Controle total sobre tom e conformidade OAB |
| Mensageria com cliente | **WhatsApp Cloud API** (Meta oficial) | E-mail (Resend/SendGrid), Telegram | Onde o cliente brasileiro está; API oficial evita ban |
| Prazos/tribunais | **APIs de tribunais / DJEN / PJe** + Codilo/Escavador/Judit.io (agregadores) | Scraping próprio (frágil) | Monitoramento de publicações e andamentos |
| Financeiro | **Google Sheets** (v1) → **Supabase + dashboard** (v2) | Conta Azul, QuickBooks | Comece simples; migre quando doer |
| Cobrança/pagamento | **Asaas** ou **Stripe/Mercado Pago** | Cora, InfinitePay | Asaas é forte para serviços jurídicos (boleto/PIX/cartão + régua de cobrança) |
| Assinatura de contrato | **Clicksign / D4Sign / Autentique** | DocuSign | Contrato de honorários e consentimento LGPD com validade jurídica |

---

## 3. Módulos em detalhe

### Módulo 1 — Captação de leads (inbound, compliant)

**Objetivo:** atrair quem já tem o problema, sem "caçar" cliente.

- **Fontes:** (a) SEO/conteúdo jurídico informativo; (b) as **calculadoras** do `algo-calc` como isca de valor (quem calcula um passivo já é lead quente); (c) indicações; (d) landing pages por área/dor.
- **Formulário de entrada:** curto (nome, contato, área do problema, 1 campo livre "descreva em uma frase"). Consentimento LGPD no rodapé.
- **De calculadora → lead:** ao final de um cálculo (ex: "seu passivo estimado é R$ X"), CTA sóbrio: *"Quer conversar com um advogado sobre isso?"* → cria lead no CRM com o contexto do cálculo anexado.
- **Fluxo:** formulário → webhook → n8n → cria registro no Supabase (`leads`) → notifica você → dispara mensagem de boas-vindas do chatbot.

**Técnicas:** captura de UTM/origem, lead scoring simples (área + urgência declarada), deduplicação por telefone/e-mail.

### Módulo 2 — Qualificação + chatbot por cliente

**Objetivo:** triagem automática em linguagem simples; chatbot que "conhece" o caso daquele cliente.

- **Chatbot de triagem (pré-cliente):** faz 4–6 perguntas (área, o que aconteceu, quando, documentos que tem, urgência). Nunca dá parecer jurídico nem promete resultado — apenas coleta e explica próximos passos. Produz um **resumo estruturado** do caso.
- **Chatbot dedicado ao cliente (pós-contratação):** cada cliente tem um "assistente" com contexto isolado — alimentado por (i) os dados do processo dele, (ii) andamentos, (iii) documentos da pasta dele no Drive. Responde "como está meu processo?" em linguagem simples, com **guardrails**: não inventa andamento, só reporta o que está na base; encaminha dúvidas jurídicas de mérito para você.
- **Arquitetura de isolamento:** cada cliente = um "namespace" no vector DB + filtro por `client_id`. O prompt do assistente injeta só os documentos daquele cliente (RAG filtrado). Zero vazamento entre clientes.

**Stack:** widget React → função serverless → Claude com *system prompt* rígido (tom, limites OAB) + contexto RAG do cliente. Registro de todas as conversas para auditoria.

**Guardrail crítico:** o chatbot **não** classifica juridicamente nem garante prazo/êxito. Frases de escape: *"Vou registrar isso e o Dr. Luccas confirma na conversa."*

### Módulo 3 — Agendamento automático (Google Calendar)

**Objetivo:** cliente marca reunião sozinho, sem ping-pong.

- **Página de agendamento:** **Cal.com** (self-host ou cloud) conectado ao seu Google Calendar → mostra só horários livres, respeita buffers, fuso, limites diários.
- **Fluxo:** chatbot qualificou → gera link do Cal.com (ou embute o seletor) → cliente escolhe → Cal.com cria evento no Calendar + gera **Google Meet** + envia convite → n8n recebe webhook e marca o lead como "reunião agendada".
- **Reagendamento/cancelamento:** o próprio Cal.com trata. Lembretes automáticos por WhatsApp/e-mail 24h e 1h antes.
- **"Marcar reunião que o cliente quiser" (pós):** o chatbot dedicado, ao detectar intenção de reunião, chama a API do Cal.com/Calendar e devolve horários — confirmação cria o evento automaticamente.

### Módulo 4 — Reunião inicial + transcrição

**Objetivo:** capturar a narrativa do cliente sem você digitar nada.

- **Gravação/transcrição:** duas rotas —
  1. **Recall.ai:** um bot entra no Meet, grava e devolve transcrição com *speaker diarization* via API (melhor para automação pura).
  2. **Google Meet nativo** (Workspace Business Standard+): ativa transcrição/gravação; arquivo cai no Drive; você processa via Drive API.
- **Consentimento (obrigatório):** aviso no início ("esta reunião será gravada e transcrita para elaborar sua documentação; você concorda?") + registro do aceite. Pode ser a primeira fala do bot ou um clique antes de entrar.
- **Saída:** transcrição em texto (com quem falou o quê e timestamps) → entregue à camada de orquestração para o pipeline do Módulo 5.

**Técnicas:** *diarization* para separar você do cliente; limpeza de ruído/muletas; marcação de trechos "fato" vs "pedido" vs "documento mencionado".

### Módulo 5 — Pipeline de IA: transcrição → Drive → petição + teses

Este é o coração. Sequência determinística, cada passo com validação:

```
transcrição
   │
   ├─(a) EXTRAÇÃO ESTRUTURADA
   │     Claude transforma a fala em JSON: partes, fatos (cronológicos),
   │     pedidos, documentos citados, valores, datas, área do direito.
   │
   ├─(b) CLASSIFICAÇÃO
   │     Define área/subárea, competência provável, rito → seleciona TEMPLATE
   │     de petição e o CONJUNTO de fontes do RAG a consultar.
   │
   ├─(c) MONTAGEM DA PASTA NO DRIVE
   │     n8n cria /Clientes/{Nome} - {Caso}/ com subpastas padronizadas
   │     (00_Contrato, 01_Documentos, 02_Transcrições, 03_Peças, 04_Prazos).
   │
   ├─(d) REDAÇÃO DOS FATOS
   │     Claude escreve a seção "DOS FATOS" completa, em ordem cronológica,
   │     fiel à narração, linguagem forense. SEM inventar fato não dito.
   │
   ├─(e) TESES (RAG obrigatório)
   │     Para cada pedido, Claude consulta o vector DB (doutrina/jurisprudência
   │     reais) e devolve LISTA DE TESES candidatas, cada uma com:
   │     fundamento + citação rastreável (fonte + link) + força estimada.
   │     NÃO redige o mérito ainda — entrega o cardápio para você escolher.
   │
   ├─(f) MONTAGEM DO RASCUNHO
   │     Gera Google Doc: cabeçalho + qualificação + DOS FATOS + [DO DIREITO:
   │     placeholders com as teses selecionáveis] + DOS PEDIDOS + valor da causa.
   │
   └─(g) AGENDA REVISÃO
         Cria evento no Calendar ("Revisão da inicial — {Cliente}") e avisa
         você e o cliente.
```

**Regras de ouro do pipeline:**
- **Fatos = fidelidade.** O modelo só narra o que o cliente disse; lacunas viram *[CONFIRMAR: ...]* em destaque, não invenção.
- **Teses = rastreabilidade.** Nenhuma citação sem fonte real do RAG. Se o RAG não tem base para a tese, ela é marcada *"sem respaldo na base — verificar manualmente"*.
- **Você sempre revisa** antes de qualquer protocolo. O sistema entrega rascunho, não peça final.
- **Idempotência:** reprocessar a mesma transcrição não duplica pastas/eventos.

**Saída para você:** um Google Doc pronto para revisar + um "briefing" (JSON legível) com fatos-chave, teses e pendências (*[CONFIRMAR]*).

### Módulo 6 — Base de conhecimento jurídico (RAG)

**Objetivo:** dar ao Claude memória jurídica **real e validada**, com citação rastreável.

- **O que indexar:** sua biblioteca de teses/modelos; doutrina que você tem direito de usar; ementas e acórdãos (fontes públicas: STF, STJ, TJs, DJEN); súmulas; enunciados; técnicas de retórica/argumentação; seus próprios cases anteriores (peças que deram certo).
- **Como (pipeline de ingestão):** documento → *chunking* semântico → embeddings → grava no vector DB com **metadados** (tribunal, data, área, tipo, fonte, URL). RAG sempre devolve o *chunk* + a fonte para citar.
- **Curadoria (não negociável):** jurisprudência entra por fonte oficial ou por você. Nada de "o modelo lembra de um acórdão" — se não está na base com fonte, não cita. Versionar (leis mudam, teses viram/caem).
- **Higiene anti-alucinação:** o prompt de teses recebe *"cite apenas o que estiver nos trechos fornecidos; se não houver base, diga que não há"*. Toda citação carrega o link da fonte para você conferir em 1 clique.
- **Atualização:** job periódico (n8n cron) puxando novas súmulas/temas repetitivos/repercussão geral e reindexando.

**Stack:** Supabase pgvector (começo) ou Qdrant (se escalar); embeddings via OpenAI/Voyage/Cohere; reranking opcional para precisão.

### Módulo 7 — Prazos processuais + notificação ao cliente

**Objetivo:** nunca perder prazo; manter cliente informado sem esforço.

- **Monitoramento de andamentos:** integrar com agregador (**Judit.io, Escavador, Codilo**) ou consumir **DJEN/PJe** — recebe publicações e movimentações dos seus processos por webhook/polling.
- **Cálculo de prazo:** ao detectar publicação, calcular o prazo (dias úteis, CPC art. 219; suspensões/recesso 20/12–20/01; feriados nacionais e locais). Aqui entra o **contador de prazos** (que também é uma das calculadoras do `algo-calc` — reaproveite o motor).
- **Agenda:** cria evento no Calendar com alertas escalonados (ex: D-5, D-2, D-dia) + tarefa na sua lista.
- **Notificação ao cliente (linguagem simples):** quando há andamento relevante, Claude **traduz o "juridiquês"** para uma mensagem clara ("O juiz pediu um documento; vou providenciar até dia X, não precisa fazer nada") e envia por WhatsApp. Guardrail: só traduz andamentos reais capturados; nada especulativo.
- **Fila de aprovação (opcional, recomendado no início):** notificações ao cliente passam por sua aprovação rápida (um toque no WhatsApp/Telegram) antes de sair, até você confiar no tom.

### Módulo 8 — Controle financeiro do escritório

**Objetivo:** faturamento, recebíveis e saúde financeira sem planilha manual caótica.

- **v1 (rápido):** Google Sheets estruturado — abas: Contratos, Honorários (fixo/êxito/hora), Recebíveis, Despesas, Fluxo de Caixa, DRE simples. n8n alimenta automaticamente ao fechar contrato e ao registrar pagamento.
- **v2 (robusto):** tabelas no Supabase + dashboard (Metabase/simple React) com MRR de honorários recorrentes, inadimplência, ticket médio, rentabilidade por caso.
- **Cobrança:** **Asaas** gera boleto/PIX/cartão, régua de cobrança automática (lembrete, vencimento, atraso), e webhook de "pago" atualiza o financeiro e libera etapas.
- **Contrato + honorários:** ao converter lead em cliente, n8n gera o contrato (template + dados) → assinatura via Clicksign/Autentique → arquiva no Drive (pasta 00_Contrato) → cria cobrança no Asaas.

---

## 4. Funções adicionais que você não listou (recomendo)

| Função | Valor | Esforço |
|--------|-------|---------|
| **CRM/pipeline visual** (Kanban de casos: lead → reunião → contrato → peticionado → em andamento → encerrado) | Visão única do escritório | Baixo (Supabase + view) |
| **Gerador de documentos recorrentes** (procuração, contrato, declaração de hipossuficiência) auto-preenchidos | Elimina retrabalho | Baixo |
| **Follow-up automático de leads frios** (informativo, dentro da OAB) | Recupera lead que sumiu | Baixo |
| **Base de "peças que deram certo"** realimentando o RAG | Suas vitórias viram ativo reutilizável | Médio |
| **Análise de documentos do cliente** (upload de PDF/contrato → IA extrai pontos-chave) | Acelera diagnóstico | Médio |
| **Painel de produtividade** (nº de casos/mês, tempo médio lead→peça, taxa de conversão) | Otimizar a esteira | Baixo |
| **Portal do cliente** (área logada: ver status, documentos, agendar, pagar) | Profissionaliza, reduz mensagens | Médio-alto |
| **Assistente de audiência** (prepara roteiro/perguntas a partir do caso + jurisprudência) | Alavanca seu diferencial argumentativo | Médio |
| **Detecção de conflito de interesse** ao entrar novo cliente (cruza com base existente) | Compliance | Baixo |
| **Backup e trilha de auditoria** de tudo (LGPD/OAB) | Proteção jurídica sua | Baixo |

---

## 5. Modelo de dados (núcleo, simplificado)

```
leads(id, nome, contato, origem, area, resumo, score, status, created_at)
clients(id, lead_id, nome, cpf_cnpj, contato, consentimento_lgpd, created_at)
cases(id, client_id, area, numero_processo, tribunal, rito, status, valor_causa)
meetings(id, case_id, tipo, data, meet_url, transcricao_url, status)
documents(id, case_id, tipo, drive_url, origem, created_at)
petitions(id, case_id, tipo, doc_url, status[rascunho|revisao|protocolada], versao)
theses(id, petition_id, texto, fundamento, fonte_url, forca, aceita)
deadlines(id, case_id, descricao, publicacao_em, prazo_fatal, status, calendar_event_id)
notifications(id, client_id, canal, texto, status, aprovada_por, enviada_em)
finances(id, case_id, tipo[fixo|exito|hora], valor, vencimento, pago_em, cobranca_id)
kb_chunks(id, texto, embedding, tribunal, area, tipo, fonte_url, data, versao)  -- vector DB
audit_log(id, entidade, entidade_id, acao, ator, payload, created_at)
```

RLS por `client_id` no Supabase garante isolamento. `audit_log` é apêndice-only.

---

## 6. Roadmap de construção (por fases, de menor a maior risco)

### Fase 0 — Fundação (1–2 semanas)
- Supabase (schema + RLS), n8n rodando, Google Workspace/APIs (Drive, Calendar, Meet) conectadas.
- CRM mínimo (tabela `leads`/`clients` + Kanban) e página de agendamento (Cal.com) funcionando.
- **Entregável:** lead entra → você agenda → reunião no Meet. Sem IA ainda.

### Fase 1 — Transcrição → rascunho (2–3 semanas) — **o maior ganho**
- Transcrição (Recall.ai ou Meet nativo) → pipeline (a)(b)(c)(d) do Módulo 5.
- Criação de pasta no Drive + rascunho de **DOS FATOS** + briefing estruturado.
- **Entregável:** ao fim da reunião, uma pasta organizada e um rascunho de fatos aparecem sozinhos.

### Fase 2 — RAG + teses (2–4 semanas)
- Ingestão da sua biblioteca + fontes públicas no vector DB.
- Passo (e)(f): geração de **lista de teses com citação rastreável** e montagem do Doc completo.
- **Entregável:** rascunho de inicial com fatos + cardápio de teses fundamentadas para você escolher.

### Fase 3 — Chatbot + notificações (2–3 semanas)
- Chatbot de triagem (site) e chatbot dedicado por cliente (RAG isolado).
- Módulo 7: monitoramento de prazos + tradução de andamentos + notificação (com fila de aprovação).
- **Entregável:** cliente pergunta status e recebe updates claros; você não perde prazo.

### Fase 4 — Financeiro + contratos + cobrança (1–2 semanas)
- Geração/assinatura de contrato, Asaas, planilha/dashboard financeiro automatizados.
- **Entregável:** do "sim" do cliente ao boleto pago, tudo rastreado.

### Fase 5 — Portal do cliente + extras (contínuo)
- Área logada, análise de documentos, assistente de audiência, painéis.

> Priorize **Fase 1** — é onde 1 pessoa ganha mais alavancagem (elimina o trabalho braçal de transformar conversa em documento organizado).

---

## 7. Custos estimados (ordem de grandeza, BRL/mês)

| Item | Início (baixo volume) | Escala (dezenas de casos/mês) |
|------|----------------------|-------------------------------|
| Google Workspace Business | ~R$ 35/usuário | ~R$ 35 |
| n8n (self-host Railway/Fly) | ~R$ 25–50 | ~R$ 50–100 |
| Supabase | R$ 0 (free) | ~R$ 125 (Pro) |
| Claude API | ~R$ 50–200 (por uso) | ~R$ 300–800 |
| Embeddings + vector DB | ~R$ 0–50 | ~R$ 100–200 |
| Transcrição (Recall.ai) | ~R$ 0–150 | ~R$ 200–500 |
| WhatsApp Cloud API | ~R$ 0–50 | conversas pagas por volume |
| Cal.com / Asaas / Clicksign | free tiers | ~R$ 50–150 somados |
| **Total aproximado** | **~R$ 200–500/mês** | **~R$ 1.000–2.000/mês** |

Custo domina por uso de IA/transcrição — escala junto com a receita, não é custo fixo pesado.

---

## 8. Riscos e mitigações

| Risco | Mitigação |
|-------|-----------|
| Alucinação de jurisprudência | RAG com citação obrigatória + revisão humana + marcação "sem respaldo" |
| Violação de sigilo/LGPD | Provedores no-training, criptografia, DPA, RLS, retenção definida, consentimento |
| Infração à publicidade OAB | Captação só inbound/informativa; chatbot não vende nem promete; marcas separadas |
| Dependência de fornecedor (lock-in) | Supabase self-hostável; LLM atrás de interface `LLMProvider`; Recall.ai desacopla do Google |
| Erro de prazo por falha de integração | Alertas redundantes (Calendar + tarefa + você) + conferência manual dos prazos fatais |
| Transcrição ruim → fatos errados | Diarization + etapa *[CONFIRMAR]* + você valida fatos com o cliente na revisão |
| Vazamento entre clientes no RAG | Namespacing/filtro por `client_id`, testes de isolamento |

---

## 9. Decisões (resolvidas) — respostas + recomendação padrão

Cada decisão abaixo já vem **fechada** com uma escolha padrão, para a sessão futura não travar. As alternativas ficam registradas caso você mude de ideia.

### 9.1 Transcrição → **Recall.ai** (padrão)
Como você não sabe qual plano de Workspace tem e vai construir em código, o **Recall.ai** é a escolha mais portável: um bot entra no Meet, grava e devolve transcrição + diarização por **API**, independente do seu plano Google. Funciona igual em Meet, Zoom ou Teams (não te prende ao Google).
*Alternativa:* transcrição nativa do Meet (só se confirmar Workspace Business Standard+) — mais barata, porém acoplada ao Google e menos controlável via código.

### 9.2 Volume → **projetar para "sonho", operar no "real"**
Realidade ano 1: **1–3 casos/mês**. Sonho: **10+/mês**. Implicação de arquitetura: o desenho já é escalável (serverless + fila de jobs), mas **não gaste esforço/otimização prematura** — no início tudo roda em free tiers e processamento sob demanda. O custo acompanha o volume; nada de infra fixa cara. A esteira só precisa não ser um gargalo quando o volume subir — e não é, porque cada caso é um job independente.

### 9.3 Áreas iniciais → **Civil (imobiliário, societário, sucessório), Penal, Trabalhista**
Ordem sugerida de construção de *templates* de petição e base de teses:
1. **Trabalhista** — petições mais padronizáveis (reclamatória), motor de cálculo já existe no `algo-calc` (reflexos, rescisão), ótimo para validar a esteira ponta-a-ponta.
2. **Cível (imobiliário/sucessório/societário)** — alto valor, boa reutilização de cláusulas e teses.
3. **Penal** — deixar por último: peças mais artesanais e sensíveis, menos padronizáveis, maior risco em automação. Comece por defesas/petições mais estruturadas.
Como você ainda não se especializou, a base de teses (Módulo 6) vira também **ferramenta de estudo** — cada caso enriquece seu acervo por área.

### 9.4 Abordagem → **código (núcleo em code-first)**
Como você vai usar o Devin para construir, o núcleo é **código** (não no-code). Isso muda a stack de orquestração:
- **Orquestração:** em vez de n8n visual, um **worker em código** — TypeScript (Node) ou Python — com uma **fila de jobs** (ex: `pg-boss`/BullMQ sobre Postgres/Redis, ou Cloud Tasks). Cada etapa do pipeline (Módulo 5) é um job idempotente. Mais controle, testável, versionável em git.
- **n8n vira opcional:** útil só para "colar" integrações simples/no-code que não valem código (ex: um lembrete). O coração é código.
- **Camada de LLM abstraída** atrás de uma interface (`LLMProvider`) para trocar Claude/OpenAI sem reescrever o pipeline.
- **Monorepo** sugerido (ex: `apps/worker`, `apps/api`, `apps/web`, `packages/core`, `packages/rag`).

### 9.5 Por onde começar → **Fase 1 (transcrição → rascunho)** (recomendação)
Você não sabe — então recomendo travar em **Fase 1**. É o maior ganho de alavancagem para 1 pessoa: elimina o trabalho braçal de virar conversa em documento organizado, e valida o elo técnico mais difícil (transcrição→IA→Drive→Doc) antes de investir no resto. Fases 0 e 1 juntas já entregam um MVP útil só para você.

### 9.6 Fontes do RAG → **começar com fontes públicas; biblioteca cresce com o uso**
Você tem pouquíssima biblioteca. Então a base parte de **fontes públicas** (STF, STJ, TJs, DJEN, súmulas, enunciados, legislação) + curadoria manual mínima. **Cada peça que você produzir e validar realimenta o RAG** — em 6–12 meses seu acervo próprio vira o diferencial. Regra anti-alucinação continua: nada de citar o que não está indexado com fonte.

---

## 10. Prompt de arranque (para a sessão futura do Devin)

Cole o bloco abaixo no início de uma **nova sessão agnóstica** do Devin, junto com este documento anexado. Ele dá ao Devin o contexto mínimo para começar a construir sem reler tudo.

> **Contexto:** Sou advogado solo (áreas: Civil — imobiliário/societário/sucessório —, Penal e Trabalhista). Quero construir, **em código**, um ecossistema de automação do escritório. A arquitetura completa está no arquivo anexo `ecossistema-juridico-blueprint.md` — leia-o inteiro antes de começar.
>
> **Decisões já tomadas** (seção 9 do doc): transcrição via **Recall.ai**; núcleo **code-first** (worker em TypeScript ou Python + fila de jobs idempotentes, LLM atrás de interface `LLMProvider`, monorepo); LLM = **Claude API**; dados no **Supabase (Postgres + pgvector)**; começar pela **Fase 1 (transcrição → rascunho de petição)**; RAG inicia com **fontes públicas** e cresce com o uso.
>
> **Guardrails inegociáveis** (seção 0 do doc): (1) toda peça é rascunho revisável por mim, nunca protocolo automático; (2) toda tese/citação vem do RAG com fonte rastreável — sem alucinação; (3) captação só inbound/informativa (regras da OAB); (4) sigilo/LGPD — provedores no-training, isolamento por `client_id`, consentimento antes de gravar reunião.
>
> **Tarefa desta sessão:** implementar a **Fase 1**. Comece propondo (a) a estrutura do monorepo, (b) o schema inicial no Supabase (tabelas da seção 5 relevantes: `cases`, `meetings`, `documents`, `petitions`, `theses`), (c) o pipeline do Módulo 5 passos (a)→(d) [extração estruturada → classificação → criação da pasta no Drive → redação de "DOS FATOS"], como jobs idempotentes. Peça as credenciais que faltarem (Recall.ai, Anthropic, Google Drive/Calendar, Supabase) e me proponha um plano antes de codar.

*Este é um projeto de arquitetura para uso pessoal. Não implementa nada ainda — é o mapa. A cada fase, construímos e validamos um incremento funcional antes de seguir. As decisões da seção 9 estão fechadas em recomendações padrão, mas continuam ajustáveis.*
