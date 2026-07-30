# Plano de implementação — Conferidor do compilado (rumo ao crawler da v2.0.0)

> **ARQUIVO TEMPORÁRIO DE ENGENHARIA.** Não é documentação do site. Cada fase
> concluída marca seus checkboxes; ao concluir a F5, **excluir este arquivo** no
> mesmo PR (o registro permanente é o changelog e o roadmap). Plano escrito em
> 29/07/2026, após a revisão manual de defasagem (v1.2.2–v1.2.13), cujas lições
> estão incorporadas aqui e em `REVISAO-LEGISLATIVA.md`.

## 1. Por que este plano existe — e o que ajusta no roadmap

O catálogo (`data/crimes.json`) foi montado por acréscimo, não raspado do texto
compilado numa data fixa; a defasagem é irregular e só foi fechada por revisão
manual (10 sessões, v1.2.2–v1.2.13). O roadmap prevê na v2.0.0 um **crawler do
DOU** (fluxo de normas novas + classificação por IA). A revisão manual provou que
a fundação correta é outra:

- **O texto compilado do Planalto é a autoridade consolidada**: risca o texto
  revogado, anota "(Incluído/Redação dada/Revogado pela Lei nº X, de YYYY)" e
  incorpora a redação vigente. Conferir contra ele é **determinístico** — não
  exige interpretar o DOU nem classificador de IA para 95% do problema.
- O fluxo do DOU continua valendo como **sinal de frescor** (saber *quando*
  reconferir), mas não como fonte primária de verdade.

Portanto o plano divide a entrega em duas partes com contratos diferentes:

| Parte | O quê | Contrato de dados | Versão |
|---|---|---|---|
| **A — Conferidor (este plano, F0–F5)** | Baixa o compilado, parseia, **compara e RELATA** divergências. Nada entra nos dados automaticamente. | Nenhuma mudança — é ferramenta interna. | Sem release própria; correções apontadas seguem `1.2.Z`. |
| **B — Crawler v2.0.0 (futuro, fora deste plano)** | Revogados entram no dataset (`revogado_em`, `revogado_por`, `vigente_desde`, `fonte`, `atualizado_em`), fusão com o acervo histórico, PRs automáticos. | Quebra o invariante "todo registro é direito vigente". | `2.0.0`, após v1.3.0/v1.4.0 (pré-requisitos do roadmap). |

A Parte A entrega ~80% do valor (nunca mais descobrir defasagem por acaso) sem
esperar os pré-requisitos da v2.0.0. Ao implementar, **atualizar a seção v2.0.0
do roadmap** para registrar essa mudança de arquitetura (compilado-first; DOU
como watcher).

**Destino do crawler do DOU (decidido em 29/07/2026):** o crawler do DOU com
classificador de IA está **abandonado** e substituído por um **watcher sem IA**
(seção 5.11, fase F7): filtro textual semanal na Seção 1 do DOU por citação dos
diplomas monitorados e por palavras-chave penais ("pena", "reclusão",
"detenção", "revoga"…). A vacatio legis dá a folga: com o Planalto revisado
semanalmente, uma olhada simples no DOU basta. O watcher cobre o único ponto
cego do conferidor — **lei penal nova autônoma** (diploma que ainda não está em
`fontes.json` e, portanto, em nenhuma página monitorada).

## 2. Decisões de arquitetura (fechadas — não rediscutir na implementação)

1. **Linguagem: Python 3.12**, como os scripts existentes. **A F1 não precisou
   de nenhuma dependência externa** (só a biblioteca padrão); se a F2 precisar
   de parser HTML, criar `scripts/crawler/requirements.txt` — nunca no build do
   site.
2. **Fetch: HTTP simples (`urllib`) com User-Agent de navegador — REVISADO na
   F1** (30/07/2026). A conclusão da F0 ("Playwright obrigatório") **estava
   errada**: era erro meu de decodificação (a Lei 11.340 vem em UTF-16 e eu a
   li como cp1252, o que a fez parecer pré-2018). Com detecção de charset
   correta, **62/62 fontes vieram atuais por HTTP puro**. Sem Playwright, sem
   browser na CI. Sem UA a conexão é recusada; a sentinela por fonte continua
   obrigatória. Evidências em `crawler/DECISOES-F0.md`.
