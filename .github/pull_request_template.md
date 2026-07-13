## Descrição

<!-- O que muda e por quê. -->

## Tipo de mudança

- [ ] Atualização do catálogo (planilha → `data/crimes.json`)
- [ ] Correção fina de derivação (`CORRECOES` em `scripts/transform_data.py`)
- [ ] Motor de benefícios (`src/lib/beneficios.ts`)
- [ ] Interface / documentação
- [ ] Infra / CI

## Checklist

- [ ] Alterei **apenas** `data/crimes.json` (fonte); o `static/data/crimes.json` é gerado.
- [ ] Regenerei o derivado: rodei `python3 scripts/transform_data.py` **ou** deixei o workflow
      "Regenerar dados derivados" cuidar disso ao entrar na `main`.
- [ ] `npm run typecheck` passa.
- [ ] `npm run build` passa.
- [ ] Para mudanças de catálogo: `pena_min_meses ≤ pena_max_meses` e `id` únicos.

## Observações de revisão

<!-- Pontos que precisam de conferência jurídica, se houver. -->
