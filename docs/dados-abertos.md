---
id: dados-abertos
title: Dados abertos
sidebar_position: 4
---

# Dados abertos

O catálogo completo é publicado como dado aberto em formato JSON:

- **Arquivo:** [`/data/crimes.json`](pathname:///sispenas/data/crimes.json)
- **Licença:** MIT com atribuição — cite como **"Equipe SISPENAS"**.

## Esquema de cada registro

```json
{
  "id": 1,
  "lei": "CP",
  "artigo": "Art. 121, caput",
  "crime": "Homicídio simples",
  "pena_min": 72,
  "pena_max": 240,
  "tipo_pena": "Reclusão",
  "acao": "Pública Incondicionada",
  "hediondo": "Não",
  "elemento": "Doloso",
  "tentativa": "Sim",
  "violencia": "Sim",
  "grave_ameaca": "Não",
  "obs": "Matar alguém. 6-20 anos reclusão",
  "pena_privativa": "Reclusão",
  "tem_multa": false,
  "multa_regime": "nenhuma",
  "infracao_menor_potencial": false,
  "derivado_auto": true
}
```

Penas (`pena_min`, `pena_max`) estão em **meses**.

## Reprodutibilidade

Os campos derivados são gerados por `scripts/transform_data.py` a partir de
`data/crimes.json` (fonte), escrevendo o catálogo enriquecido em
`static/data/crimes.json`.

## Como citar

> Equipe SISPENAS. *SISPENAS — Sistema de Pesquisa de Tipos Penais e Benefícios*.
> Disponível em: https://github.com/amorim-rc/algo-pen. Acesso em: [data].
