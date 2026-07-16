---
id: catalogo-tipos-penais
title: Catálogo de tipos penais
sidebar_position: 2
---

# Catálogo de tipos penais

O catálogo é a base factual do SISPENAS: é dele que saem as penas cominadas, a hediondez,
a violência e as demais características que alimentam o cálculo dos benefícios. Esta
página descreve **como ele é estruturado, como é derivado e como sua qualidade é garantida
nele**.

## Os dois arquivos

O catálogo existe em duas formas, e a distinção importa para quem for contribuir:

| Arquivo | Papel | Quem edita |
|---|---|---|
| `data/crimes.json` | **Fonte da verdade.** Campos redigidos à mão. | Pessoas (inclusive pela interface web do GitHub) |
| `static/data/crimes.json` | **Derivado.** Fonte + campos calculados. É o único que a aplicação lê. | `scripts/transform_data.py` |

Nunca edite `static/data/crimes.json`: ele é sobrescrito. O workflow
`.github/workflows/regen-data.yml` observa `data/crimes.json`, roda a transformação e
commita o resultado — não é preciso ter Python instalado para contribuir.

```
data/crimes.json  ──►  scripts/transform_data.py  ──►  static/data/crimes.json
   (fonte, à mão)          (deriva + audita)              (consumido pelo site)
                                   │
                                   └──►  static/data/qualidade.json  (relatório)
```

## Campos da fonte

| Campo | Descrição |
|---|---|
| `id` | Identificador estável. É o que aparece em `?tipo=N` na URL. |
| `lei` | Diploma (`CP`, `CTB`, `Lei 11.343/06`…). |
| `artigo` | Dispositivo (`Art. 121, §2º, I`). |
| `crime` | Nome do tipo penal. |
| `pena_min` / `pena_max` | Pena cominada **em meses**. |
| `tipo_pena` | `Reclusão`, `Detenção`, `Prisão simples`, `Multa`. |
| `acao` | Ação penal (pública incondicionada, condicionada, privada). |
| `hediondo` | `Sim` / `Não` — inclui os **equiparados** (tráfico, tortura, terrorismo). |
| `elemento` | `Doloso`, `Culposo`, `Preterdoloso`. |
| `tentativa` | O tipo admite tentativa? |
| `violencia` / `grave_ameaca` | Elementares que vedam vários benefícios. |
| `obs` | Texto livre com a descrição legal. É de onde a pena é parseada. |

## Campos derivados

Gerados por `scripts/transform_data.py`. **Todos são heurísticos** e sujeitos a revisão.

| Campo | Como é derivado |
|---|---|
| `pena_privativa` | Mapeado de `tipo_pena`. |
| `tem_multa`, `multa_regime` | Regex sobre `obs` (`e multa` → cumulativa; `ou multa` → alternativa). |
| `pena_min_meses`, `pena_max_meses` | Parser de intervalos (`"15 dias a 6 meses"`, `"1-5 anos"`), com fallback para `pena_min`/`pena_max`. O mês vale 30 dias (art. 11, CP). |
| `pena_*_rotulo`, `pena_faixa_rotulo` | Exibição na unidade natural. |
| `infracao_menor_potencial` | `pena_max_meses <= 24` **e** pena > 0. |
| `tem_pena_privativa` | O tipo comina prisão? Se não, declara `sancoes_nao_privativas`. |
| `resultado_morte` | Regex sobre o **nome** do tipo (art. 112, VI e VIII, LEP). |
| `perdao_judicial_previsto` | Lista curada de dispositivos (art. 107, IX, CP). |
| `chave_dispositivo`, `duplicata`, `duplicata_divergente` | Detecção de registros repetidos. |
| `duplicata_tipo` | `pena` · `identidade` · `hediondez` — o tipo do defeito (ver abaixo). |

### `tem_pena_privativa` — e por que o catálogo só tem tipos penais

Até a v1.1.0 o catálogo carregava, além dos tipos penais, **notas de referência e
dispositivos sem pena própria**: `REFERÊNCIA — A LGPD não tipifica crimes`, `CP, Art. 141,
I` (causa de aumento), `CP, Art. 171, §5º` (regra de ação penal), `CP, Art. 128` (excludente
de ilicitude). Eram 21 registros com pena zero.

Com pena zero, eles **satisfaziam qualquer teto de pena** e eram contados como "cabíveis"
em transação penal, ANPP e sursis — inflando o alcance desses benefícios. A transação
reportava 325 tipos cabíveis; o correto era 303.

