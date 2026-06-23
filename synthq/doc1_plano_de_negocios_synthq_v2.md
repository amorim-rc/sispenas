# PLANO DE NEGÓCIOS INTERNO — SYNTHQ
## Documento Estratégico Confidencial dos Fundadores

**Versão:** 3.0 | **Data:** Junho/2026
**Classificação:** Uso interno — Não compartilhar externamente sem autorização
**Autores:** Luccas Cavicchioli (CEO) + Leandro Moraes (CTO)

---

# PARTE I — FUNDAMENTOS ESTRATÉGICOS

## 1. Tese de Investimento (Investment Thesis)

### 1.1. A Tese em Uma Frase

> A SynthQ captura valor na camada de compilação lógica da computação quântica — o único ponto da stack onde otimização gera economia financeira direta e mensurável para qualquer cliente, em qualquer hardware, sem vendor lock-in.

### 1.2. Por Que Agora (Timing)

A computação quântica vive em junho/2026 um momento de inflexão:

**Sinais de mercado (últimos 18 meses):**
- IBM anunciou o Heron (133 qubits, error rates 10x melhores que Eagle) e roadmap para 100k qubits em 2033
- Microsoft declarou "Level 2 Quantum" alcançado com processador topológico (abril/2025)
- Google demonstrou vantagem quântica em simulação de materiais (Nature, 2025)
- Quantinuum atingiu 99.8% fidelidade de 2-qubit gates com íons aprisionados
- AWS Braket, Azure Quantum e IBM Quantum reportam crescimento de 3x em uso comercial (2024→2025)
- Mercado de software quântico projeta CAGR de 45% (McKinsey Quantum Technology Monitor 2025)

**O que isso significa para a SynthQ:**
1. **Demanda por QPU cresce** → custo de execução se torna dor real (não apenas teórica)
2. **Transição para FTQC começa** → portas T se tornam o gargalo econômico dominante
3. **Nenhum player endereça T-count como produto** → janela de mercado aberta
4. **Capital fluindo para quantum** → investidores buscam oportunidades de software (margens maiores que hardware)

**Janela de oportunidade estimada:** 18-36 meses antes que grandes players (IBM, Google) internalizem soluções de otimização de T-count como feature nativa. Tempo suficiente para:
- Construir produto + base de clientes
- Publicar papers que estabeleçam autoridade científica
- Depositar patentes defensivas
- Posicionar-se como aquisição estratégica ou parceiro de integração

### 1.3. Por Que Nós

| Vantagem Competitiva | Descrição | Durabilidade |
|---------------------|-----------|--------------|
| Expertise científica proprietária | CTO doutorando em algoritmos quânticos com domínio de ZX-Calculus | Alta (5+ anos de pesquisa não replicável rapidamente) |
| Agnosticismo de hardware | Opera na camada lógica pura, complementar a TODOS os provedores | Estrutural (arquitetura de produto) |
| Custo de operação ultra-baixo | Brasil + equipe enxuta + SaaS puro | 3-5 anos (até escala global) |
| First-mover em T-count como produto | Ninguém vende otimização de T-count standalone | 18-36 meses (janela) |
| Acesso acadêmico privilegiado | Conexão direta com grupos de pesquisa UFRN/USP | 5+ anos (rede pessoal) |

### 1.4. Riscos Existenciais e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| IBM/Google internaliza otimização T-count | Média (30%) | Alto | Ser adquirido ou pivotar para consultoria especializada |
| Computação quântica não escala (quantum winter) | Baixa (10%) | Fatal | Diversificar para otimização de circuitos clássicos (EDA) ou consultoria |
| Motor não escala para circuitos industriais (>50 qubits) | Média (25%) | Alto | Focar em nichos (VQE, QAOA) onde circuitos são estruturados |
| CTO abandona projeto | Baixa (15%) | Alto | Documentação rigorosa + IP assignment contratual desde dia 1 |
| Falta de clientes dispostos a pagar | Média (20%) | Alto | Validar com LOIs antes de investir pesado em produto |

---

## 2. Proposta de Valor Detalhada

### 2.1. O Problema (Formulação Rigorosa)

Em computação quântica tolerante a falhas (FTQC), circuitos são decompostos no gate set universal **Clifford+T**:
- **Portas Clifford** (H, S, CNOT): implementáveis transversalmente em códigos de correção de erro. Custo computacional: ~0 (comparativo).
- **Portas T** (porta π/8): NÃO implementáveis transversalmente. Requerem **Magic State Distillation** (MSD).

**O custo da Magic State Distillation:**
- Cada porta T requer destilação de um "magic state" |A⟩ = T|+⟩
- A destilação consome ~15-50 qubits físicos por magic state (dependendo do código)
- Em hardware com error rates atuais (~10⁻³), são necessárias múltiplas rodadas de destilação
- Estimativas (Litinski, 2019): um computador quântico fault-tolerant gastaria **90% dos qubits físicos** apenas em fábricas de magic states
- Em cloud quantum (pricing por shot/tempo): custo é DIRETAMENTE proporcional ao T-count + T-depth

**Exemplo concreto de impacto econômico:**
- Circuito VQE para molécula de LiH (exemplo industrial simples): ~2000 portas T após compilação
- Se cada porta T custa ~$0.01 em cloud QPU (estimativa conservadora baseada em IBM pricing 2025)
- Custo por execução: ~$20/shot
- Algoritmo variacional requer ~10⁴-10⁶ shots para convergir
- Custo total: $200k - $20M por problema
- **Se SynthQ reduz T-count em 40%:** economia de $80k - $8M por problema

### 2.2. A Solução (Formulação Técnica)

A SynthQ oferece um **compilador de otimização lógica** que:

1. **Recebe** circuito quântico em formato padrão (OpenQASM 3.0, Qiskit IR)
2. **Converte** para representação de grafo ZX (tensor network no formalismo ZX-Calculus)
3. **Aplica** transformações matematicamente exatas (preservam semântica computacional):
   - Simplificação por regras categóricas (spider fusion, bialgebra, pivot)
   - Otimização de phase gadgets (fusão de rotações)
   - Redução de Clifford interior
   - Phase-folding e T-merging
4. **Extrai** circuito otimizado de volta para OpenQASM
5. **Reporta** métricas de ganho (T-count, T-depth, gate count total, profundidade)

**Propriedades críticas do produto:**
- **Corretude garantida**: transformações preservam equivalência unitária (provável matematicamente)
- **Agnóstico de hardware**: opera ANTES do mapeamento físico
- **Complementar**: não substitui transpiladores existentes — os MELHORA
- **Determinístico**: mesmo input → mesmo output (reprodutível)

### 2.3. Proposta de Valor por Segmento

