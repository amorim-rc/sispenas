---
id: metodologia
title: Metodologia
sidebar_position: 2
---

# Metodologia

## Unidade de análise: o tipo penal

A unidade de análise é o
**tipo penal**: cada conduta com cominação de pena própria — incluindo formas simples,
qualificadas, privilegiadas, culposas, e cada inciso/alínea que gere pena autônoma.

O catálogo cobre o Código Penal, o Código Penal Militar, a Lei de Drogas, o Estatuto do
Desarmamento, o CTB, o ECA, a Lei Maria da Penha, os Crimes Ambientais e dezenas de
outros diplomas.

## Campos do catálogo

Cada tipo penal registra, entre outros: `lei`, `artigo`, `crime`, `pena_min` e
`pena_max` (em **meses**), `tipo_pena`, `acao`, `hediondo`, `elemento`, `tentativa`,
`violencia`, `grave_ameaca` e `obs`.

### Campos derivados automaticamente

Para viabilizar filtros combinados e o cálculo de benefícios, alguns campos são
**derivados por heurística** a partir do texto legal e das observações:

| Campo | Descrição | Como é derivado |
|-------|-----------|-----------------|
| `pena_privativa` | Reclusão, Detenção, Prisão simples ou Nenhuma | mapeado de `tipo_pena` |
| `tem_multa` | se há pena de multa (cumulativa, alternativa ou isolada) | regex sobre `obs` |
| `multa_regime` | `cumulativa` / `alternativa` / `isolada` / `nenhuma` | conectores no texto |
| `infracao_menor_potencial` | pena máxima ≤ 2 anos | `pena_max ≤ 24` |

:::warning Multa é uma dimensão independente
No Direito Penal brasileiro a multa é, na maioria dos casos, **cumulada** com a pena
privativa ("reclusão de 1 a 4 anos, **e multa**"). Por isso a multa é modelada como uma
dimensão **independente** (`tem_multa`), e não como um valor mutuamente exclusivo de
reclusão/detenção. Consequência prática: filtrar por **"Reclusão"** retorna também os
tipos com **reclusão + multa**. Para restringir apenas aos que têm multa, combine
"Reclusão" com o chip "Multa".
:::

Todos os campos derivados carregam a marca `derivado_auto: true` e serão revisados
individualmente. Correções manuais podem ser registradas em `CORRECOES` no
`scripts/transform_data.py` e regeneradas com `python3 scripts/transform_data.py`.

## Cálculo dos benefícios

Os benefícios são calculados por **funções puras** sobre um *cenário* (pena em abstrato,
pena concreta e características do réu/caso). O cálculo é **recalculado em tempo real** à
medida que o usuário altera qualquer parâmetro — inclusive a própria pena cominada, o que
permite **simular alterações legislativas**.

Os patamares legais adotados (limiares de 1, 2 e 4 anos; frações de progressão do
Art. 112 LEP; tabela de prescrição do Art. 109 CP; etc.) estão documentados em
[Benefícios penais](./beneficios-penais.md).
