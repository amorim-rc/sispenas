# Dosimetria Penal Brasil — Especificações Técnicas v2

## Visão Geral

Sistema de dosimetria penal e catálogo exaustivo de tipos penais brasileiros, com dupla vocação: **prática forense** (advogados criminalistas) e **pesquisa de políticas públicas** (acadêmicos, legisladores). Inspirado no SISPENAS (Machado & Machado, 2008) e expandido com cobertura legislativa atualizada e ferramentas de cálculo automatizado.

---

## Roadmap

| Versão | Descrição | Status |
|--------|-----------|--------|
| **v1** | Planilha Google Sheets + Apps Script. Catálogo unitário (529 tipos) + granularizado (822 tipos de 62 diplomas). Dosimetria trifásica, progressão, prescrição, concurso, geração de textos jurídicos | **Concluída** |
| **v2** | GitHub Pages — site estático servindo dados curados em JSON. Interface web com busca, filtros, cálculos. CI/CD com workflows de validação de dados. `.xlsx` gerado automaticamente pela CI | **Próxima** |
| **v2.5** | Crawler automatizado do DOU + agente IA (Claude/GPT) que identifica alterações na legislação penal e propõe atualizações via Pull Request, com esteira de CI monitorada por pessoa com competência jurídica e técnica | Planejada |
| **v3** | Sistema web completo com API REST pública, autenticação, histórico de alterações legislativas, busca avançada com NLP | Planejada |
| **v4** | Plataforma integrada: prática forense + pesquisa de políticas públicas. Simulação de alteração legislativa, cruzamento exaustivo de tipos com benefícios, dados abertos para pesquisa acadêmica, dashboards analíticos | Planejada |

---

## Arquitetura v2 — GitHub Pages

### Estrutura de Diretórios

```
dosimetria-penal-brasil/
│
├── index.html                          # Página principal — busca e navegação
├── catalogo.html                       # Catálogo granularizado — tabela interativa
├── dosimetria.html                     # Calculadora de dosimetria trifásica
├── progressao.html                     # Calculadora de progressão de regime
├── prescricao.html                     # Calculadora de prescrição
├── sobre.html                          # Sobre o projeto, créditos, metodologia
│
├── data/
│   ├── crimes.json                     # Fonte de verdade — catálogo granularizado completo
│   ├── crimes_unitarios.json           # Catálogo unitário (tipo base + qualificadoras descritivas)
│   ├── legislacao.json                 # Metadados dos diplomas (nome completo, data, ementa, status)
│   ├── beneficios.json                 # Tabela de benefícios penais (ANPP, sursis, etc.)
│   ├── agravantes_atenuantes.json      # Circunstâncias judiciais, agravantes, atenuantes
│   ├── progressao.json                 # Frações de progressão (Art. 112 LEP)
│   ├── prescricao.json                 # Tabela de prescrição (Art. 109 CP)
│   └── changelog.json                  # Histórico de alterações no banco de dados
│
├── dist/
│   └── dosimetria_penal.xlsx           # Planilha gerada automaticamente pela CI a partir dos JSONs
│
├── js/
│   ├── app.js                          # Inicialização, roteamento, estado global
│   ├── catalogo.js                     # Busca, filtros, paginação, ordenação do catálogo
│   ├── dosimetria.js                   # Cálculo trifásico (Art. 68 CP)
│   ├── progressao.js                   # Progressão, livramento, regime inicial
│   ├── prescricao.js                   # Prescrição abstrata, retroativa, marcos
│   ├── concurso.js                     # Concurso de crimes (material, formal, continuado)
│   ├── gerador-texto.js                # Geração de textos jurídicos fundamentados
│   ├── db.js                           # Carregamento e indexação dos JSONs
│   └── utils.js                        # Funções utilitárias (formatação, validação)
│
├── css/
│   ├── style.css                       # Estilos principais
│   └── print.css                       # Estilos para impressão de petições
│
├── scripts/
│   ├── validate_data.py                # Validação: penas dentro do intervalo, referências cruzadas
│   ├── generate_xlsx.py                # Gera .xlsx a partir dos JSONs
│   ├── json_from_py.py                 # Converte catalogo_granularizado.py → crimes.json
│   └── stats.py                        # Gera estatísticas para o changelog
│
├── .github/
│   └── workflows/
│       ├── validate.yml                # CI: valida dados a cada push/PR
│       ├── build.yml                   # CI: gera .xlsx, deploya no GitHub Pages
│       ├── crawler.yml                 # v2.5: crawler DOU (cron semanal)
│       └── ai-update.yml              # v2.5: agente IA propõe atualizações via PR
│
├── LICENSE                             # Licença do projeto
├── README.md                           # Documentação principal
├── CONTRIBUTING.md                     # Guia de contribuição
├── METHODOLOGY.md                      # Metodologia de catalogação
└── CHANGELOG.md                        # Histórico de versões
```