3. **Relatório, nunca escrita automática.** O conferidor produz
   `crawler/relatorios/AAAA-MM-DD.md` (+ `.json`). Humano decide e aplica como
   patch (`1.2.Z`), como na revisão manual. Acuidade jurídica é o valor central:
   dado errado publicado é pior que dado ausente.
4. **Comparar contra o DERIVADO** (`static/data/crimes.json`), não contra a
   fonte: a moldura real vem de `parse_pena_range(obs)` — comparar com
   `pena_min/max` da fonte geraria falsos resultados (armadilha nº 2 da revisão).
5. **Snapshots HTML não são commitados** (ficam em `crawler/snapshots/`,
   gitignored; na CI viram artifact). **Fixtures de teste são commitadas**
   (trechos pequenos, congelados).
6. **Casamento por artigo em TODOS os rótulos** — nunca filtrar por `lei`
   (armadilha nº 1: artigos do CP rotulados pela lei criadora, ex.
   `lei="Lei 14.811/24"`).

## 3. O que já existe e será reaproveitado

| Ativo | Onde | Uso no conferidor |
|---|---|---|
| Mapa `PLANALTO` (28 padrões → URL do compilado) | `scripts/transform_data.py:184` | Semente do `data/fontes.json` (F1). Hoje cobre ~28 dos ~60 diplomas. |
| `parse_pena_range(obs)` | `transform_data.py:347` | Extrair para `scripts/pena_parser.py` compartilhado (F3) — **refactor deve manter `transform_data.py` byte-idêntico no derivado** (CI compara). Atenção: o formato do Planalto é "de 2 (dois) a 4 (quatro) anos" — pré-normalizar removendo os por-extenso entre parênteses antes de aplicar o parser. |
| `chave_dispositivo`, normalização de artigo | `transform_data.py:210` | Chave de casamento no differ. |
| Workflows `ci.yml` / `regen-data.yml` | `.github/workflows/` | Modelo para o workflow mensal (F5). |
| Revisão manual v1.2.2–v1.2.13 | changelog + `REVISAO-LEGISLATIVA.md` | **Gabarito de testes** (seção 7). |

## 4. Estrutura de arquivos proposta

```
data/fontes.json                    # registro de diplomas → URL + sentinela (F1)
scripts/pena_parser.py              # parse_pena_range extraído/estendido (F3)
scripts/crawler/
  __init__.py
  requirements.txt                  # playwright, beautifulsoup4, lxml
  baixar.py                         # CLI: fetch + validação de frescor (F1)
  parsear.py                        # HTML → modelo estruturado (F2)
  conferir.py                       # differ + relatório (F3)
  vigencia.py                       # checador de vacatio legis (F4)
  revogacao.py                      # detector de revogação total / LexML (F4)
  fixtures/                         # trechos HTML congelados p/ testes (F2)
  tests/                            # pytest (F2–F4)
crawler/                            # gitignored: snapshots/ e relatorios/
.github/workflows/conferidor.yml    # cron mensal → issue com relatório (F5)
```

## 5. O pipeline, componente a componente

### 5.1 `data/fontes.json` (F1)

Uma entrada por **diploma** (não por rótulo). Esquema:

```json
{
  "id": "cp",
  "rotulos": ["CP", "CP (atualiz.)", "Lei 14.811/24", "Lei 14.478/22"],
  "url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
  "sentinela": "Lei nº 15.397, de 2026",
  "obs": "rotulos inclui leis criadoras de artigos do CP presentes no catálogo"
}
```

- `rotulos`: todos os valores de `lei` do catálogo que apontam para este
  diploma. Resolve os rótulos divididos (`Lei 9.605/98 (atualiz.)`) e as leis
  criadoras. Validação: **todo rótulo distinto de `crimes.json` deve constar de
  exatamente um diploma** (a CI do conferidor falha se sobrar rótulo órfão).
- `sentinela`: string de emenda recente **que DEVE existir na página** (a mais
  nova conhecida). É o teste de frescor barato: página sem a sentinela = cache
  velho → o fetch falha alto em vez de conferir contra texto desatualizado.
  Atualizada a cada reforma incorporada.
- Semear com o mapa `PLANALTO` e completar os ~32 diplomas restantes (lista de
  rótulos: rodar `python -c` com `collections.Counter` sobre `crimes.json`).
- `transform_data.url_planalto()` passa a ler deste arquivo (fonte única).

### 5.2 Fetcher — `baixar.py` (F1)