| Segmento | Dor Principal | Proposta SynthQ | Métrica de Valor |
|----------|--------------|-----------------|-----------------|
| Centros de inovação corporativos | "Estourei o budget de QPU e não consigo rodar meu PoC" | Reduzir custo de execução em 30-70% | $/shot economizado |
| Startups quantum | "Meus circuitos são muito profundos para hardware atual" | Reduzir profundidade (depth) para caber em QPU disponível | # qubits/depth viabilizados |
| Plataformas QaaS (AWS/IBM/Azure) | "Clientes reclamam de custo e churn" | White-label: oferecer otimização como feature da plataforma | Redução de churn / aumento de NPS |
| Pesquisadores | "Perco semanas otimizando circuitos na mão" | Automação de otimização | Horas economizadas |

---

## 3. Análise de Mercado Aprofundada

### 3.1. Dimensionamento (TAM/SAM/SOM)

**TAM — Total Addressable Market:**
- Mercado global de computação quântica (hardware + software + serviços): $65B projetado para 2030 (BCG, 2024)
- Software quântico (subcategoria): $8.6B projetado para 2030 (McKinsey)
- **TAM relevante (middleware/compilers/tools): ~$2B até 2030**

**SAM — Serviceable Available Market:**
- Organizações com budget ativo de quantum computing: ~500-800 globalmente (2026)
- Destes, ~200-300 com circuitos complexos o suficiente para otimização (T-count relevante)
- Ticket médio estimado (SaaS Enterprise): $30k-100k/ano
- **SAM: ~$200-400M até 2028**

**SOM — Serviceable Obtainable Market (primeiros 12 meses):**
- Mercado brasileiro acessível: 10-20 centros de inovação com programas quantum
- Conversão esperada (conservador): 3-5 clientes
- Ticket médio PoC: R$ 50k-80k
- **SOM 12 meses: R$ 150k-400k**

### 3.2. Segmentação de Clientes

**Tier 1 — Early Adopters (primeiros 12 meses):**
| Empresa | Setor | Programa Quantum | Potencial |
|---------|-------|-----------------|-----------|
| Petrobras (CENPES) | Energia | Quantum para otimização de reservatórios | Alto |
| Itaú Unibanco (IQ Lab) | Finanças | Quantum para precificação de derivativos | Alto |
| Vale | Mineração | Quantum para simulação de materiais | Médio |
| WEG | Indústria | Quantum para otimização logística | Médio |
| Banco do Brasil (LIC) | Finanças | Lab de inovação com foco quantum | Médio |
| EDP Brasil | Energia | Otimização de redes inteligentes | Médio |
| Embraer | Aeroespacial | Simulação de fluidos quântica | Alto |

**Tier 2 — Growth (meses 12-24):**
- Startups quantum globais (IonQ ecosystem, IBM partners)
- Institutos de pesquisa com funding (Fraunhofer, RIKEN, NIST)
- Consultorias com prática quantum (Accenture, McKinsey Quantum Black)

**Tier 3 — Scale (meses 24+):**
- Plataformas QaaS (AWS Braket, Azure Quantum, IBM Quantum)
- Fabricantes de hardware (como integração de compilador)
- Consórcio Cinquanta PB (governo brasileiro)

### 3.3. Análise Competitiva Detalhada

#### Mapa competitivo:

```
                    FOCO EM T-COUNT
                         ↑
                         |
                   SynthQ ★
                         |
          BQSKit •       |        • PyZX (acadêmico)
                         |
    ─────────────────────┼─────────────────────── AGNÓSTICO
    VENDOR LOCK-IN       |                         DE HARDWARE
                         |
       pytket •          |
                         |
    Qiskit Transpiler •  |      • Staq
                         |
                         ↓
                   FOCO EM MAPEAMENTO FÍSICO
```

#### Análise detalhada dos competidores:

**1. Qiskit Transpiler (IBM)**
- Pontos fortes: ecossistema massivo, comunidade, integração nativa com IBM QPUs
- Fraquezas: otimiza para hardware IBM (não T-count puro), level 3 é lento, não faz ZX nativo
- Posição: transpilador generalista, não competidor direto
- Oportunidade para SynthQ: ser plugin "pré-Qiskit" — otimiza ANTES do transpiler rodar

**2. pytket / tket (Quantinuum)**
- Pontos fortes: otimização sofisticada, bons resultados em benchmarks, ZX-Calculus parcial
- Fraquezas: closed-source core, otimizado para hardware Quantinuum (íons), pricing opaco
- Posição: competidor mais próximo em capacidade técnica
- Oportunidade: SynthQ é agnóstico + transparente em métricas + modelo SaaS simples

**3. BQSKit (Berkeley Lab)**
- Pontos fortes: síntese numérica de qualidade, academic backing
- Fraquezas: runtime exponencial para circuitos >10 qubits, sem modelo comercial, equipe acadêmica
- Posição: ferramenta de pesquisa, não produto
- Oportunidade: SynthQ escala onde BQSKit não escala

**4. PyZX (Oxford / Aleks Kissinger)**
- Pontos fortes: implementação de referência de ZX-Calculus, open-source, bem mantida
- Fraquezas: biblioteca de pesquisa (não produto), sem API/SaaS, sem suporte comercial
- Posição: building block (a SynthQ USA PyZX como componente)
- Relação: parceiro/dependência técnica, não competidor

**5. Classiq (Israel, $150M+ raised)**
- Pontos fortes: funding massivo, equipe grande, síntese high-level
- Fraquezas: foco em DESIGN de circuitos (não otimização de T-count), não opera na camada lógica pura
- Posição: upstream (gera circuitos) — SynthQ seria downstream (otimiza circuitos gerados)
- Oportunidade: integração/parceria (Classiq gera, SynthQ otimiza)

### 3.4. Barreiras de Entrada e Moat (Fosso Competitivo)

| Barreira | Força | Tempo para replicar |
|----------|-------|-------------------|
| Expertise em ZX-Calculus aplicado | Alta | 3-5 anos (doutorado) |
| Heurísticas proprietárias de reescrita | Média-Alta | 1-2 anos com equipe sênior |
| Base de benchmarks validados | Média | 6-12 meses |
| Patente(s) depositada(s) | Alta | 20 anos de proteção |
| Relações com clientes (switching cost) | Média | 12-24 meses |
| Publicações científicas (autoridade) | Alta | 2-3 anos |
| Dados de uso (quais circuitos clientes otimizam) | Média-Alta | Crescente com tempo |

**Moat principal:** A combinação de (1) expertise científica profunda + (2) execução como produto SaaS + (3) agnosticismo de hardware cria uma posição única que nenhum competidor ocupa hoje. IBM/Google poderiam construir internamente, mas não vendem para clientes de concorrentes. Quantinuum (pytket) tem vendor lock-in. Acadêmicos (PyZX, BQSKit) não têm modelo comercial.

---

## 4. Modelo de Negócios e Monetização

### 4.1. Evolução do Modelo (3 Fases)

#### Fase 1: Projetos Empacotados (Pré-incubação — Meses 1-12)

