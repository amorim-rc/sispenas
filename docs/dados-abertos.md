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
  "derivado_auto": true,
  "pena_min_meses": 72,
  "pena_max_meses": 240,
  "pena_min_rotulo": "6 anos",
  "pena_max_rotulo": "20 anos",
  "pena_faixa_rotulo": "6 a 20 anos",
  "pena_unidade_derivada": true,
  "infracao_menor_potencial": false,

  "avaliavel": true,
  "motivo_nao_avaliavel": "",
  "resultado_morte": true,
  "resultado_morte_derivado": true,
  "perdao_judicial_previsto": false,
  "chave_dispositivo": "cp|art. 121, caput",
  "duplicata": false,
  "duplicata_divergente": false,
  "duplicata_ids": []
}
```

Penas (`pena_min`, `pena_max`, `pena_*_meses`) estão em **meses**. O primeiro bloco é a
fonte redigida à mão; os demais são derivados. Ver
[Catálogo de tipos penais](/docs/catalogo-tipos-penais) para o significado de cada campo.

### Campos que exigem atenção

| Campo | Por quê |
|---|---|
| `avaliavel` | **Filtre por `true` em qualquer estatística.** 22 registros são notas de referência e causas de aumento, com pena zero: incluí-los infla o alcance de todo benefício com teto de pena. |
| `duplicata_divergente` | 48 dispositivos aparecem duas vezes **com penas conflitantes**. O catálogo expõe a contradição em vez de escolher um valor. |
| `resultado_morte_derivado` | `true` = veio da heurística, sem revisão manual. |
| `id` | É **append-only** e serve de URL pública (`/pesquisa/tipos?tipo=N`). Nunca é reatribuído. |

## Relatório de qualidade

Cada regeneração emite [`/data/qualidade.json`](pathname:///sispenas/data/qualidade.json)
com o estado do catálogo — contagens, lacunas conhecidas e a lista completa das
contradições, com os `id` envolvidos. Use-o para saber o que é confiável antes de citar.

## Reprodutibilidade

Os campos derivados são gerados por `scripts/transform_data.py` a partir de
`data/crimes.json` (fonte), escrevendo o catálogo enriquecido em
`static/data/crimes.json`. O processo é determinístico: a mesma fonte produz sempre o
mesmo derivado, e a CI falha se o derivado commitado divergir da fonte.

## Estabilidade e versionamento

Os dados abertos são **API pública** para efeito de versionamento semântico: acrescentar
campo é MENOR, remover ou ressignificar campo é MAIOR. Ver
[Roadmap](/docs/roadmap#como-este-roadmap-usa-o-versionamento-semântico).

## Como citar

> Equipe SISPENAS. *SISPENAS — Sistema de Pesquisa de Tipos Penais e Benefícios*.
> Disponível em: https://github.com/amorim-rc/sispenas. Acesso em: [data].