### Banco de Dados — Escolha Técnica

**Formato escolhido: JSON estático**

Para GitHub Pages (site 100% estático, sem servidor), as opções de "banco de dados" são:

| Opção | Prós | Contras | Veredicto |
|-------|------|---------|-----------|
| **JSON** | Nativo do JS, sem dependências, versionável no Git, facilmente validável, suporta estruturas aninhadas | Carregamento integral na memória | **Escolhido para v2** |
| CSV/TSV | Simples, editável em planilha | Sem tipagem, sem aninhamento, parsing manual | Descartado |
| SQLite (sql.js/WASM) | Queries SQL reais no browser | ~1 MB de biblioteca, complexo, lento no carregamento inicial | Reservado para v3 |
| IndexedDB | Persistência local, bom para cache | API complexa, sem portabilidade, não é fonte de verdade | Auxiliar (cache) |

**Estratégia de performance para ~2.000 tipos:**

1. **Carregamento**: `crimes.json` (~500 KB gzipped para ~2.000 tipos) carregado uma vez via `fetch()` no `app.js`
2. **Indexação em memória**: `db.js` cria índices (`Map`) por lei, artigo, hediondo, violência para buscas O(1)
3. **Busca full-text**: Implementação leve de busca por substring normalizada (sem acentos, lowercase) — sem necessidade de biblioteca externa para o volume atual
4. **Paginação virtual**: Para a tabela do catálogo, renderização de apenas ~50 linhas visíveis (virtual scrolling) para performance em dispositivos móveis
5. **Cache local**: `localStorage` com versionamento — se o JSON não mudou (hash), usa cache local

### Estrutura do `crimes.json`

```json
{
  "version": "2.0.0",
  "generated_at": "2026-06-07T18:00:00Z",
  "stats": {
    "total_tipos": 822,
    "total_diplomas": 62,
    "hediondos": 79,
    "com_violencia": 182,
    "com_grave_ameaca": 89
  },
  "crimes": [
    {
      "id": "cp-121-caput",
      "lei": "CP",
      "lei_completa": "Decreto-Lei 2.848/1940 (Código Penal)",
      "artigo": "Art. 121, caput",
      "crime": "Homicídio simples",
      "pena_min_meses": 72,
      "pena_max_meses": 240,
      "tipo_pena": "Reclusão",
      "acao_penal": "Pública Incondicionada",
      "hediondo": false,
      "elemento_subjetivo": "Doloso",
      "tentativa": true,
      "violencia": true,
      "grave_ameaca": false,
      "cabe_anpp": false,
      "cabe_sursis_processual": false,
      "cabe_sursis_pena": false,
      "observacoes": "6-20 anos reclusão. Bem jurídico: vida.",
      "tags": ["vida", "pessoa", "parte-especial", "titulo-i"],
      "atualizado_em": "2026-06-07",
      "fonte_atualizacao": null
    }
  ]
}
```

### Estrutura do `legislacao.json`

```json
{
  "diplomas": [
    {
      "sigla": "CP",
      "nome_completo": "Decreto-Lei 2.848, de 7 de dezembro de 1940",
      "ementa": "Código Penal",
      "data_publicacao": "1940-12-07",
      "status": "vigente",
      "ultima_alteracao": "Lei 14.994/2024",
      "url_planalto": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
      "total_tipos_catalogados": 422,
      "observacoes": "Parte Especial: Arts. 121-361. Parte Geral: Arts. 1-120."
    }
  ]
}
```

---