| Aspecto | Detalhe |
|---------|---------|
| Modelo | Venda de projeto/PoC com deliverable fixo |
| Produto | "Envie seus 3-5 circuitos mais críticos, devolvo otimizados + relatório de economia" |
| Pricing | R$ 30k-80k por projeto (3-5 circuitos + relatório) |
| Ciclo de venda | 30-60 dias (decisão de gerente de inovação, não de C-level) |
| Entrega | Circuitos otimizados em OpenQASM + relatório PDF com métricas |
| Meta | 3-5 projetos no período |
| Receita esperada | R$ 150k-400k |
| Margem bruta | >80% (custo é tempo de CTO + infra cloud) |
| Racional | Validar demanda, gerar case studies, financiar desenvolvimento |

**Por que PoC primeiro (e não SaaS direto):**
1. Não temos produto self-service ainda (motor precisa de ajuste manual para circuitos complexos)
2. Alto-touch com cliente gera insights sobre necessidades reais
3. Case studies de PoC são melhor material de venda para Fase 2
4. Revenue desde o mês 4-6 (vs. 12+ meses para SaaS)
5. Valida willingness-to-pay antes de investir em plataforma

#### Fase 2: SaaS Developer API (Incubação — Meses 13-36)

| Aspecto | Detalhe |
|---------|---------|
| Modelo | Assinatura mensal + pay-per-use |
| Produto | API REST: POST /optimize, retorna circuito otimizado em <5s |
| Tiers | Developer ($99/mês, 100 otimizações), Startup ($499/mês, 1000), Enterprise ($2.5k+/mês, ilimitado + SLA) |
| Ciclo de venda | Self-service (Dev/Startup), 60-90 dias (Enterprise) |
| Meta (mês 24) | 50-100 assinantes, 5-10 Enterprise |
| MRR esperado (mês 24) | $50k-150k/mês |
| Margem bruta | >90% |
| Racional | Escala, recorrência, valuation de SaaS |

#### Fase 3: Licenciamento B2B + White-Label (Escala — Meses 36+)

| Aspecto | Detalhe |
|---------|---------|
| Modelo | Licença enterprise + royalties por uso |
| Produto | SDK embeddable para plataformas QaaS |
| Clientes | AWS Braket, Azure Quantum, IBM Quantum, Rigetti QCS |
| Pricing | Licença anual $500k-2M + royalty por circuito ($0.01-0.10/otimização) |
| Racional | Captura de valor na cadeia, posição de infraestrutura |

### 4.2. Unit Economics (Fase 2 — Estado Estacionário)

| Métrica | Valor |
|---------|-------|
| ARPU (Average Revenue Per User) | $200-500/mês |
| CAC (Customer Acquisition Cost) | $500-2000 (inbound/content-led) |
| LTV (Lifetime Value) | $4.8k-12k (24 meses avg retention) |
| LTV/CAC | 6-10x (excelente) |
| Gross Margin | >90% |
| Payback Period | 2-4 meses |
| Net Revenue Retention | >120% (upsell de tier) |

### 4.3. Projeção de Receita (3 Anos)

| Período | Modelo | Clientes | Receita (R$) | Acumulado |
|---------|--------|----------|-------------|-----------|
| M1-M6 | Bootstrapping + Dev | 0 | 0 | 0 |
| M7-M9 | PoC #1-#2 | 2 | 100k | 100k |
| M10-M12 | PoC #3-#5 | 5 | 200k | 300k |
| M13-M18 | PoC + SaaS beta | 8 + 20 API | 350k | 650k |
| M19-M24 | SaaS growth | 50 API + 5 Enterprise | 600k | 1.25M |
| M25-M36 | SaaS + Licenciamento | 150 API + 15 Ent + 1 Lic | 2.5M | 3.75M |

---

## 5. Estratégia Go-To-Market

### 5.1. Posicionamento

**Tagline:** "Cut your quantum bill in half. Same circuit, fewer T-gates, any hardware."

**Mensagem por audiência:**
| Audiência | Mensagem Central | Canal |
|-----------|-----------------|-------|
| C-Level / VP Innovation | "Reduz custo de QPU em 30-70% sem mudar código" | LinkedIn + eventos C-level |
| Engenheiro quantum | "API simples: POST seu OpenQASM, receba otimizado em 2s" | Dev community + GitHub |
| Pesquisador | "Reproducible ZX-based optimization with published benchmarks" | arXiv + conferências |
| Investidor | "First standalone T-count optimizer, $8.6B TAM, >90% margins" | Deck + warm intros |

### 5.2. Flywheel (Ciclo Virtuoso)

```
Publicação científica → Credibilidade acadêmica
        ↓
Benchmark público → Developers experimentam
        ↓
Casos de uso reais → Case studies
        ↓
Case studies → Clientes enterprise
        ↓
Receita → Investimento em P&D
        ↓
Mais pesquisa → Mais publicações
        ↓
(VOLTA AO INÍCIO)
```

### 5.3. Canais de Aquisição (Priorizado)

| Canal | Custo | Tempo p/ resultado | Qualidade |
|-------|-------|-------------------|-----------|
| 1. Rede pessoal (academia → corporativo) | Zero | Imediato | Alta |
| 2. Publicações + arXiv | Baixo (tempo) | 3-6 meses | Muito alta |
| 3. Benchmark público (GitHub) | Baixo | 1-3 meses | Alta |
| 4. Eventos/conferências quantum | Médio ($2-5k/evento) | 1-3 meses | Alta |
| 5. Content marketing (blog técnico) | Baixo (tempo) | 6-12 meses | Média-alta |
| 6. Partnerships (IBM Quantum Network) | Baixo | 3-6 meses | Alta |
| 7. Cold outreach para centros de inovação | Baixo | 1-2 meses | Média |

### 5.4. Estratégia de Validação Pré-Produto

**"Free Benchmark" Strategy:**
1. Identificar 10-15 centros de inovação com programas quantum ativos
2. Oferecer: "Envie 1 circuito real, otimizo grátis, apresento relatório de economia"
3. Converter demonstração gratuita em PoC pago (upsell natural)
4. Usar resultados como case study para próximos clientes

**Meta:** 5 benchmarks gratuitos → 3 conversões em PoC pago (60% conversion rate)

---

## 6. Equipe e Organização

### 6.1. Fundadores

**CEO — Luccas de Amorim Rêgo Cavicchioli**
| Aspecto | Detalhe |
|---------|---------|
| Formação | Filosofia (UFPE) + Direito (em curso) |
| Experiência | 3 anos no ecossistema de tecnologia |
| Papel | Estratégia, negócios, captação, GTM, jurídico/IP |
| Dedicação | 40h/semana |
| Contribuição única | Pensamento analítico + visão estratégica + capacidade de articulação |

**CTO — Leandro Moraes**
| Aspecto | Detalhe |
|---------|---------|
| Formação | Física (UFRN) + Mestrado Física + Doutorado Física (último ano, UFRN c/ período USP) |
| Especialização | Algoritmos quânticos, ZX-Calculus, síntese de circuitos |
| Papel | P&D, arquitetura técnica, motor algorítmico, publicações |
| Dedicação | 30-40h/semana |
| Contribuição única | Conhecimento científico profundo + rede acadêmica + capacidade de publicação |

### 6.2. Complementaridade dos Fundadores

