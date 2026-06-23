# DOCUMENTO 6 — ROTEIRO DO VÍDEO DE APRESENTAÇÃO
## SynthQ — Candidatura Metrópole Parque (IMD/UFRN)
## Edital Unificado Nº 01/2026 | Pré-incubação Deep Tech

**Duração máxima:** 7 minutos
**Formato:** Videochamada gravada (dois fundadores em cidades diferentes)
**Plataforma de publicação:** YouTube (não listado)
**Resolução mínima:** 720p (recomendado 1080p)

---

# CONFIGURAÇÃO TÉCNICA

## Equipamento recomendado

| Item | Luccas (CEO) | Leandro (CTO) |
|------|-------------|---------------|
| Câmera | Webcam HD ou câmera de celular (tripé) | Idem |
| Áudio | Microfone de lapela ou headset com bom mic | Idem |
| Iluminação | Ring light ou janela frontal (evitar contraluz) | Idem |
| Fundo | Limpo, neutro (parede lisa ou background virtual discreto) | Idem |
| Internet | Cabo ethernet se possível (evitar cortes) | Idem |

## Setup da gravação

**Opção A (recomendada): Gravação em Zoom/Google Meet com compartilhamento de tela**
- Ambos em chamada de vídeo
- Gravar via recurso nativo da plataforma (Zoom: "Record to Cloud")
- Para a demo: CTO compartilha tela com Jupyter rodando
- Vantagem: natural, mostra dinâmica real da dupla

**Opção B: Gravação individual + edição**
- Cada um grava seu segmento individualmente (OBS Studio ou similar)
- Editor monta os segmentos com transições
- Para a demo: screen recording separado do Jupyter
- Vantagem: melhor qualidade técnica, mas menos natural

**Recomendação:** Opção A — o edital valoriza autenticidade e dinâmica da equipe. Uma videochamada real transmite colaboração genuína.

---

# ROTEIRO MINUTO A MINUTO

## [0:00 – 0:45] ABERTURA E APRESENTAÇÃO PESSOAL

**Quem aparece:** Ambos em tela dividida (side by side)

**LUCCAS (CEO):**
> "Olá! Somos a SynthQ. Eu sou Luccas Cavicchioli — filósofo de formação, estudante de Direito, e há três anos no ecossistema de tecnologia. Sou o CEO, responsável pela estratégia de negócios, captação e go-to-market."

**LEANDRO (CTO):**
> "E eu sou Leandro Moraes — físico, mestre e doutorando em Física pela UFRN, com período na USP. Minha pesquisa é em algoritmos e computação quântica, especificamente em otimização de circuitos via ZX-Calculus. Sou o CTO — responsável por toda a tecnologia e pesquisa."

**LUCCAS:**
> "Estamos nos candidatando à pré-incubação Deep Tech no Metrópole Parque porque acreditamos que a computação quântica precisa de ferramentas de infraestrutura — e nós temos a ciência para construir isso."

**[Dica visual:** Sorriso, postura aberta, olhar na câmera. Tom: confiante mas não arrogante.]

---

## [0:45 – 2:00] O PROBLEMA

**Quem lidera:** LEANDRO (credibilidade técnica)
**Visual:** Slide ou imagem compartilhada (opcional) mostrando diagrama simples de circuito quântico

**LEANDRO:**
> "Para entender o que fazemos, preciso explicar um conceito: na computação quântica tolerante a falhas, toda computação é traduzida em um vocabulário básico chamado Clifford+T.
>
> Neste vocabulário, as operações Clifford são baratas — quase gratuitas. Mas as operações T são extremamente caras. Cada porta T requer um processo chamado Magic State Distillation, que consome até 90% dos recursos físicos do computador quântico.
>
> Em termos práticos: quando uma empresa roda um circuito quântico na nuvem — no IBM Quantum, no AWS Braket — o custo é dominado pelo número de portas T. Quanto mais portas T, mais caro, mais lento, e às vezes impossível de rodar no hardware disponível."

**LUCCAS:**
> "Traduzindo para linguagem de negócios: um único problema de simulação molecular pode custar centenas de milhares de dólares em tempo de QPU. E ninguém oferece uma ferramenta que reduza esse custo de forma automática e garantida."

**[Dica visual:** Se usar slide, mostrar diagrama simples: circuito com muitas portas T → "$$$$". Manter visual LIMPO — não sobrecarregar.]

---

## [2:00 – 2:45] A SOLUÇÃO

**Quem lidera:** LUCCAS (pitch comercial)
**Visual:** Tela com diagrama da pipeline (simplificado)

**LUCCAS:**
> "A SynthQ resolve exatamente isso. Somos um middleware de otimização: o cliente nos envia um circuito quântico no formato padrão da indústria — OpenQASM — e nós devolvemos o mesmo circuito, matematicamente equivalente, mas com 30 a 60% menos portas T.
>
> O resultado: menos custo de execução, circuitos que cabem em hardware menor, e tudo isso sem mudar uma linha do código do cliente. É complementar a qualquer plataforma — funciona com IBM, com AWS, com Google, com qualquer hardware."

