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
  "infracao_menor_potencial": false,

  "tem_pena_privativa": true,
  "sancoes_nao_privativas": [],
  "resultado_morte": true,
  "resultado_morte_derivado": true,
  "perdao_judicial_previsto": false,
  "chave_dispositivo": "cp|art. 121, caput",
  "duplicata": false,
  "duplicata_divergente": false,
  "duplicata_ids": []
}
```

Penas (`pena_min`, `pena_max`, `pena_*_meses`) estão em **meses** — o mês do art. 11 do
Código Penal tem 30 dias, então 0,5 são 15 dias. O primeiro bloco é a fonte redigida à
mão; os demais são calculados por `scripts/transform_data.py` a cada build.

## Para que serve cada campo

Nem todo campo tem o mesmo peso: alguns definem o que o sistema responde, outros
apenas descrevem. A tabela abaixo diz **onde cada um é usado**, para quem for reaproveitar
os dados saber o que pode mudar sem quebrar uma conta.

### Fonte — redigida à mão, é a autoridade

| Campo | Onde é usado |
|---|---|
| `id` | Endereço público do tipo (`/pesquisa/tipos?tipo=N`), citado em pareceres e trabalhos. **Nunca é reatribuído**: um id aposentado não volta a ser usado por outro crime. |
| `lei`, `artigo` | Identificam o dispositivo. Juntos formam a `chave_dispositivo`, que detecta registro repetido, e ligam a linha ao texto oficial conferido toda semana pelo conferidor. |
| `crime` | Nome exibido na busca. Também é dele — **e não do `obs`** — que se deduz o `resultado_morte`. |
| `pena_min`, `pena_max` | **A moldura.** Alimentam toda a dosimetria e todos os benefícios com limiar de pena (transação penal, ANPP, sursis, regime inicial, prescrição). Desde a v1.2.17 são a autoridade; antes disso a moldura era extraída do texto do `obs`, e uma frase secundária podia mudar a pena publicada. |
| `tipo_pena` | Reclusão, detenção, prisão simples ou nenhuma. Define o regime inicial e distingue o tipo sem pena privativa. |
| `acao` | Espécie de ação penal. Condiciona os institutos que dependem de representação ou de queixa. |
| `hediondo` | Fecha indulto, graça e comutação, e endurece as frações de progressão e livramento condicional. |
| `elemento` | Doloso, culposo ou preterdoloso. Crime culposo admite substituição por pena restritiva qualquer que seja a pena, e não admite tentativa. |
| `tentativa` | Habilita a redução do art. 14, II na terceira fase da dosimetria. |
| `violencia`, `grave_ameaca` | Vedam substituição por restritivas de direitos, ANPP e arrependimento posterior. |
| `obs` | **Descritivo.** Observação de leitura humana — origem da redação, formas do artigo, remissões. Não define a pena; o que dele ainda se extrai é a presença e o regime da multa. |

### Derivados — recalculados a cada build, não edite

| Campo | Para que existe |
|---|---|
| `pena_min_meses`, `pena_max_meses` | Moldura canônica para cálculo. |
| `pena_min_rotulo`, `pena_max_rotulo`, `pena_faixa_rotulo` | Exibição na unidade natural: "15 dias a 3 meses", "2 a 5 anos", "até 5 anos". |
| `pena_privativa`, `tem_pena_privativa`, `sancoes_nao_privativas` | Separam o tipo com pena de prisão daquele cuja sanção é outra (art. 28 da Lei 11.343/06). |
| `tem_multa`, `multa_regime` | Multa cumulativa, alternativa ou isolada, lida do `obs`. |
| `infracao_menor_potencial` | Pena máxima até dois anos — porta de entrada da Lei 9.099/95. |
| `resultado_morte`, `resultado_morte_derivado` | Marcam o tipo com morte como resultado; o segundo avisa que veio de heurística sobre o **nome** do crime, sem revisão manual. |
| `perdao_judicial_previsto` | Só é `true` nas hipóteses expressamente previstas em lei — não há perdão judicial genérico. |
| `chave_dispositivo`, `duplicata`, `duplicata_divergente`, `duplicata_ids` | Detecção de registro repetido. `duplicata_divergente` marcaria o mesmo dispositivo com penas conflitantes; **hoje não há nenhum**. |
| `derivado_auto` | Marca o registro cujos campos passaram por preenchimento automático. |

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
