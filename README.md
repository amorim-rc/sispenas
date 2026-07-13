# SISPENAS

**Sistema de Pesquisa de Tipos Penais e Benefícios** — ferramenta aberta de pesquisa de
políticas públicas para estudar o **impacto dos benefícios penais** sobre os tipos penais
brasileiros.

Construído em **Docusaurus 3 + React + TypeScript**. Catálogo de **1.061 tipos penais**
de 65 diplomas legislativos.

## Recursos

- Busca por **nome, artigo, lei ou observações**.
- Filtros combinados: **modalidade de pena** (reclusão, detenção, prisão simples, multa),
  hediondez, elemento subjetivo, violência/grave ameaça, ação penal, menor potencial
  ofensivo.
  - A multa é uma **dimensão independente**: filtrar por "Reclusão" inclui os tipos com
    reclusão **+ multa**; combine com "Multa" para restringir.
- Seleção de um tipo penal com **cálculo dinâmico dos benefícios penais** (ANPP, transação,
  suspensão do processo, substituição por PRD, sursis, regime inicial, progressão,
  livramento, prescrição, saída temporária, detração, remição, indulto).
- **Simulação de alteração legislativa**: ajuste a pena e veja, em tempo real, quais
  benefícios se tornam cabíveis ou incabíveis.

## Instalação

```bash
npm install
```

## Desenvolvimento

```bash
npm run start      # servidor local com hot-reload
```

## Build de produção

```bash
npm run build
npm run serve      # testar o build localmente
```

## Dados

O catálogo-fonte fica em `data/crimes.json`. Os campos derivados
(`pena_privativa`, `tem_multa`, `multa_regime`, `infracao_menor_potencial`) são gerados por:

```bash
python3 scripts/transform_data.py
```

O script grava o catálogo enriquecido em `static/data/crimes.json` (consumido pelo site).
Correções manuais podem ser registradas em `CORRECOES`, no próprio script.

## Documentação

A documentação (Sobre, Metodologia, Benefícios penais, Dados abertos, Roadmap) fica em
`docs/` e é publicada dentro do próprio site.

## Origem e proposta original × implementação atual

O SISPENAS foi concebido em 2008 pelas professoras **Maíra Rocha Machado** e **Marta
Rodriguez de Assis Machado** (Direito GV/FGV), em pesquisa vinculada a edital da Secretaria
de Assuntos Legislativos do Ministério da Justiça:

> MACHADO, Maíra Rocha; MACHADO, Marta Rodriguez de Assis (coord.). **SISPENAS: Sistema de
> Consulta sobre Crimes, Penas e Alternativas à Prisão**. Revista Jurídica, Brasília, v. 10,
> n. 90, ed. esp., p. 1-26, abr./maio 2008. (Íntegra em
> [`static/artigos/`](./static/artigos/machado-machado-2008-sispenas-rev-juridica-90.pdf).)

O artigo original define os objetivos, o modelo de dados e a metodologia do sistema. Esta
implementação **preserva a intuição central** (catalogar tipos penais e cruzá-los com
benefícios, permitindo simular alterações legislativas) e a **atualiza**. Comparação:

| Aspecto | Proposta original (2008) | Esta implementação |
|---|---|---|
| **Arquitetura** | Software com servidor: Apache + **PHP + PostgreSQL**, com CRUD, controle de acesso e fluxo de aprovação (papéis administrador/alimentador/usuário); código entregue ao Ministério da Justiça | Site **estático** (Docusaurus 3 + React + TS) sobre **JSON**, publicável no GitHub Pages, sem servidor/banco; sem CRUD nem papéis |
| **Unidade "tipo"** | Conduta + circunstâncias com cominação própria; um artigo é desmembrado em várias unidades; inclui **"tipos mistos"** (margens de majorantes/minorantes pré-calculadas em abstrato) | Mesmo conceito de tipo por artigo/parágrafo, exposto via **"tipos correlatos"**; **não** gera sistematicamente os "tipos mistos" calculados (lacuna) |
| **Tamanho do catálogo** | **1.529** tipos (CP + 37 leis especiais) | **1.061** tipos (subconjunto; roadmap visa ~1.688) |
| **Pena (armazenamento)** | Cadastrada **em dias** (1 mês = 30 dias, 1 ano = 360 dias); exibida em anos/meses | Canônica **em meses**; exibida na **unidade natural** (dias/meses/anos), com conversão automática |
| **Multa** | Critério com conectores **"E" / "E/OU" / "OU"** (cumulativa/alternativa/isolada) | Dimensão independente: `tem_multa` + `multa_regime` (`cumulativa`/`alternativa`/`isolada`/`nenhuma`), espelhando os conectores |
| **Critérios "em abstrato"** | 9: pena mín., pena máx., tipo de prisão, multa, violência, grave ameaça, hediondo, elemento subjetivo, vedação específica | Mesmos critérios como filtros; acrescenta ação penal e menor potencial ofensivo |
| **Benefícios** | Composição civil, transação, suspensão do processo, substituição por PRD/multa, sursis (2-4 e 4-6 anos), limite de cumprimento (30 anos), livramento (1/3, 1/2, 2/3), regime inicial | Conjunto **atualizado à lei vigente**: **ANPP** (Lei 13.964/2019), transação, suspensão do processo, substituição por PRD, sursis, regime inicial, **progressão**, livramento, **prescrição**, **saída temporária**, **detração**, **remição**, **indulto** |
| **Consultas cruzadas** | Dois sentidos: tipo → benefícios **e** benefício → tipos atingidos | Sentido **tipo → benefícios** implementado com recálculo dinâmico; benefício → tipos é aproximado pelos filtros (ainda não é tela dedicada) |
| **Simulação** | Entidades "simuladas" **persistidas** e marcadas no banco, para projetos de lei | Simulação **efêmera** na tela (sliders de pena mín./máx./concreta + circunstâncias); nada é persistido |
| **Atualização dos dados** | Cadastro manual por "alimentadores", com aprovação | Carga inicial via planilha + IA; manutenção por **scraper do DOU** ou IA; humanos só fazem ajustes finos |
| **Critérios concretos** | Ex.: reincidência exibida como "critério não-generalizável" (descritivo) | Circunstâncias concretas (primariedade, reincidência, confissão, etc.) entram na simulação e alteram os resultados |

### Por que as decisões diferentes

- **Estático em vez de PHP/PostgreSQL:** o objetivo aqui é uma ferramenta de pesquisa
  pública, versionada em Git e publicável no GitHub Pages, sem custo de servidor/banco. O
  preço disso é abrir mão de CRUD, papéis de usuário e do fluxo de aprovação do original —
  substituídos por um pipeline de dados (planilha/IA → `data/crimes.json` → build).
- **Pena em meses + exibição natural:** o original armazenava tudo em dias por limitação
  técnica; aqui a conversão dias/meses/anos é automática e a exibição usa a unidade natural
  ("15 dias", "1 a 4 anos"), evitando leituras confusas.
- **Conjunto de benefícios atualizado:** o artigo é de 2008 e antecede a **ANPP** e outras
  mudanças (ex.: limite de cumprimento hoje é de 40 anos). O motor foi reescrito para a
  legislação atual; alguns institutos do original (composição civil, limite de cumprimento)
  ainda não têm card próprio e podem ser reincorporados.
- **Simulação efêmera:** para uso exploratório imediato, a simulação acontece na tela sem
  necessidade de gravar "tipos simulados", como fazia o sistema original voltado ao
  Ministério da Justiça.

### Lacunas conhecidas em relação ao original

- Cobertura do catálogo (1.061 vs 1.529) e geração de "tipos mistos" (majorantes/minorantes).
- Tela dedicada de **benefício → tipos atingidos** (as tabelas de alcance do artigo).
- Institutos ainda sem card: composição civil dos danos e limite de cumprimento de pena.

## Aviso

Ferramenta destinada à **pesquisa e simulação**. Os cálculos simplificam controvérsias
e **não constituem aconselhamento jurídico**. Parte dos dados foi derivada
automaticamente do texto legal e será revisada individualmente.

## Licença

**MIT com atribuição** à **Equipe SISPENAS**. Veja [`LICENSE`](./LICENSE).
