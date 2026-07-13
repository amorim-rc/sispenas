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

## Aviso

Ferramenta destinada à **pesquisa e simulação**. Os cálculos simplificam controvérsias
e **não constituem aconselhamento jurídico**. Parte dos dados foi derivada
automaticamente do texto legal e será revisada individualmente.

## Licença

**MIT com atribuição** à **Equipe SISPENAS**. Veja [`LICENSE`](./LICENSE).