## Workflows de CI/CD

### 1. `validate.yml` — Validação de Dados (a cada push/PR)

```yaml
name: Validar Dados
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install jsonschema
      - run: python scripts/validate_data.py
```

**Regras de validação (`validate_data.py`):**

1. **Integridade estrutural**: Todo crime deve ter todos os 16 campos obrigatórios
2. **Penas válidas**: `pena_min > 0` e `pena_max >= pena_min` (exceto referências com `pena_min = 0`)
3. **Consistência de benefícios**:
   - `cabe_anpp = true` somente se `pena_min < 48` (4 anos) E `violencia = false` E `grave_ameaca = false`
   - `cabe_sursis_processual = true` somente se `pena_min <= 12` (1 ano)
   - `cabe_sursis_pena = true` somente se `pena_max <= 24` (2 anos) para simples, ou `pena_max <= 48` para etário/humanitário
4. **Hediondos**: Cruzamento com o rol taxativo da Lei 8.072/90 atualizada
5. **Duplicatas**: Nenhum par `(lei, artigo)` repetido
6. **Referência legislativa**: Toda `lei` deve existir em `legislacao.json`
7. **Formato de artigo**: Regex `Art\. \d+(-[A-Z])?` para padronização

### 2. `build.yml` — Build e Deploy

```yaml
name: Build e Deploy
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install openpyxl
      - run: python scripts/generate_xlsx.py
      - run: python scripts/stats.py
      - uses: actions/upload-artifact@v4
        with:
          name: dosimetria-penal
          path: dist/dosimetria_penal.xlsx
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### 3. `crawler.yml` — Crawler do DOU (v2.5)

```yaml
name: Crawler DOU
on:
  schedule:
    - cron: '0 8 * * 1'  # Segunda-feira às 8h UTC
  workflow_dispatch:
jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install requests beautifulsoup4 openai
      - run: python scripts/crawler_dou.py
      - run: |
          if git diff --quiet data/crimes.json; then
            echo "Nenhuma alteração detectada"
          else
            git checkout -b update/dou-$(date +%Y%m%d)
            git add data/
            git commit -m "feat: atualização automática via DOU $(date +%Y-%m-%d)"
            git push origin HEAD
            gh pr create --title "Atualização automática — DOU $(date +%Y-%m-%d)" \
              --body "Alterações detectadas pelo crawler. Revisão humana necessária." \
              --label "auto-update,needs-review"
          fi