- CLI: `python scripts/crawler/baixar.py [--fonte cp] [--todas] [--forcar]`.
- Playwright/Chromium headless; espera `networkidle`; salva
  `crawler/snapshots/<id>/<AAAA-MM-DD>.html` + `meta.json` (data, hash, URL).
- **Encoding**: páginas antigas do Planalto são windows-1252; ler o `meta
  charset` do HTML e decodificar de acordo (fallback: tentar utf-8 → cp1252).
- Valida a sentinela; sem ela, exit code ≠ 0 com mensagem clara.
- Politeness: 1 requisição a cada 2s, User-Agent identificado
  (`sispenas-conferidor/1.0 (+https://amorim-rc.github.io/sispenas/)`), 2
  retries com backoff. ~60 páginas por rodada — carga desprezível.

### 5.3 Parser — `parsear.py` (F2) — **o núcleo difícil**

Entrada: HTML de um snapshot. Saída: JSON estruturado por dispositivo:

```json
{
  "artigo": "Art. 121", "sufixo": null,
  "dispositivo": "§2º-D",
  "situacao": "vigente" | "revogado" | "vetado",
  "texto": "…",
  "pena_texto": "Pena – reclusão, de 20 (vinte) a 40 (quarenta) anos.",
  "anotacao": {"acao": "incluido", "norma": "Lei nº 15.358", "ano": 2026},
  "tem_vigencia_pendente": false
}
```

Regras aprendidas na revisão manual (cada uma vira caso de teste):

1. **Versões sobrepostas**: quando um dispositivo é alterado, o Planalto mantém
   a redação antiga (riscada com `<strike>`/`<s>` — mas NEM SEMPRE) seguida da
   nova. No art. 24-A da Lei Maria da Penha há **duas linhas "Pena" consecutivas
   sem strike** (a antiga de 2018 e a nova de 2024). Regra: dentro de um mesmo
   dispositivo, **a versão vigente é a de anotação mais recente**; texto riscado
   é sempre não vigente. Este é o risco nº 1 de precisão do projeto.
2. **Anotações**: regex sobre `\((Inclu[íi]d[oa]|Reda[çc][ãa]o dada|Revogad[oa]|
   Renumerad[oa])[^)]*?pela\s+(Lei|Lei Complementar|Medida Provisória)[^)]*?
   ([\d.]+)[^)]*?de\s+(\d{4})\)` — capturar ação, norma e ano.
3. **Tokens a tratar**: `(VETADO)`, `(Vide …)`, `Vigência`, `Produção de
   efeitos` (os dois últimos disparam o checador da 5.6).
4. **Hierarquia**: caput / §§ / incisos / alíneas; epígrafe (nomen juris) na
   linha anterior ao "Art.". Artigos com sufixo (121-A, 217-A, 359-M).
5. Números por extenso nos intervalos: "de 2 (dois) a 5 (cinco) anos" —
   normalizar `\(\w[^)]*\)` fora de anotações antes do parse de pena.

### 5.4 Extrator de pena — `scripts/pena_parser.py` (F3)

- Extrair `parse_pena_range` + `_norm_unidade` + constantes do
  `transform_data.py` para módulo compartilhado; `transform_data` importa dele
  (**critério: derivado byte-idêntico após o refactor**).
- Estender com: pré-normalização dos por-extenso; "até N anos/meses" (mínimo
  legal implícito — LCP art. 32 e CE têm pena só de teto, min=0 no catálogo);
  tipo de pena (reclusão/detenção/prisão simples/impedimento — CPM tem
  "impedimento" e "suspensão do exercício do posto"); multa
  (cumulativa "e multa" / alternativa "ou multa").

### 5.5 Differ — `conferir.py` (F3)

- Índice do catálogo: para cada entrada do **derivado**, chave
  `(diploma_id, artigo_normalizado)` — o diploma vem de `fontes.json.rotulos`
  (nunca do rótulo cru).
- Classificação por dispositivo:
  - **AUSENTE**: vigente na lei com pena própria, sem linha no catálogo;
  - **REVOGADO**: linha no catálogo, dispositivo revogado/vetado na lei;
  - **DIVERGENTE-moldura**: `pena_faixa_rotulo` ≠ intervalo extraído;
  - **DIVERGENTE-tipo**: reclusão×detenção etc.;
  - **SEM-CASAMENTO**: dispositivo da lei não parseável / linha do catálogo sem
    dispositivo correspondente (revisar parser antes de acusar o catálogo);
  - **OK**.