```
CEO (Luccas)                    CTO (Leandro)
──────────────                  ──────────────
Negócios / GTM     ←→     Tecnologia / Ciência
Captação           ←→     Desenvolvimento
Clientes           ←→     Produto
Jurídico/IP        ←→     Arquitetura
Comunicação        ←→     Publicações
Operações          ←→     P&D
Estratégia macro   ←→     Execução técnica
```

**O que falta e como suprir:**
| Gap | Quando suprir | Como |
|-----|--------------|------|
| Engenheiro de software sênior (Rust/Python) | Mês 6-9 | Stock options + bolsa FAPERN |
| Designer UX (dashboard/docs) | Mês 9-12 | Freelancer |
| DevRel / Community | Mês 12-18 | Contratação |
| Sales (Enterprise) | Mês 18-24 | Contratação |

### 6.3. Governança e Acordos

**Itens a formalizar ANTES da inscrição ou nos primeiros meses:**
1. **Acordo de Sócios (Memorando de Entendimentos):** Divisão de equity, vesting, dedicação, saída
2. **IP Assignment:** Todo código/pesquisa produzido pelos sócios pertence à SynthQ
3. **Vesting:** 4 anos com cliff de 1 ano para ambos (padrão)
4. **Equity split:** 50/50
5. **Tipo societário:** LTDA inicialmente → S/A para captação futura

---

## 7. Planejamento Financeiro

### 7.1. Investimento Necessário (Pré-Seed)

| Categoria | Valor Total (12 meses) | Mensal |
|-----------|----------------------|--------|
| Infraestrutura cloud (AWS/GCP) | R$ 24.000 | R$ 2.000 |
| Taxa Metrópole Parque | R$ 3.912 | R$ 326 |
| Ferramentas e licenças | R$ 6.000 | R$ 500 |
| Viagens e prospecção comercial | R$ 18.000 | R$ 1.500 |
| Registro PI (marca + patente) | R$ 8.000 | R$ 667 (amortizado) |
| Marketing e eventos | R$ 9.600 | R$ 800 |
| Bolsa pesquisador júnior (a partir M6) | R$ 21.000 | R$ 3.000 (7 meses) |
| Contabilidade + jurídico | R$ 6.000 | R$ 500 |
| Reserva de contingência | R$ 15.000 | — |
| **TOTAL** | **R$ 111.512** | **~R$ 9.300/mês** |

**Fontes de financiamento:**
| Fonte | Valor | Probabilidade | Timeline |
|-------|-------|---------------|----------|
| Centelha 3 RN (FAPERN) | Até R$ 100k | 40% | 3-6 meses |
| FINEP/Tecnova III | Até R$ 300k | 25% | 6-12 meses |
| Receita de PoCs (a partir M6) | R$ 150-400k | 60% | 6-12 meses |
| Recursos próprios (bootstrap) | R$ 30-50k | 100% | Imediato |
| PIPE/FAPESP | Até R$ 250k | 20% | 6-9 meses |

### 7.2. Projeção de Fluxo de Caixa (12 Meses)