**LEANDRO:**
> "A mágica — literalmente — está no ZX-Calculus. É um formalismo matemático que permite representar circuitos quânticos como grafos e aplicar transformações que preservam o resultado computacional mas simplificam a estrutura. Minha pesquisa de doutorado é exatamente nisso — e a SynthQ transforma essa ciência em produto."

---

## [2:45 – 5:00] DEMONSTRAÇÃO DO PROTÓTIPO

**Quem lidera:** LEANDRO (compartilha tela)
**Visual:** Jupyter Notebook rodando ao vivo

**[Leandro compartilha tela com o Jupyter Notebook aberto]**

**LEANDRO:**
> "Deixa eu mostrar o protótipo funcionando. Aqui tenho um Jupyter Notebook com nossa pipeline."

**[Passo 1 — Input]**
> "Primeiro, carrego um circuito de benchmark — uma QFT de 5 qubits, que é uma sub-rotina fundamental em computação quântica."

**[Executa célula — mostra o circuito original]**
> "Aqui temos o circuito original: [X] portas no total, [Y] portas T."

**[Passo 2 — Otimização]**
> "Agora rodo o motor SynthQ — ele converte para representação ZX, aplica as simplificações, e extrai o circuito otimizado."

**[Executa célula — mostra processamento]**
> "Pronto. Levou [Z] segundos."

**[Passo 3 — Resultado]**
> "Resultado: o circuito otimizado tem [A] portas T — uma redução de [B]%. O circuito é matematicamente idêntico ao original, mas significativamente mais barato de executar."

**[Passo 4 — Tabela comparativa]**
> "E aqui uma tabela com vários circuitos de benchmark. Redução média de [C]% no T-count."

**[Volta para tela dividida]**

**LUCCAS:**
> "Isso que o Leandro acabou de mostrar se traduz diretamente em economia. Se um cliente gasta R$ 200 mil por ano em tempo de QPU, estamos falando de R$ 60 a 120 mil de economia. E isso é apenas com os algoritmos que já temos funcionando."

**[Dicas para a demo:**
- Ensaiar pelo menos 3 vezes antes de gravar
- Ter cells pré-executadas como backup (caso dê erro ao vivo)
- Circuitos pequenos (5-8 qubits) para execução rápida na câmera
- Mostrar números REAIS — não inventar
- Se possível, mostrar um gráfico de barras (antes/depois) ao final]

---

## [5:00 – 5:45] MERCADO E MODELO DE NEGÓCIOS

**Quem lidera:** LUCCAS
**Visual:** Volta para tela dividida (ambos em câmera)

**LUCCAS:**
> "O mercado de software quântico projeta 8,6 bilhões de dólares até 2030. Dentro disso, middleware e compiladores são a camada onde se captura valor sem depender de hardware específico.
>
> Nosso modelo começa com projetos de PoC — a empresa nos envia circuitos reais, otimizamos, e entregamos um relatório de economia. Ticket de 30 a 80 mil reais por projeto. Já mapeamos centros de inovação como Petrobras, Itaú e Embraer como primeiros clientes potenciais.
>
> No médio prazo, evoluímos para API SaaS — o desenvolvedor quântico chama nossa API, envia o circuito, recebe de volta otimizado em segundos. Margem bruta superior a 90%, modelo recorrente."

---

## [5:45 – 6:30] EQUIPE E DIFERENCIAL

**Quem lidera:** Alternado
**Visual:** Tela dividida

**LUCCAS:**
> "Nosso diferencial começa pela equipe. A combinação é rara: eu trago visão de mercado, captação e execução de negócios. O Leandro traz o que pouquíssimas pessoas no mundo têm — conhecimento científico profundo exatamente no problema que estamos resolvendo."

**LEANDRO:**
> "Não existe nenhum produto comercial no mundo dedicado exclusivamente à redução de T-count. A IBM otimiza para hardware próprio. A Quantinuum tem lock-in. Ferramentas acadêmicas como PyZX não são produto. Nós somos os únicos a oferecer isso de forma agnóstica, como serviço, com garantia matemática."

**LUCCAS:**
> "E é por isso que somos Deep Tech genuína — não estamos aplicando tecnologia pronta. Estamos transformando pesquisa de fronteira em empresa."

---

## [6:30 – 7:00] CHAMADA PARA AÇÃO / ENCERRAMENTO

**Quem lidera:** LUCCAS (fecha)
**Visual:** Tela dividida, ambos em câmera

**LUCCAS:**
> "O que buscamos no Metrópole Parque é o ambiente certo para transformar essa pesquisa em empresa. Nos próximos 12 meses, queremos: formalizar a empresa, conquistar 5 clientes pagantes, e publicar nossos resultados.
>
> Temos a ciência. Temos a oportunidade de mercado. Precisamos do ecossistema — e o IMD é o lugar certo para isso."

**LEANDRO:**
> "Obrigado pela atenção. Estamos à disposição para qualquer pergunta."