- **Lista de exceções deliberadas** (`scripts/crawler/excecoes.json`): casos que
  o humano já avaliou e decidiu manter (ex.: equiparações modeladas como
  modificador e não linha; formas "aumenta a respectiva pena" que viraram
  modificadores na v1.2.6). Cada exceção com justificativa e data. Sem isso o
  relatório mensal repetiria para sempre os mesmos achados já decididos.
- Modificadores (`data/modificadores.json`) na primeira versão: **fora do
  diff automático** — apenas listar anotações de leis novas nos artigos-fonte
  dos modificadores, para triagem humana.

### 5.6 Checador de vigência — `vigencia.py` (F4)

Para todo achado cuja anotação seja de lei com menos de ~24 meses: baixar a
lei-reforma (`/_atoAAAA-AAAA/AAAA/lei/lNNNNN.htm`), localizar a cláusula "entra
em vigor" e calcular a data efetiva (lição da Lei 15.190/2025: 180 dias de
vacatio; da LC 224/2025: efeitos em 1º/01/2026). Achado ainda não vigente sai no
relatório numa seção própria ("vigência futura — não aplicar ainda"), com data.

### 5.7 Detector de revogação total — `revogacao.py` (F4)

Lição dos agrotóxicos: a página da Lei 7.802/89 **não anuncia** que a Lei
14.785/2023 a revogou por inteiro. Verificações (LexML foi testado na F0 e
**descartado** — URN sem metadados estáticos; SRU atrás de challenge anti-bot):

1. Banner no topo do snapshot (regex `Revogad[ao]\s+pela` nos primeiros 2KB);
2. **Watcher do DOU (5.11/F7)**: a lei revogadora nova casa a citação do
   diploma e o vocabulário penal — cobre o caso dali em diante;
3. Fallback: alerta de envelhecimento — diploma sem alteração há N anos é
   sinalizado para conferência manual esporádica.

### 5.8 Relatório

- `crawler/relatorios/AAAA-MM-DD.md`: sumário por diploma → achados ordenados
  por gravidade (REVOGADO > DIVERGENTE > AUSENTE > vigência futura), cada um com
  o trecho da lei, a linha do catálogo (id, rótulo) e o link do compilado.
- `.json` gêmeo com os mesmos dados (máquina; diffs entre rodadas).
- Exit codes de `conferir.py`: 0 = sem achados novos; 3 = achados (para a CI
  distinguir de erro real).

### 5.9 Automação — `.github/workflows/conferidor.yml` (F5)

- **Cadência: semanal, toda segunda-feira às 05:00 de Brasília** — cron em UTC:
  `0 8 * * 1` (Brasília é UTC−3 fixo; o horário de verão foi extinto em 2019).
  O GitHub pode atrasar crons alguns minutos — irrelevante aqui.
- **Acionamento manual** (`workflow_dispatch`): GitHub → aba **Actions** →
  workflow "Conferidor" → botão **Run workflow**. Sem terminal.
- O job instala Playwright, roda `baixar.py --todas` e `conferir.py`; sobe
  snapshots+relatório como artifact.