```

**Funcionamento do crawler (v2.5):**

1. Acessa a API do DOU (Diário Oficial da União) e busca publicações na seção de legislação penal
2. Filtra por palavras-chave: "código penal", "crimes", "pena", "reclusão", "detenção", "hediondo", etc.
3. Envia o texto extraído para um agente IA (Claude/GPT) com o prompt: "Identifique se esta publicação altera algum tipo penal existente ou cria novos tipos. Se sim, gere as entradas JSON correspondentes."
4. Compara com `crimes.json` atual e propõe alterações via PR
5. **A PR NÃO é mergeada automaticamente** — requer revisão de pessoa com competência jurídica e técnica

---

## Interface Web v2

### Páginas

**1. Catálogo Granularizado (`catalogo.html`)**
- Tabela interativa com todas as 16 colunas
- Filtros por: lei, hediondo, violência, grave ameaça, tipo de pena, ação penal, elemento subjetivo
- Busca full-text por nome do crime, artigo ou observações
- Ordenação por qualquer coluna
- Exportação para CSV/PDF
- Destaque visual: rosa (hediondo), laranja (violência/ameaça), cinza (referência)

**2. Calculadora de Dosimetria (`dosimetria.html`)**
- Seleção do crime via dropdown com busca (alimentado pelo JSON)
- Preenchimento automático de pena mín/máx ao selecionar o crime
- 1ª fase: 8 circunstâncias judiciais (Art. 59) com toggles favorável/desfavorável
- 2ª fase: agravantes/atenuantes com checkboxes
- 3ª fase: causas de aumento/diminuição com frações editáveis
- Resultado: pena definitiva + regime inicial + benefícios aplicáveis
- Botão "Gerar Justificativa" → texto jurídico fundamentado (HTML/PDF)

**3. Progressão de Regime (`progressao.html`)**
- Inputs: pena definitiva, data de início, tipo de crime, réu primário/reincidente
- Cálculo automático de todas as frações (16%-70%)
- Timeline visual com datas estimadas de: progressão, livramento, término
- Remição por trabalho e estudo

**4. Prescrição (`prescricao.html`)**
- Inputs: pena em abstrato ou concreta, idade do réu, marcos interruptivos (datas)
- Cálculo de prescrição abstrata e retroativa
- Redução Art. 115 (menoridade/senilidade)
- Verificação automática entre marcos

### Tecnologias Frontend

- **HTML5 + CSS3 + JavaScript vanilla** — sem frameworks (simplicidade, zero build, rápido no GitHub Pages)
- **Alternativa avaliada**: Se a complexidade crescer, migrar para Alpine.js (8 KB) ou Preact (3 KB) — não React/Vue/Angular (overhead desnecessário para site estático)
- **Responsividade**: CSS Grid + Flexbox, mobile-first
- **Acessibilidade**: WAI-ARIA, contraste WCAG 2.1 AA, navegação por teclado
- **Impressão**: CSS `@media print` otimizado para petições e relatórios

---

## Modelo de Dados — Evolução por Versão

| Campo | v1 (Sheets) | v2 (JSON) | v3 (API) | v4 (Plataforma) |
|-------|-------------|-----------|----------|-----------------|
| id único | Não | Sim | Sim | Sim |
| Lei | Sim | Sim | Sim (FK) | Sim (FK) |
| Artigo | Sim | Sim | Sim | Sim |
| Crime | Sim | Sim | Sim | Sim |
| Pena mín/máx | Sim | Sim | Sim | Sim |
| Tipo de pena | Sim | Sim | Sim | Sim |
| Ação penal | Sim | Sim | Sim | Sim |
| Hediondo | Sim | Sim | Sim | Sim |
| Elemento subjetivo | Sim | Sim | Sim | Sim |
| Tentativa | Sim | Sim | Sim | Sim |
| Violência | Sim | Sim | Sim | Sim |
| Grave ameaça | Sim | Sim | Sim | Sim |
| Cabe ANPP | Sim | Sim (auto) | Sim (auto) | Sim (auto) |
| Cabe sursis proc. | Sim | Sim (auto) | Sim (auto) | Sim (auto) |
| Cabe sursis pena | Sim | Sim (auto) | Sim (auto) | Sim (auto) |
| Observações | Sim | Sim | Sim | Sim |
| Tags/categorias | Não | Sim | Sim | Sim |
| Histórico alterações | Não | changelog.json | Sim (tabela) | Sim (timeline) |
| Benefícios (12 SISPENAS) | 3 | 3 | 12 | 12 |
| Simulação legislativa | Não | Não | Não | Sim |
| Jurisprudência vinculada | Texto livre | Texto livre | Estruturado | Estruturado + busca |

---

# README.md

# Dosimetria Penal Brasil

**Sistema de dosimetria penal, progressão de regime e catálogo exaustivo de tipos penais da legislação brasileira.**

Dupla vocação: **prática forense** (advogados criminalistas) e **pesquisa de políticas públicas** (acadêmicos e legisladores).

---

## O que é

Uma ferramenta completa para:

- **Consultar** todos os tipos penais brasileiros — granularizados por variante (simples, qualificado, privilegiado, culposo, com aumento, etc.), cada um com seu intervalo de pena próprio
- **Calcular** a dosimetria da pena pelo sistema trifásico do Art. 68 do Código Penal (pena-base, agravantes/atenuantes, causas de aumento/diminuição)
- **Estimar** progressão de regime (Art. 112 LEP, com as frações do Pacote Anticrime), livramento condicional, prescrição e outros benefícios
- **Gerar** textos jurídicos fundamentados (petições de progressão, livramento, alegação de prescrição, excesso de prazo)
- **Filtrar e analisar** crimes por lei, hediondice, presença de violência/grave ameaça, tipo de pena, ação penal, elemento subjetivo

## Cobertura Atual

| Métrica | Valor |
|---------|-------|
| Tipos penais granularizados | 822 |
| Diplomas legislativos | 62 |
| Crimes hediondos catalogados | 79 |
| Crimes com violência como elementar | 182 |
| Crimes com grave ameaça como elementar | 89 |

**Legislação coberta** (seleção): Código Penal, Código Penal Militar, Lei de Drogas (11.343/06), Estatuto do Desarmamento (10.826/03), CTB, Lei de Crimes Ambientais (9.605/98), Lei de Tortura (9.455/97), Lei de Organização Criminosa (12.850/13), Lei de Lavagem de Dinheiro (9.613/98), Crimes Tributários (8.137/90), Sistema Financeiro (7.492/86), Racismo (7.716/89), Abuso de Autoridade (13.869/19), ECA, Estatuto do Idoso (10.741/03), Licitações (14.133/21), CDC, Biossegurança (11.105/05), Transplantes (9.434/97), Crimes Falimentares (11.101/05), e mais 40+ diplomas.

**Atualizações recentes incluídas**: Feminicídio como crime autônomo (Lei 14.994/2024), fraude eletrônica (Lei 14.155/2021), fraude com criptomoedas (Lei 14.478/2022), injúria racial equiparada a racismo (Lei 14.532/2023), Lei Henry Borel (Lei 14.344/2022), golpe de Estado (Lei 14.197/2021), bullying/cyberbullying (Lei 14.811/2024), Lei Sansão — maus-tratos a cão/gato (Lei 14.064/2020).

## Como Usar

### v2 (GitHub Pages) — em breve
Acesse o site e use diretamente no navegador. Sem instalação, sem cadastro, sem custo.

### v1 (Planilha)
1. Baixe o arquivo `dosimetria_penal.xlsx` da pasta `dist/`
2. Importe no Google Sheets (Arquivo → Importar → Upload)
3. Abra o Apps Script (Extensões → Apps Script)
4. Cole o conteúdo de `dosimetria_apps_script.js`
5. Salve e atualize a planilha (F5)
6. O menu "Dosimetria Penal" aparece na barra superior

## Metodologia

Cada tipo penal é catalogado seguindo a metodologia granularizada do SISPENAS (Machado & Machado, 2008): cada variante de um artigo (simples, qualificado, privilegiado, culposo, com causa de aumento, com causa de diminuição) constitui uma entrada autônoma com intervalo de pena próprio.

**Critério de "tipo"**: uma combinação de conduta + circunstâncias que gera uma cominação de pena distinta no texto legal. Ex: Art. 121, caput (homicídio simples: 6-20 anos) e Art. 121, §2º, I (homicídio qualificado por motivo torpe: 12-30 anos) são dois tipos distintos.

**16 campos por tipo**: Lei, Artigo, Crime, Pena Mín (meses), Pena Máx (meses), Tipo de Pena, Ação Penal, Hediondo, Elemento Subjetivo, Tentativa, Violência, Grave Ameaça, Cabe ANPP, Cabe Sursis Processual, Cabe Sursis Pena, Observações.

## Roadmap

| Versão | O que | Quando |
|--------|-------|--------|
| **v1** | Planilha + Apps Script funcional | Concluída |
| **v2** | GitHub Pages — site estático com dados em JSON, busca, filtros, cálculos no browser, CI/CD com validação de dados | Em desenvolvimento |
| **v2.5** | Crawler automatizado do DOU + agente IA para detectar alterações legislativas e propor atualizações via PR, com esteira de qualidade monitorada por pessoa com competência jurídica e técnica | Planejada |
| **v3** | Sistema web com API REST pública, banco de dados relacional, histórico de alterações, busca com NLP | Planejada |
| **v4** | Plataforma integrada: prática forense + pesquisa de políticas públicas. Simulação de alteração legislativa ("se a pena do crime X mudar para Y, quais benefícios passam a ser aplicáveis?"), cruzamento com 12 benefícios penais, dados abertos para pesquisa acadêmica | Planejada |

## Referências

- MACHADO, Maíra Rocha; MACHADO, Marta Rodriguez de Assis. **SISPENAS — Sistema de consulta sobre crimes, penas e alternativas à prisão**. Revista Jurídica da Presidência, v. 10, n. 90, Ed. Esp., p. 01-26, abr./maio 2008.
- BRASIL. **Decreto-Lei 2.848/1940** (Código Penal) e legislação penal esparsa.
- BRASIL. **Lei 13.964/2019** (Pacote Anticrime).

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instruções sobre como contribuir com novos tipos penais, correções ou funcionalidades.

Toda contribuição que adicione ou altere dados de tipos penais deve:
1. Citar a fonte legislativa (artigo e diploma)
2. Passar nos workflows de validação da CI
3. Ser revisada por pessoa com conhecimento jurídico

## Autor

**Luccas Cavicchioli**
Filósofo (UFPE) | Estudante de Direito | Profissional de tecnologia

---

# LICENSE

```
MIT License