| Mês | Receita | Custos | Fluxo Mensal | Acumulado |
|-----|---------|--------|-------------|-----------|
| M1 | 0 | -8.000 | -8.000 | -8.000 |
| M2 | 0 | -8.000 | -8.000 | -16.000 |
| M3 | 0 | -8.000 | -8.000 | -24.000 |
| M4 | 0 | -9.000 | -9.000 | -33.000 |
| M5 | 0 | -9.000 | -9.000 | -42.000 |
| M6 | +50.000 (PoC #1) | -12.000 | +38.000 | -4.000 |
| M7 | 0 | -12.000 | -12.000 | -16.000 |
| M8 | +60.000 (PoC #2) | -12.000 | +48.000 | +32.000 |
| M9 | 0 | -12.000 | -12.000 | +20.000 |
| M10 | +70.000 (PoC #3) | -12.000 | +58.000 | +78.000 |
| M11 | +50.000 (PoC #4) | -12.000 | +38.000 | +116.000 |
| M12 | +70.000 (PoC #5) | -12.000 | +58.000 | +174.000 |

**Breakeven: Mês 6** (com primeiro PoC)
**Acumulado 12 meses (cenário base): +R$ 174k**

### 7.3. Cenários

| Cenário | Receita 12m | Condições |
|---------|-------------|-----------|
| Pessimista | R$ 100k | 2 PoCs, delays de 2 meses cada |
| Base | R$ 300k | 5 PoCs conforme planejado |
| Otimista | R$ 500k | 5 PoCs + 1 edital aprovado + SaaS beta |

### 7.4. Métricas Financeiras-Chave (Targets)

| Métrica | Target M12 | Target M24 | Target M36 |
|---------|-----------|-----------|-----------|
| MRR | R$ 25k (PoC recorrente) | R$ 80k (SaaS + Enterprise) | R$ 250k |
| Clientes pagantes | 5 | 30 | 100+ |
| Burn rate mensal | R$ 12k | R$ 40k | R$ 100k |
| Runway (meses) | 15+ | 12+ | 18+ |
| Margem bruta | 80% | 88% | 92% |

---

## 8. Análise de Riscos Expandida

### 8.1. Matriz de Riscos

| # | Risco | Prob. | Impacto | Score | Mitigação | Responsável |
|---|-------|-------|---------|-------|-----------|-------------|
| R1 | Motor não escala além de 15 qubits | 25% | Alto | 🔴 | Heurísticas adaptativas + foco em classes estruturadas | CTO |
| R2 | Nenhum cliente disposto a pagar em 12m | 20% | Alto | 🔴 | Benchmark gratuito → conversão; pivotar para consultoria | CEO |
| R3 | IBM lança feature equivalente | 30% | Alto | 🔴 | Patente defensiva + agnosticismo + ser adquirido | Ambos |
| R4 | CTO precisa se dedicar ao doutorado (defesa) | 40% | Médio | 🟡 | Planejar defesa nos primeiros 6 meses | CTO |
| R5 | PyZX muda licença ou descontinua | 10% | Médio | 🟢 | Fork interno + reimplementação proprietária | CTO |
| R6 | Edital de fomento não aprovado | 50% | Baixo | 🟡 | Bootstrapping viável + receita de PoC compensa | CEO |
| R7 | Dificuldade de contratar talento quantum | 60% | Médio | 🟡 | Stock options + bolsas + rede acadêmica | Ambos |
| R8 | Quantum winter (mercado esfria) | 10% | Fatal | 🟡 | Pivot para EDA clássica ou consultoria | CEO |
| R9 | Problemas entre sócios (divergências) | 15% | Alto | 🟡 | Acordo de sócios formal com cláusulas de resolução | CEO |
| R10 | Violação de IP (alguém patenteia antes) | 10% | Alto | 🟢 | Depósito prioritário de patente (primeiros 6 meses) | CEO |

### 8.2. Planos de Contingência

**Se R1 se materializa (motor não escala):**
- Pivotar para nichos de circuitos pequenos mas de alto valor (criptografia quântica, sensing)
- Oferecer como ferramenta híbrida: otimização ZX + transpilação clássica

**Se R2 se materializa (sem clientes):**
- Converter para modelo de consultoria (vender horas de PhD, não software)
- Buscar grants acadêmicos (CNPq, FAPERN) para financiar P&D até produto amadurecer

**Se R3 se materializa (IBM lança feature):**
- Posicionar como alternativa agnóstica ("funciona com IBM E com IonQ E com Rigetti")
- Buscar aquisição estratégica (IonQ, Rigetti, ou players menores que não têm compilador próprio)

---

# PARTE II — MAPEAMENTO DE CRITÉRIOS E ESTRATÉGIA DE INSCRIÇÃO

## 9. Critérios de Avaliação — Análise Tática

### 9.1. Distribuição de Pesos (Análise Estratégica)

O edital distribui os pesos assim:
| Eixo | Peso | % do total | Prioridade estratégica |
|------|------|-----------|----------------------|
| Tecnologia (inovação + desenvolvimento) | 1,5 | 30% | CRÍTICA |
| Mercado (viabilidade + validação) | 1,5 | 30% | CRÍTICA |
| Gestão (planejamento + papéis) | 1,0 | 20% | ALTA |
| Capital (financeiras) | 0,5 | 10% | MÉDIA |
| Currículo (formação + experiência) | 0,25 | 5% | BAIXA |
| Disponibilidade (horas/semana) | 0,25 | 5% | BAIXA (fácil maximizar) |

**Insight estratégico:** 60% da nota vem de Tecnologia + Mercado. Esses dois eixos DETERMINAM a aprovação. Gestão (20%) é o terceiro pilar. Currículo, disponibilidade e capital somam apenas 20% — são "complementos", não diferenciais.

**Consequência prática:** Investir 80% do esforço de preparação em demonstrar (1) inovação tecnológica e (2) viabilidade de mercado. Gestão deve ser impecável mas não precisa ser inovadora — clareza e coerência bastam.

### 9.2. Quadro 1 — Currículo (Peso 0,25) — Estratégia

**Critérios objetivos (fácil calcular):**

Para **Luccas (CEO):**
| Critério | Pontuação | Justificativa |
|----------|-----------|---------------|
| Graduação em área alinhada | 1-2 pts | Filosofia: argumentar "pensamento analítico e lógico" como base para gestão de tecnologia. Adicionar que está cursando Direito (IP/regulatório de tech) |
| Pós-graduação | 0 pts | Não se aplica (ainda) |
| Experiência profissional (1pt/ano, máx 2) | 2 pts | 3 anos em tech (citar: gestão de produto, operações, estratégia) |
| **Subtotal Luccas** | **3-4/5** | |

Para **Leandro (CTO):**
| Critério | Pontuação | Justificativa |
|----------|-----------|---------------|
| Graduação em área alinhada | 2 pts | Física — diretamente alinhada a computação quântica |
| Pós-graduação em área alinhada | 1 pt | Mestrado + Doutorado em Física/Computação Quântica |
| Experiência profissional (1pt/ano, máx 2) | 2 pts | 5 anos de pesquisa ativa = experiência profissional em área alinhada |
| **Subtotal Leandro** | **5/5** | |

**Nota consolidada (média dos sócios): ~4-4.5/5**

**Estratégia de maximização:**
- Apresentar experiência de Luccas de forma que evidencie ALINHAMENTO com TIC (não apenas "trabalhei em tech" mas "gestão de produto tecnológico", "operações de plataforma", "estratégia de startup")
- Vincular Filosofia a "pensamento algorítmico, lógica formal, teoria de sistemas" — linguagem que comunica com avaliadores de TIC
- Para Leandro: enfatizar que pesquisa de doutorado É o produto

### 9.3. Quadro 2 — Disponibilidade (Peso 0,25) — Estratégia

| Opção | Nota |
|-------|------|
| 40h/semana | 5 |
| 30-39h/semana | 4 |

**Decisão:** Declarar **40 horas para ambos os sócios**.

**Justificativa para Leandro (que está no doutorado):**
- A pesquisa de doutorado É o trabalho na SynthQ (são a mesma atividade intelectual)
- O orientador pode confirmar que a pesquisa tem foco direto no produto
- Dedicação ao doutorado = dedicação à startup (não são atividades concorrentes)
- Defesa prevista para os próximos 6-12 meses → após defesa, 100% na empresa

**Nota esperada: 5/5**

### 9.4. Quadro 3.1 — Tecnologia: Grau de Inovação (Peso embutido em 1,5)

**O que o avaliador quer ver:**
- Produto/serviço genuinamente novo (não incremental)
- Base científica sólida
- Diferencial tecnológico defensável
- Potencial de patenteamento

**Argumentos para nota 5/5:**

1. **Primeiro middleware comercial de otimização de T-count do mundo**
   - Validação: busca exaustiva por competidores mostra zero produtos standalone nesta categoria
   - IBM, Google, Quantinuum otimizam T-count INTERNAMENTE mas NÃO vendem como produto separado

2. **Base científica de fronteira**
   - ZX-Calculus: formalismo publicado na última década, com explosão de papers desde 2020
   - Artigo de referência (pygridsynth, 2026): demonstra que o campo está em evolução ativa
   - Pesquisa de Leandro posicionada na fronteira global

3. **Diferencial proprietário**
   - Heurísticas de reescrita (ordem de aplicação de regras ZX): IP core
   - Integração de técnicas de mixed synthesis (quadratic error suppression)
   - Foco em classes industriais de circuitos (VQE, QAOA, QFT) — não apenas exemplos acadêmicos

4. **Potencial de patente**
   - Método de otimização de circuitos quânticos via reescrita categórica
   - Sistema e método para redução automática de T-count em circuitos Clifford+T
   - Não existe prior art como PRODUTO (apenas como pesquisa acadêmica)

**Linguagem a usar nas respostas:**
> "Inovação radical — não existe produto equivalente no mercado global. Única solução comercial de otimização de T-count, baseada em pesquisa científica de fronteira (ZX-Calculus), com potencial de patenteamento e diferencial proprietário defensável."

### 9.5. Quadro 3.2 — Tecnologia: Grau de Desenvolvimento (Peso embutido em 1,5)

**O que o avaliador quer ver:**
- Protótipo funcional (requisito mínimo do edital)
- Evidência de que "funciona" (não apenas teoria)
- Clareza sobre o que já foi construído vs. o que falta

**Ponto vulnerável:** Este é o critério onde temos MENOR nota potencial. A tecnologia é inovadora mas o protótipo precisa de evidência concreta.

**Estratégia para maximizar (meta: 3.5-4/5):**

1. **Ter Jupyter notebook demonstrável** (OBRIGATÓRIO)
   - Input: circuito OpenQASM de 5-10 qubits
   - Processing: conversão para ZX, simplificação, extração
   - Output: circuito otimizado + métricas (T-count antes/depois)
   - DEVE estar funcionando antes da gravação do vídeo

2. **Apresentar como TRL 4** (validação em laboratório)
   - "Protótipo funcional demonstrado em ambiente controlado"
   - "Resultados reprodutíveis em benchmarks padrão"
   - "Pronto para validação com primeiros usuários"

3. **Comunicar roadmap de desenvolvimento com milestones claros**
   - Sinaliza maturidade de gestão técnica (não é "hobby de pesquisador")

4. **Mostrar resultados quantitativos**
   - "Redução média de X% no T-count em suite de Y circuitos de benchmark"
   - Números concretos > promessas vagas

**⚠️ AÇÃO CRÍTICA:** Leandro precisa ter, no mínimo, um notebook Jupyter funcional que demonstre a pipeline básica (parse → simplify → extract) em pelo menos 3-5 circuitos pequenos, com métricas de T-count antes/depois. SEM ISSO, A NOTA NESTE CRITÉRIO SERÁ BAIXA.

### 9.6. Quadro 3.3 — Mercado: Viabilidade Mercadológica (Peso embutido em 1,5)

**O que o avaliador quer ver:**
- Público-alvo definido e acessível
- Modelo de receita claro
- Competidores mapeados com diferenciais
- Tamanho de mercado crível

**Argumentos para nota 5/5:**

1. **Mercado quantificado com fontes críveis**
   - McKinsey Quantum Technology Monitor 2025
   - BCG Quantum Computing Market Report 2024
   - IBM Quantum Network: 200+ organizações pagantes (prova de demanda)

2. **Público-alvo ultra-definido**
   - Empresas nomeadas (Petrobras, Itaú, Vale)
   - Dor específica ("budget de QPU estourado")
   - Canal de acesso claro (gerentes de inovação via LinkedIn + eventos)

3. **Modelo de receita validado por analogia**
   - Modelo SaaS por uso = mesmo modelo de Datadog, Stripe, Twilio
   - Já funciona no quantum: IBM cobra por "runtime seconds", AWS cobra por "task"
   - SynthQ reduz o que eles cobram → proposta de valor direta

4. **Diferenciais cristalinos vs. competidores**
   - Tabela comparativa clara
   - Posição única no mapa competitivo (agnóstico + focado em T-count)

### 9.7. Quadro 3.4 — Mercado: Resultados de Validação (Peso embutido em 1,5)

**O que o avaliador quer ver:**
- Evidência de que alguém QUER isso (não apenas que é inovador)
- Testes com potenciais usuários
- Feedback do mercado

**Ponto vulnerável:** Ainda não temos clientes pagantes nem LOIs formais.

**Estratégia para maximizar (meta: 3-4/5):**

1. **Benchmark técnico como proxy de validação**
   - "Demonstramos redução de X% em circuitos utilizados pela indústria (VQE, QAOA)"
   - "Resultados reprodutíveis e publicados em [repositório/preprint]"
   - Benchmark = validação técnica, que é proxy para validação de mercado

2. **Validação indireta**
   - "Centros de inovação corporativos gastam $Y/ano em QPU time — dor comprovada"
   - "IBM Quantum Network tem 200+ membros pagantes — mercado existe"
   - "Nenhum produto resolve este problema específico — gap confirmado"

3. **Feedback qualitativo**
   - Se possível: emails/conversas com pesquisadores ou profissionais confirmando interesse
   - "Apresentamos a ideia em [evento/contexto] e recebemos feedback positivo de [X pessoas]"

4. **⚠️ ALTA PRIORIDADE:** Se possível antes da inscrição, obter 1 carta de interesse (LOI) de qualquer organização. Mesmo uma universidade declarando "gostaríamos de testar" já conta como validação.

### 9.8. Quadro 3.5 — Gestão: Clareza do Planejamento (Peso embutido em 1,0)

**O que o avaliador quer ver:**
- Roadmap estruturado com metas temporais
- KPIs mensuráveis
- Coerência entre objetivos e recursos
- Realismo (nem otimismo ingênuo nem pessimismo)

**Estratégia para nota 5/5:**
- Roadmap trimestral com KPIs SMART
- Plano financeiro coerente (custos + receitas + fontes)
- Análise de riscos com mitigações
- Timeline de desenvolvimento técnico + comercial alinhados

**Temos:** Tudo isso está neste documento. Basta transpor para as respostas de inscrição de forma concisa e estruturada.

### 9.9. Quadro 3.6 — Gestão: Clareza dos Papéis (Peso embutido em 1,0)

**O que o avaliador quer ver:**
- Divisão clara de responsabilidades
- Complementaridade
- Sem zona cinzenta / sobreposição
- Plano de expansão da equipe

**Estratégia para nota 5/5:**
- Tabela CEO vs CTO com responsabilidades não sobrepostas
- Destaque à complementaridade: negócios + ciência
- Mencionar pipeline de talento (bolsistas, stock options)
- Governança: acordo de sócios, vesting, IP assignment

### 9.10. Quadro 3.7 — Capital (Peso 0,5)

**O que o avaliador quer ver:**
- Custos realistas e detalhados
- Fontes de financiamento identificadas
- Sustentabilidade da operação
- Coerência entre ambição e recursos

**Estratégia para nota 4-5/5:**
- Custos mensais detalhados (R$ 9-12k/mês — realista para pré-incubação)
- Fontes: bootstrap + editais + receita de PoC
- Projeção de breakeven (mês 6)
- Taxa do Metrópole Parque cabível no orçamento

---

## 10. Projeção de Nota e Simulação

### 10.1. Cenário Base (Nota Esperada)

| Eixo | Critério | Peso | Nota | Ponderado |
|------|----------|------|------|-----------|
| Currículo | Formação + experiência | 0,25 | 4.5 | 1.125 |
| Disponibilidade | Horas/semana | 0,25 | 5.0 | 1.250 |
| Tecnologia | Grau de inovação | 0,75 | 5.0 | 3.750 |
| Tecnologia | Grau de desenvolvimento | 0,75 | 3.5 | 2.625 |
| Mercado | Viabilidade mercadológica | 0,75 | 4.5 | 3.375 |
| Mercado | Resultados de validação | 0,75 | 3.0 | 2.250 |
| Gestão | Clareza do planejamento | 0,50 | 5.0 | 2.500 |
| Gestão | Clareza dos papéis | 0,50 | 5.0 | 2.500 |
| Capital | Informações financeiras | 0,50 | 4.5 | 2.250 |
| **TOTAL** | | **5,00** | | **21.625** |

**Nota final: 21.625 / 5.00 = 4.33/5.0**

### 10.2. Cenário Pessimista (Sem Protótipo Robusto)

| Eixo | Critério | Peso | Nota | Ponderado |
|------|----------|------|------|-----------|
| Currículo | | 0,25 | 4.0 | 1.000 |
| Disponibilidade | | 0,25 | 5.0 | 1.250 |
| Tecnologia | Inovação | 0,75 | 4.5 | 3.375 |
| Tecnologia | **Desenvolvimento** | 0,75 | **2.5** | **1.875** |
| Mercado | Viabilidade | 0,75 | 4.0 | 3.000 |
| Mercado | **Validação** | 0,75 | **2.5** | **1.875** |
| Gestão | Planejamento | 0,50 | 4.5 | 2.250 |
| Gestão | Papéis | 0,50 | 4.5 | 2.250 |
| Capital | | 0,50 | 4.0 | 2.000 |
| **TOTAL** | | **5,00** | | **18.875** |

**Nota pessimista: 18.875 / 5.00 = 3.78/5.0** (ainda passa, mas com margem pequena)

### 10.3. Cenário Otimista (Com LOI + Benchmark Forte)

| Eixo | Critério | Peso | Nota | Ponderado |
|------|----------|------|------|-----------|
| Currículo | | 0,25 | 4.5 | 1.125 |
| Disponibilidade | | 0,25 | 5.0 | 1.250 |
| Tecnologia | Inovação | 0,75 | 5.0 | 3.750 |
| Tecnologia | Desenvolvimento | 0,75 | 4.5 | 3.375 |
| Mercado | Viabilidade | 0,75 | 5.0 | 3.750 |
| Mercado | Validação | 0,75 | 4.0 | 3.000 |
| Gestão | Planejamento | 0,50 | 5.0 | 2.500 |
| Gestão | Papéis | 0,50 | 5.0 | 2.500 |
| Capital | | 0,50 | 5.0 | 2.500 |
| **TOTAL** | | **5,00** | | **23.750** |

**Nota otimista: 23.750 / 5.00 = 4.75/5.0** (excelente)

### 10.4. Alavancas de Nota (O Que Move a Agulha)

| Ação | Impacto na nota final | Esforço | Prioridade |
|------|----------------------|---------|------------|
| Ter protótipo funcional demonstrável | +0.3 a +0.5 | Alto (CTO: 2-4 semanas) | **#1 CRÍTICA** |
| Ter benchmark quantitativo publicado | +0.2 a +0.4 | Médio (CTO: 1-2 semanas) | **#2 CRÍTICA** |
| Obter 1 LOI de organização | +0.2 a +0.3 | Médio (CEO: 2-4 semanas) | **#3 ALTA** |
| Declaração do orientador | +0 (requisito Deep Tech, não pontuação) | Baixo | **#4 OBRIGATÓRIA** |
| Vídeo de alta qualidade com demo | +0.1 a +0.2 | Médio (ambos: 1 semana) | **#5 ALTA** |
| Roadmap impecável no formulário | +0 a +0.1 (já estamos em 5/5) | Baixo | Média |

---

# PARTE III — ESTRATÉGIA DE EXECUÇÃO (PRIMEIROS 90 DIAS)

## 11. Plano de Ação Imediato

### 11.1. Sprint 0 — Preparação para Inscrição (Semanas 1-3)

| # | Ação | Responsável | Deadline | Entregável |
|---|------|-------------|----------|------------|
| 1 | Protótipo Jupyter funcional (parse→simplify→extract, 3-5 circuitos) | Leandro | Semana 2 | Notebook .ipynb executável |
| 2 | Benchmark: rodar em 10+ circuitos de referência, documentar T-count reduction | Leandro | Semana 2 | Tabela de resultados |
| 3 | Declaração do orientador (redigir + assinar) | Leandro + Orientador | Semana 1 | PDF assinado |
| 4 | Comprovante grupo de pesquisa (espelho CNPq) | Leandro | Semana 1 | PDF |
| 5 | Preenchimento das respostas Anexo A + B no formulário | Luccas | Semana 2 | Rascunho completo |
| 6 | Gravação do vídeo de 7 minutos | Ambos | Semana 3 | YouTube (não listado) |
| 7 | Revisão final e submissão | Luccas | Semana 3 | Inscrição submetida |
| 8 | Pagamento taxa de inscrição (R$ 100) | Luccas | Semana 3 | Comprovante |

### 11.2. Sprint 1 — Pós-Inscrição / Início MVP (Semanas 4-8)

| # | Ação | Responsável | Entregável |
|---|------|-------------|------------|
| 1 | Setup de repositório (Python 3.11, FastAPI, PyZX, rustworkx, testes) | Leandro | Repo GitHub privado |
| 2 | Parser robusto OpenQASM 2.0/3.0 → ZX | Leandro | Módulo parser testado |
| 3 | Motor de simplificação v1 (7 regras básicas) | Leandro | Módulo engine testado |
| 4 | Exporter ZX → OpenQASM | Leandro | Módulo exporter testado |
| 5 | API REST básica (POST /optimize) | Leandro | FastAPI rodando |
| 6 | Benchmark suite v1 (20 circuitos) | Leandro | Relatório + gráficos |
| 7 | Prospecção: lista de 15 centros de inovação + emails | Luccas | CRM/planilha |
| 8 | Proposta comercial de PoC (template) | Luccas | PDF modelo |
| 9 | Acordo de sócios (MOU) | Luccas + Advogado | Documento assinado |
| 10 | Submissão a edital Centelha 3 (se aberto) | Luccas | Formulário enviado |

### 11.3. Sprint 2 — Validação (Semanas 9-12)

| # | Ação | Responsável | Entregável |
|---|------|-------------|------------|
| 1 | Abordagem "Free Benchmark" para 5-10 empresas | Luccas | 5+ conversas agendadas |
| 2 | Motor v2: otimizações avançadas (phase gadgets, T-merging) | Leandro | Performance 2x melhor |
| 3 | Publicação de benchmark (blog ou preprint arXiv) | Ambos | URL pública |
| 4 | Primeiro benchmark real com circuito de cliente | Ambos | Relatório para cliente |
| 5 | Registro de marca INPI (SynthQ) | Luccas | Protocolo |
| 6 | Participação em 1 evento quantum (talk ou poster) | Leandro | Networking + visibilidade |

---

## 12. KPIs e Métricas de Acompanhamento

### 12.1. Dashboard de KPIs (Trimestral)

**Produto:**
| KPI | T1 | T2 | T3 | T4 |
|-----|----|----|----|----|
| T-count reduction médio (%) | 25% | 35% | 45% | 50%+ |
| Circuitos suportados (# qubits máx) | 10 | 15 | 20 | 30+ |
| Tempo de otimização (p95, segundos) | 30s | 10s | 5s | 2s |
| Benchmark suite size | 10 | 30 | 50 | 100 |

**Comercial:**
| KPI | T1 | T2 | T3 | T4 |
|-----|----|----|----|----|
| Leads qualificados | 5 | 15 | 25 | 35 |
| PoCs propostas | 0 | 3 | 5 | 8 |
| PoCs contratadas | 0 | 1 | 3 | 5 |
| Receita acumulada (R$) | 0 | 50k | 150k | 300k |

**Científico:**
| KPI | T1 | T2 | T3 | T4 |
|-----|----|----|----|----|
| Papers submetidos | 0 | 1 | 1 | 2 |
| Benchmark público (citations) | 0 | 0 | 5 | 15 |
| Patente depositada | Não | Não | Sim | — |

---

# ANEXO A — BENCHMARK COMPETITIVO (Para uso na inscrição)

## A.1. Metodologia

**Objetivo:** Demonstrar quantitativamente a capacidade de redução de T-count do motor SynthQ em circuitos de referência.

**Baseline de comparação:**
- Qiskit Transpiler (level 3, optimization_level=3)
- PyZX (full_reduce)
- Circuito original (sem otimização)

**Suite de circuitos de benchmark:**

| # | Circuito | Qubits | Descrição | Relevância industrial |
|---|----------|--------|-----------|----------------------|
| 1 | QFT (Quantum Fourier Transform) | 5 | Sub-rotina ubíqua | Criptografia, simulação |
| 2 | QFT | 8 | Escala maior | Idem |
| 3 | Grover (2 iterações) | 4 | Busca quântica | Otimização combinatória |
| 4 | VQE Ansatz (H₂ molécula) | 4 | Química quântica | Pharma, materiais |
| 5 | VQE Ansatz (LiH molécula) | 8 | Química quântica | Idem (mais complexo) |
| 6 | QAOA (MaxCut, p=1) | 5 | Otimização combinatória | Logística, finanças |
| 7 | QAOA (MaxCut, p=2) | 5 | Otimização combinatória | Idem (mais profundo) |
| 8 | Bernstein-Vazirani | 6 | Oráculo | Didático |
| 9 | Random Clifford+T (densidade 30%) | 10 | Stress test | Estresse do motor |
| 10 | Toffoli decomposition cascade | 5 | Multi-controlled | Aritmética quântica |

## A.2. Métricas Reportadas

Para cada circuito:
1. **T-count original** (após decomposição em Clifford+T)
2. **T-count após Qiskit transpiler level 3**
3. **T-count após PyZX full_reduce**
4. **T-count após SynthQ** (nosso motor)
5. **Redução percentual** ((original - SynthQ) / original × 100%)
6. **T-depth original vs. otimizado**
7. **Gate count total original vs. otimizado**
8. **Tempo de processamento** (segundos)

## A.3. Resultados Esperados (A Ser Preenchido com Dados Reais)

| Circuito | T-count Original | Qiskit L3 | PyZX | **SynthQ** | **Redução (%)** |
|----------|-----------------|-----------|------|-----------|----------------|
| QFT-5 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| QFT-8 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| Grover-4 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| VQE-H₂ | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| VQE-LiH | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| QAOA-p1 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| QAOA-p2 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| BV-6 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| Random-10 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |
| Toffoli-5 | [medir] | [medir] | [medir] | **[medir]** | **[calcular]** |

**⚠️ NOTA:** Esta tabela será preenchida com dados REAIS do protótipo. Não usar números inventados. A credibilidade da inscrição depende de resultados reprodutíveis.

## A.4. Análise Esperada

Com base na literatura (van de Wetering, 2020; Kissinger & van de Wetering, 2020), a simplificação ZX completa tipicamente reduz:
- T-count: 20-60% dependendo da estrutura do circuito
- T-depth: 15-50%
- Gate count total: 10-40%

Circuitos com **mais redundância Clifford** (VQE ansatz, QAOA) tendem a ter maior redução.
Circuitos **já otimizados** (QFT exata) tendem a ter menor redução.

## A.5. Apresentação dos Resultados

Para uso na inscrição, os resultados serão apresentados como:
1. **Gráfico de barras:** T-count por circuito (Original vs. SynthQ)
2. **Tabela resumo:** Redução média, máxima e mínima
3. **Comparação vs. state-of-the-art:** SynthQ vs. PyZX vs. Qiskit

---

# ANEXO B — CRONOGRAMA DE EDITAIS DE FOMENTO

## B.1. Editais Mapeados (2026-2027)

| Edital | Órgão | Valor (até) | Elegibilidade | Deadline (est.) | Probabilidade |
|--------|-------|-------------|---------------|----------------|---------------|
| Centelha 3 RN | FAPERN + FINEP | R$ 100k | Empreendedores RN | 2026 H2 | 40% |
| Tecnova III | FINEP | R$ 300k | Startups deep tech | 2026 H2 | 25% |
| PIPE Fase 1 | FAPESP | R$ 250k | Empresa com sede em SP (parceiro?) | 2027 H1 | 20% |
| RHAE Pesquisador na Empresa | CNPq | R$ 80k/ano (bolsa) | Empresa com CNPJ + pesquisador | 2027 | 30% |
| Startups Conectadas | SEBRAE + ANPROTEC | R$ 50k + mentoria | Incubadas/aceleradas | Fluxo contínuo | 50% |
| Lei do Bem (11.196/05) | MCTI | Incentivo fiscal 60-80% | PJ com lucro real | Após CNPJ + receita | Médio prazo |
| EMBRAPII | EMBRAPII + UFRN | Co-financiamento P&D | Parceria com ICT | 2027 | 30% |

## B.2. Estratégia de Submissão

**Prioridade 1 (inscrever assim que possível):**
- Centelha 3 RN (FAPERN): Melhor fit — startup nascente no RN, deep tech, pré-incubada

**Prioridade 2 (após CNPJ):**
- Tecnova III (FINEP): Maior valor, requer CNPJ
- RHAE (CNPq): Financia bolsa do CTO/pesquisadores

**Prioridade 3 (médio prazo):**
- EMBRAPII: Co-financiamento de P&D com UFRN como ICT parceira
- Lei do Bem: Incentivos fiscais sobre gastos com P&D

---

# ANEXO C — GLOSSÁRIO PARA AVALIADORES NÃO TÉCNICOS

| Termo | Explicação Acessível |
|-------|---------------------|
| Qubit | A unidade básica de informação quântica (como o "bit" clássico, mas pode ser 0 e 1 ao mesmo tempo) |
| Porta T | Uma operação básica em computação quântica que é muito cara de executar. Como se fosse a "gasolina premium" dos computadores quânticos |
| T-count | Número de portas T em um circuito. Quanto menor, mais barato e rápido de rodar |
| Clifford+T | O "vocabulário básico" da computação quântica tolerante a falhas — um conjunto mínimo de operações que permite fazer qualquer cálculo |
| ZX-Calculus | Um método matemático de representar e simplificar circuitos quânticos usando grafos (diagramas de pontos e linhas) |
| Magic State Distillation | Processo caro e complexo necessário para executar portas T. Consome até 90% dos recursos do computador |
| FTQC | Computação quântica tolerante a falhas — a próxima geração de computadores quânticos, mais confiáveis |
| NISQ | Era atual dos computadores quânticos — "intermediários, ruidosos, de escala limitada" |
| QPU | Processador quântico (como a GPU é para gráficos, a QPU é para cálculos quânticos) |
| OpenQASM | Linguagem padrão para escrever programas quânticos (como Python é para programas clássicos) |
| SaaS | Software as a Service — modelo de venda de software por assinatura mensal (como Netflix, Spotify) |

---

*Fim do Documento 1 — Plano de Negócios Interno SynthQ v3.0*
*Para uso exclusivo dos fundadores. Não distribuir sem autorização.*