- Se exit 3: abre/atualiza **issue no GitHub do repositório** ("Conferidor:
  achados da semana AAAA-SS") com o relatório no corpo (`gh issue
  create/comment` via `GH_TOKEN`). Na F5 **não abre PR nem toca nos dados** —
  o PR automático dos achados mecânicos chega na F6 (5.10).
- Sentinela falhou (página velha na CI)? Falha o job com mensagem própria —
  pode ser o cache do Planalto para datacenter; reexecutar; se persistir,
  investigar fetch (F0 documenta alternativas).

### 5.10 (F6) PR automático para achados mecânicos

Fase firme (decisão do usuário, 29/07/2026), condicionada a alguns ciclos de
relatórios estáveis (precisão comprovada) antes de ligar. Escopo **estrito**:

- **Só UPDATE de linha existente** com correção inequívoca: moldura ou tipo de
  pena divergente do compilado. O gerador edita `data/crimes.json` (a fonte,
  nunca o derivado), reescreve o `obs` liderando pela faixa nova (armadilha
  nº 3), cria a entrada de changelog e abre PR citando o trecho do compilado.
  **Merge continua exigindo revisão humana** (competência jurídica) — como o
  roadmap já previa para o crawler.
- **Nunca ADD/REMOVE**: crime novo ou revogação exigem decisões de modelagem
  que não se automatizam com segurança (linha × modificador, equiparações,
  campos violencia/grave_ameaca/tentativa/acao, atribuição de id, hediondez,
  `resultado_morte`/`CORRECOES_MORTE`). Esses achados permanecem na issue, para
  uma sessão humana/IA aplicar como patch.
- Gates: CI completa no PR (`--estrito`, derivado sincronizado, typecheck,
  verificar, build) + checador de vigência (nunca propor mudança ainda não
  vigente) + no máximo um PR aberto por vez (não empilhar).

### 5.11 (F7) Watcher do DOU — sem IA — `scripts/crawler/dou_watcher.py`

Substitui o antigo "crawler do DOU" do roadmap. Filtro textual puro, acoplado ao
mesmo workflow semanal:

- **Fonte** (o spike da F7 escolhe): endpoint JSON `in.gov.br/leiturajornal`
  (sem autenticação) ou o INLABS (XML diário oficial, exige conta gratuita).
  Janela: os 8 dias anteriores à rodada, Seção 1.
- **Filtro** (norma é candidata se atende A ou B):
  - **A — citação de diploma monitorado**: regex gerada de `fontes.json`
    ("Lei nº 9.605", "Decreto-Lei nº 2.848", "Lei nº 11.340"…);
  - **B — vocabulário penal**: `reclusão`, `detenção`, `pena –`/`pena de`,
    `prisão simples`, `revoga`, `passa a vigorar acrescido`, `Código Penal`,
    `crime`. Só em atos normativos (Lei, LC, MP, Decreto-Lei) — ignora
    portarias/despachos, que dominam o volume.
- **Saída**: seção "DOU da semana — normas possivelmente penais" na issue do
  conferidor: norma, data, link e termos que casaram. **Nenhuma decisão
  automática** — é alerta de triagem humana.
- **Papel estratégico**: detectar lei penal **nova e autônoma** (diploma fora de
  `fontes.json`), o único caso invisível ao conferidor do compilado. Quando
  aparecer: humano adiciona a fonte nova em `fontes.json` e o conferidor passa a
  vigiá-la para sempre.
- Falsos positivos são aceitáveis e esperados (é um alerta semanal barato);
  falso negativo é o que se quer evitar — na dúvida, listar.

## 6. Armadilhas conhecidas (da revisão manual — TODAS viram teste ou regra)

| # | Armadilha | Mitigação no plano |
|---|---|---|
| 1 | Planalto serve página velha a cliente não interativo | Playwright + sentinela por fonte (5.1/5.2) |
| 2 | Rótulo pela lei criadora (`lei="Lei 14.811/24"` p/ artigo do CP) | `fontes.json.rotulos` + casar por artigo (5.5) |
| 3 | `obs` dita a moldura (vence `pena_min/max`) | comparar contra o DERIVADO (decisão 4) |
| 4 | Revogação total invisível na página da lei antiga | LexML + banner + envelhecimento (5.7) |
| 5 | Vacatio legis ("Vigência", "Produção de efeitos") | checador 5.6 |
| 6 | Versões sobrepostas sem strike (24-A Maria da Penha) | regra "anotação mais recente vence" + fixture |
| 7 | Encoding windows-1252 em páginas antigas | detecção de charset (5.2) |
| 8 | "dias-multa" contamina o parse do intervalo | já neutralizado no `parse_pena_range` — manter no módulo extraído |
| 9 | Pena só de teto ("até 6 meses") — min=0 legítimo | extrator 5.4; não acusar DIVERGENTE |
| 10 | Erros de ORIGEM no catálogo (Henry Borel 26, MP 24-A, CDC 73, falências 171/173/177, combustíveis 1º, CPM hediondos) | o differ pega crime/pena trocados; hediondez fica p/ auditoria própria (fora de escopo) |
| 11 | Formas "nas mesmas penas do caput" (equiparações) | herdar pena do caput no parser; conferir como linha se o catálogo modelou como linha |
| 12 | Aumentos "aumenta-se a pena de X" não são linha | fora do diff de linhas; listagem p/ triagem (5.5, modificadores) |

## 7. Estratégia de testes e gabarito

- **Fixtures congeladas** (F2): trechos representativos commitados —
  CP (art. 121 completo: sufixos, §§, revogados da L14.994), CPM (290 com §5º),
  Maria da Penha (24-A, versões sobrepostas), Lei 9.605 (art. 32 §§ novos),
  LCP art. 32 ("até"), CE (dias-multa), uma página windows-1252, Lei 7.802
  (revogação invisível). Pytest cobre parser, extrator e differ com elas.
- **Recall** (o conferidor ACHA o que sabemos que existiu): script de teste
  reverte em memória correções conhecidas do catálogo (ex.: devolve ao art.
  24-A a pena antiga 3m–2a; remove o art. 147-C) e exige que `conferir.py`
  aponte exatamente esses achados.
- **Precisão** (não inventa problema): rodar sobre o catálogo atual + exceções;
  meta: zero achados nos diplomas revisados nesta sessão (qualquer achado novo
  é ou bug do parser ou defasagem real — ambos valem investigar).
- CI de PR roda **apenas os testes com fixtures** (sem rede). O fetch vivo é só
  do workflow mensal.

## 8. Fases, critérios de aceite e orçamento

Cada fase é um PR pequeno e independente. "Barata?" = executável por sessão de
modelo menor com este arquivo como única briefing.

| Fase | Entrega | Critério de aceite | Esforço | Barata? |
|---|---|---|---|---|
| **F0** ✅ 29/07/2026 | Spike: fetch, charset, LexML, levantamento HTML | **Concluída** — `crawler/DECISOES-F0.md`: Playwright obrigatório (curl serve cópia pré-2018 da L11340), cp1252 padrão, anotações = links com href p/ lei+âncora, revogado total = corpo removido, LexML descartado | — | — |
| **F1** ✅ 30/07/2026 | `data/fontes.json` (62 fontes, 69 rótulos) + `baixar.py` + gitignore + `url_planalto` unificado | **Concluída** — 62/62 snapshots íntegros (sentinela válida), zero rótulo órfão, derivado **byte-idêntico**, sem dependências externas | — | — |
| **F2** ✅ 30/07/2026 | `parsear.py` + 5 fixtures + 18 testes + testes na CI | **Concluída** — art. 121 produz exatamente os 12 marcadores vigentes; 62/62 diplomas parseados sem falha (11.617 dispositivos, 1.149 com pena explícita, 116 revogados); sem dependências externas | — | — |
| **F3** | `pena_parser.py` extraído/estendido + `conferir.py` + relatório | Refactor byte-idêntico; recall e precisão da seção 7 passando; relatório legível gerado para o catálogo inteiro | 1–2 sessões | Sim, com F2 pronto |
| **F4** | `vigencia.py` + `revogacao.py` (banner; sem LexML) + exceções | Caso 15.190 (vacatio) detectado; caso 7.802 coberto por banner/watcher documentado em teste | 1 sessão | Sim |
| **F5** | `conferidor.yml` (cron semanal seg 05:00 BRT + dispatch) + issue automática + atualização do roadmap | Workflow roda no `workflow_dispatch` de ponta a ponta e abre issue de exemplo; roadmap v2.0.0 atualizado (compilado-first; DOU vira watcher) | 1 sessão | Sim |
| **F6** | PR automático p/ achados mecânicos (5.10) — só UPDATE, nunca ADD/REMOVE | PR de exemplo gerado com CI verde e corpo citando o compilado; limite de 1 PR aberto; merge segue humano | 1–2 sessões | Parcial |
| **F7** | Watcher do DOU sem IA (5.11) + **excluir este arquivo** | Rodada de teste lista as normas penais de uma semana conhecida (ex.: a semana da Lei 15.410/26); seção integrada à issue semanal | 1 sessão | Sim |

Total: ~9–12 sessões curtas. Ordem estrita F0→F5; F6 liga só após ciclos de
relatório com precisão comprovada; F7 pode rodar em paralelo à espera da F6.

## 9. Versionamento e contrato de dados

- F0–F5 **não alteram dados nem o site** → sem release obrigatória. Se quiser
  registrar, uma única entrada de changelog `melhoria` ("Conferidor automático
  de defasagem") ao final da F5, na release `1.Y.0` seguinte que houver.
- Correções que os relatórios apontarem: patches `1.2.Z` normais, **uma sessão
  = uma release** (ver memória do projeto).
- Nada de `revogado_em`/`fonte` no dataset nesta parte — isso é a v2.0.0, com
  os pré-requisitos do roadmap (v1.3.0 benefícios em dados; v1.4.0 acervo).

## 10. Instruções para a sessão executora

1. Ler este arquivo inteiro + `REVISAO-LEGISLATIVA.md` (lições) + memória
   `sispenas-defasagem-legislativa`.
2. Executar UMA fase por sessão (branch própria; commit pequeno; sem push/PR sem
   o usuário pedir — convenção do CLAUDE.md).
3. Ao terminar a fase: marcar os checkboxes abaixo, rodar a verificação padrão
   (`transform_data --estrito`, `typecheck`, `verificar`, `build` — nada pode
   quebrar mesmo sendo tooling), e atualizar a linha de status.
4. Na fase final (F7): excluir `PLANO-CRAWLER.md` **e `REVISAO-LEGISLATIVA.md`**
   (decisão do usuário, 29/07/2026 — o handoff da revisão manual vive até lá
   porque a F2 usa suas lições como casos de teste), mover o que for perene
   para `docs/` (se algo for), e registrar a conclusão na memória do projeto.
5. Fixture obrigatória da F2 (achado da F0): o HTML da Lei 11.340 deve vir do
   **navegador** (Playwright), nunca de curl — o CDN serve cópia pré-2018 a
   cliente HTTP.

### Status

- [x] F0 — spike de fetch/charset/LexML — **concluída em 29/07/2026**
      (`crawler/DECISOES-F0.md`)
- [x] F1 — fontes.json + fetcher — **concluída em 30/07/2026**
      (62/62 fontes íntegras; `python scripts/crawler/baixar.py --todas`)
- [x] F2 — parser estrutural + fixtures — **concluída em 30/07/2026**
      (`python -m pytest scripts/crawler/tests`)
- [ ] F3 — extrator de pena + differ + relatório
- [ ] F4 — vigência + revogação total
- [ ] F5 — automação CI (semanal, seg 05:00 BRT) + roadmap
- [ ] F6 — PR automático de achados mecânicos (após precisão comprovada)
- [ ] F7 — watcher do DOU sem IA + exclusão deste arquivo

**Achados da F2 a verificar na F3** (candidatos a erro de catálogo, encontrados
de passagem ao montar as fixtures — exigem conferência jurídica antes de virar
correção):
- **LCP art. 32**: a lei comina *"multa, de duzentos mil réis a dois contos de
  réis"*; o catálogo (id da LCP, art. 32) traz *"15 dias a 3 meses, prisão
  simples"*. Ou o registro pegou outro artigo, ou herdou pena de dispositivo
  vizinho. Conferir contra o compilado antes de mexer.
- **CP art. 121, § 2º-D**: o texto oficial tem erro de digitação — *"de 20
  (vinte) a 40 (quarenta anos)"*. Não afeta o catálogo, mas o extrator de pena
  precisa confiar nos algarismos, não no número por extenso.
- **Pena embutida na frase**: no CPM art. 290, § 5º, a pena está no corpo do
  parágrafo ("a pena será de reclusão de 5 a 15 anos"), sem linha "Pena –".
  O extrator da F3 tem de procurar no `texto` quando `pena_texto` for nulo.

**Última atualização:** 2026-07-30 — **F0, F1 e F2 CONCLUÍDAS.** F0 caracterizou o
HTML (anotações são links com href para lei+âncora; artigo revogado tem o corpo
removido; dispositivo alterado mantém a redação antiga **sem** riscado, valendo
a anotação mais recente; LexML descartado). F1 entregou `data/fontes.json`
(62 diplomas, 69 rótulos, zero órfão) e `scripts/crawler/baixar.py`: **62/62
fontes íntegras**, sem dependências externas, derivado byte-idêntico, e
`url_planalto()` do `transform_data` agora lê do mesmo registro (o mapa antigo
tinha 4 URLs 404). **Correção importante:** a tese "Playwright obrigatório" da
F0 caiu — era erro de decodificação (UTF-16 lido como cp1252); HTTP puro basta.
F2 entregou `parsear.py` (fatiamento do HTML cru, porque a árvore do Word
malformado desloca as fronteiras de parágrafo), 5 fixtures congeladas e 18
testes — inclusive o caso decisivo do art. 24-A, em que a redação de 2018
aparece antes da de 2024 sem riscado e o parser escolhe a mais recente.
Próxima fase: **F3** (extrator de pena + differ + relatório). O pipeline é 100%
determinístico — sem IA e sem consumo de tokens; o custo é só minutos de GitHub
Actions (gratuitos em repositório público).