Copyright (c) 2026 Luccas Cavicchioli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Resumo da licença**: Uso totalmente livre. Pode copiar, modificar, distribuir, usar comercialmente. A única exigência é manter a atribuição de autoria (copyright notice) nas cópias.

---

# CONTRIBUTING.md (rascunho)

## Como Contribuir

### Adicionando tipos penais

1. Faça fork do repositório
2. Edite `data/crimes.json` seguindo o schema existente
3. Garanta que cada novo tipo tenha:
   - `lei`: sigla do diploma (deve existir em `legislacao.json`)
   - `artigo`: no formato `Art. XXX, §Yº, Z` (padronizado)
   - `crime`: nome do tipo penal (nomen juris) — descritivo e único
   - `pena_min_meses` e `pena_max_meses`: em meses (inteiros positivos)
   - Todos os 16 campos preenchidos
4. Execute `python scripts/validate_data.py` localmente
5. Abra um Pull Request com a fonte legislativa citada

### Reportando erros

Se encontrar um erro em pena, classificação ou artigo, abra uma Issue com:
- O tipo penal afetado (lei + artigo)
- O valor incorreto e o valor correto
- A fonte legislativa que comprova a correção

### Código de conduta

Este é um projeto de interesse público. Contribuições devem priorizar precisão jurídica sobre velocidade.

