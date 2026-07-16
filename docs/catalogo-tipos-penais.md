---
id: catalogo-tipos-penais
title: Catálogo de tipos penais
sidebar_position: 2
---

# Catálogo de tipos penais

O catálogo é a base factual do SISPENAS: é dele que saem as penas cominadas, a hediondez,
a violência e as demais características que alimentam o cálculo dos benefícios. Esta
página descreve **como ele é estruturado, como é derivado e o que ainda não é confiável
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

:::note[Causas de aumento voltarão]
As majorantes removidas não são lixo — são parte da 3ª fase da dosimetria (art. 68, CP).
Elas voltam como **entidade própria** na v3.0.0, não como tipos penais.
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

## Qualidade: o que ainda não é confiável

A cada regeneração, o script emite `static/data/qualidade.json` com o estado do catálogo.
**Estes números são conhecidos e não estão resolvidos:**

| Indicador | Valor | Significado |
|---|---|---|
| Tipos penais | 1.039 | Total no arquivo |
| Com pena privativa | 1.038 | Entram nas estatísticas de alcance |
| Sem pena privativa | 1 | Art. 28 da Lei 11.343/06 (sanções próprias) |
| **Dispositivos distintos** | **862** | O catálogo tem menos dispositivos do que registros |
| Registros duplicados | 353 | Mesmo `lei + artigo` em mais de um registro |
| **Duplicatas divergentes** | **42** | Cópias do mesmo dispositivo **com penas ou hediondez diferentes** |

:::danger[Contradições internas]
42 dispositivos aparecem duas vezes **com dados conflitantes**. Exemplos:

- `CP, Art. 127` — 16 a 64 meses **vs.** 24 a 120 meses
- `CP, Art. 151, §1º, I` — 1 a 6 meses **vs.** 6 a 24 meses

Não é possível saber qual versão está correta sem revisão jurídica artigo a artigo. Até
lá, **ambas são exibidas** e sinalizadas como duplicata — o SISPENAS prefere expor a
contradição a escolher silenciosamente um dos valores. A resolução é prioridade da
v1.1.Z — ver [Conferência integral](/docs/roadmap#conferência-integral-do-catálogo).
:::

A CI roda `python3 scripts/transform_data.py --estrito --max-contradicoes=42`, que **falha
se o número de contradições aumentar**. O catálogo pode melhorar, não piorar.

### Outras lacunas conhecidas

- **Hipóteses de perdão judicial sem tipo correspondente** no catálogo (art. 140, §1º;
  art. 176, par. único; CTB art. 291 c/c CP 121, §5º). Listadas em
  `perdao_judicial_sem_tipo`, no relatório de qualidade.
- **Concurso de crimes** (material, formal, continuidade) não é modelado: cada tipo é
  avaliado isoladamente.
- **Causas de aumento e diminuição** não compõem a pena calculada — a dosimetria parte da
  pena cominada no caput do dispositivo registrado.
- Parte dos campos ainda é `derivado_auto` e não passou por revisão individual.

## Como corrigir um tipo penal

1. Edite `data/crimes.json` — direto pela interface do GitHub, se preferir.
2. Abra um Pull Request descrevendo a fonte legal da correção.
3. A CI valida; ao integrar, o `regen-data` regenera o derivado automaticamente.

Correções finas que a heurística não acerta ficam em tabelas explícitas no
`scripts/transform_data.py` (`CORRECOES`, `CORRECOES_MORTE`), com o motivo documentado —
assim a exceção sobrevive à próxima regeneração.