Foram removidos, e a regra passou a ser **imposta** pelo transformador: um registro que não
declare pena nem sanção falha o build (convenção C1, no `CONTRIBUTING.md`).

Sobra uma distinção legítima: **tipo penal que não comina prisão**. Hoje é só o art. 28 da
Lei 11.343/06 (porte para consumo), cujas sanções são as do art. 28, I a III — advertência,
prestação de serviços e medida educativa. Ele é tipo penal, fica no catálogo, declara
`sancoes_nao_privativas` e recebe `tem_pena_privativa: false`, que o mantém fora das
estatísticas de alcance (que se medem por patamar de pena) sem excluí-lo da consulta.

:::note[Majorantes com pena própria são exibidas]
As causas de aumento que constituem um **dispositivo com pena própria** — como o roubo
majorado (art. 157, §2º) — são tipos do catálogo e aparecem normalmente na busca. O que
não entra é a causa de aumento **abstrata**, que só diz "aumenta-se de 1/3" sobre a pena
de *outro* crime, sem patamar próprio (ex.: art. 141, aumento nos crimes contra a honra):
como registro de pena zero, ela distorceria as estatísticas de alcance. Essas majorantes
abstratas serão modeladas como **entidade própria** na 3ª fase da dosimetria (art. 68, CP),
prevista para a v3.0.0.
:::

### `resultado_morte` — por que só o nome do tipo

A regex roda **apenas contra o nome do tipo**, nunca contra `obs`. O campo `obs` costuma
descrever a pena de *outros parágrafos* do mesmo artigo ("se resulta morte, triplica"), o
que produziria falsos positivos em tipos cujo caput não é qualificado pela morte — como o
art. 135 (omissão de socorro), o art. 267 (epidemia dolosa) e o art. 270 (envenenamento).

O campo importa porque o art. 112, VI e VIII, da LEP reserva as frações de 50% e 70% ao
condenado por **crime hediondo com resultado morte**, e o art. 122, §2º, lhe veda a saída
temporária.

### `perdao_judicial_previsto` — por que uma lista curada

Não existe perdão judicial genérico: ele só incide **onde a lei o prevê expressamente** e
**não se estende por analogia**. Por isso o campo não é inferido do elemento culposo, e
sim de uma lista de dispositivos mantida em `PERDAO_JUDICIAL`, no script de transformação.
Onde a lei restringe o perdão à modalidade culposa, a regra exige `elemento == "Culposo"`
— o art. 121, §4º, por exemplo, tem uma 1ª parte culposa e uma 2ª parte dolosa, e só a
primeira o admite.

## Garantias de qualidade

A cada regeneração, o script emite `static/data/qualidade.json` com o estado do catálogo,
e a CI o valida antes de qualquer publicação.

| Indicador | Valor |
|---|---|
| Tipos penais | 1.006 |
| Com pena privativa | 1.005 |
| Sem pena privativa | 1 (art. 28 da Lei 11.343/06, sanções próprias) |
| Dispositivos distintos | 872 |
| **Contradições internas** | **0** |

### Contradições: zeradas e travadas

Uma contradição interna ocorreria se dois registros do mesmo dispositivo (`lei + artigo`)
divergissem em pena ou hediondez. **Não há nenhuma** — todas foram conferidas contra o
texto compilado do Planalto. O transformador as classificava em três tipos (`pena`,
`identidade`, `hediondez`) por um **coeficiente de sobreposição** de vocabulário, e esse
classificador segue ativo como guarda: a CI roda
`transform_data.py --estrito --max-contradicoes=0` e **falha se uma nova contradição
entrar**. O catálogo não pode regredir.

### O que a CI garante a cada mudança

- **Só tipos penais** (convenção C1): notas de referência, agravantes e excludentes não
  entram.
- **Toda sanção declarada** (C2) e **`id` append-only** (C3): a URL pública nunca aponta
  para o crime errado.
- **Zero contradições** (C4) e derivado sincronizado com a fonte.
- **Casos-âncora de direito penal** (`npm run verificar`): 22 benefícios × 1.005 tipos.

## Como corrigir um tipo penal

1. Edite `data/crimes.json` — direto pela interface do GitHub, se preferir.
2. Abra um Pull Request descrevendo a fonte legal da correção.
3. A CI valida; ao integrar, o `regen-data` regenera o derivado automaticamente.

Correções finas que a heurística não acerta ficam em tabelas explícitas no
`scripts/transform_data.py` (`CORRECOES`, `CORRECOES_MORTE`), com o motivo documentado —
assim a exceção sobrevive à próxima regeneração.