---

# METHODOLOGY.md (rascunho)

## Metodologia de Catalogação

### Definição de "tipo penal"

Adotamos a definição granularizada do SISPENAS: cada combinação de **conduta + circunstâncias** que gera uma **cominação de pena distinta** no texto legal constitui um tipo penal autônomo.

**Exemplo — Art. 121 CP (Homicídio):**

| Tipo | Artigo | Pena | Entrada autônoma? |
|------|--------|------|-------------------|
| Homicídio simples | Art. 121, caput | 6-20 anos reclusão | Sim |
| Homicídio privilegiado | Art. 121, §1º | 6-20 anos (redução 1/6 a 1/3) | Sim |
| Homicídio qualificado (motivo torpe) | Art. 121, §2º, I | 12-30 anos reclusão | Sim |
| Homicídio qualificado (motivo fútil) | Art. 121, §2º, II | 12-30 anos reclusão | Sim |
| Homicídio culposo | Art. 121, §3º | 1-3 anos detenção | Sim |
| Feminicídio | Art. 121-A | 20-40 anos reclusão | Sim |

### Fontes

- Texto legal vigente: planalto.gov.br
- Alterações: DOU (Diário Oficial da União)
- Classificação de hediondo: Lei 8.072/90 atualizada
- Referência acadêmica: SISPENAS (Machado & Machado, 2008)

### Campos booleanos

- **Hediondo**: `true` somente se o crime consta no rol taxativo da Lei 8.072/90 (ou equiparados: tortura, tráfico, terrorismo)
- **Violência**: `true` se violência física é elementar do tipo (ex: roubo, lesão corporal). Não inclui violência como qualificadora opcional
- **Grave ameaça**: `true` se grave ameaça é elementar do tipo
- **Tentativa**: `true` se o crime admite tentativa (plurissubsistente). `false` para crimes unissubsistentes, habituais, culposos, omissivos próprios e preterdolosos
- **Cabe ANPP**: calculado automaticamente — `pena_min < 48 meses` E `violencia = false` E `grave_ameaca = false` (Art. 28-A CPP)
- **Cabe Sursis Processual**: `pena_min <= 12 meses` (Art. 89, Lei 9.099/95)