**[Ambos acenam / sorriem. Fim.]**

---

# NOTAS DE PRODUÇÃO

## Timing detalhado

| Segmento | Início | Fim | Duração | Responsável principal |
|----------|--------|-----|---------|----------------------|
| Abertura | 0:00 | 0:45 | 45s | Ambos |
| Problema | 0:45 | 2:00 | 75s | Leandro → Luccas |
| Solução | 2:00 | 2:45 | 45s | Luccas → Leandro |
| Demo | 2:45 | 5:00 | 135s | Leandro (tela) |
| Mercado | 5:00 | 5:45 | 45s | Luccas |
| Equipe | 5:45 | 6:30 | 45s | Alternado |
| Encerramento | 6:30 | 7:00 | 30s | Luccas → Leandro |
| **TOTAL** | | | **7:00** | |

## Checklist pré-gravação

- [ ] Jupyter Notebook testado e funcionando (executar todas as células 2x antes)
- [ ] Conexão de internet estável (testar velocidade: mínimo 10 Mbps up)
- [ ] Áudio testado (gravar 30s de teste e ouvir — sem eco, sem ruído)
- [ ] Iluminação verificada (rosto bem iluminado, sem sombras fortes)
- [ ] Fundo limpo e profissional
- [ ] Roteiro impresso ou em segundo monitor (não ler literalmente — usar como guia)
- [ ] Zoom/Meet configurado para gravar em alta qualidade
- [ ] Backup: cells do Jupyter pré-executadas (screenshot dos outputs caso dê erro ao vivo)
- [ ] Relógio visível para controlar tempo

## Checklist pós-gravação

- [ ] Assistir inteiro e verificar: áudio claro? Imagem boa? Demo visível?
- [ ] Duração ≤ 7 minutos (cortar se necessário)
- [ ] Upload no YouTube como "não listado"
- [ ] Testar link em aba anônima (verificar que funciona sem login)
- [ ] Copiar link para o campo da Pergunta 17 do Anexo B

## Dicas de comunicação

| Fazer | Evitar |
|-------|--------|
| Olhar na câmera (não no rosto do outro na tela) | Ler roteiro literalmente |
| Tom conversacional, natural | Falar rápido demais (ansiedade) |
| Pausas breves entre seções | Jargão excessivo sem explicar |
| Gesticular naturalmente | Ficar estático / robótico |
| Sorrir nos momentos certos (abertura, encerramento) | Parecer entediado ou inseguro |
| Usar "nós" (reforça equipe) | Interromper o outro |
| Falar em português claro e direto | Usar inglês desnecessariamente |
| Mostrar entusiasmo genuíno | Prometer resultados que não tem |

## Alternativas se a demo falhar ao vivo

1. **Plano B — Demo pré-gravada:** Gravar screen recording do Jupyter funcionando separadamente, e inserir como "corte" durante o vídeo. Leandro narra por cima.
2. **Plano C — Screenshots:** Se nada funcionar, mostrar screenshots estáticos dos outputs do notebook com narração explicativa.
3. **Recomendação:** Gravar 2-3 takes. Usar o melhor. Não precisa ser perfeito — precisa ser autêntico e demonstrar que funciona.

---

# TEXTO DE APOIO (Para decorar / usar como base)

## Frases-chave para ter na ponta da língua

- "A SynthQ reduz o custo de computação quântica em 30 a 60%, de forma automática e garantida."
- "Somos o único middleware comercial de otimização de T-count no mundo."
- "Transformamos pesquisa de fronteira em produto — isso é Deep Tech."
- "O circuito otimizado é matematicamente idêntico ao original."
- "Funcionamos com qualquer hardware — IBM, IonQ, Rigetti, qualquer um."
- "Nos próximos 12 meses: 5 clientes, CNPJ formalizado, e uma publicação científica."

## Perguntas que os avaliadores podem fazer (e respostas rápidas)

| Pergunta provável | Resposta concisa |
|-------------------|------------------|
| "O que diferencia vocês do Qiskit transpiler?" | "O Qiskit otimiza para hardware IBM específico. Nós otimizamos a lógica pura — antes do Qiskit rodar. São complementares." |
| "Por que não open-source?" | "O valor está nas heurísticas proprietárias de otimização. Publicamos resultados e benchmarks, mas o como é nosso IP." |
| "Como validam que funciona?" | "Verificação matemática: simulamos o circuito original e otimizado — devem produzir o mesmo resultado. É provável, não empírico." |
| "Já têm clientes?" | "Estamos em fase de validação técnica. Mapeamos [X] centros de inovação e planejamos oferecer benchmarks gratuitos como porta de entrada." |
| "E se a computação quântica demorar mais que o previsto?" | "Nosso modelo funciona já no regime NISQ — circuitos menores já se beneficiam. E quanto mais o mercado cresce, mais nosso produto importa." |

---

*Fim do Documento 6 — Roteiro do Vídeo SynthQ*
*Nota: Este roteiro é um guia. Adaptar com naturalidade durante a gravação.*
