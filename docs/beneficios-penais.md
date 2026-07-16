---
id: beneficios-penais
title: Benefícios penais
sidebar_position: 3
---

# Benefícios penais modelados

O SISPENAS modela os **22 benefícios** abaixo. Todos os valores de pena são tratados em
**meses**. A implementação é para fins de pesquisa e simplifica controvérsias.

## Como o catálogo é modelado

Desde a v1.1.0, cada benefício é um **registro declarativo** (`BeneficioDef`), e não uma
regra embutida no código. O registro reúne:

- **metadados** — nome, fundamento legal, categoria e *natureza*;
- **requisitos** e **vedações**, com citação do dispositivo ou súmula;
- **parâmetros editáveis** — cada patamar, fração ou vedação é um dado, com valor padrão
  extraído da legislação vigente e o dispositivo de origem;
- uma **função pura de avaliação**, que lê os parâmetros em vez de constantes.

Essa separação é o que permite a **Busca por benefício**: alterar um patamar recalcula o
catálogo inteiro de tipos penais sem tocar no código. É também o passo preparatório para
mover o catálogo de benefícios para JSON versionado (roadmap, v1.2.0).

### Natureza do benefício

A *natureza* indica de qual pena o benefício depende — e determina se a busca reversa é
exata ou presumida:

| Natureza | Significado | Busca por benefício |
|----------|-------------|---------------------|
| **Pena em abstrato** | Depende da pena cominada no tipo | Avaliação **exata** |
| **Pena concreta** | Depende da pena fixada na sentença | Exige **pena concreta presumida** |
| **Independe da pena** | Não há patamar (detração, remição) | Alcança todo o catálogo |

:::note Pressuposto metodológico da busca reversa
A pena concreta **não é atributo do tipo penal**. Para varrer o catálogo, o sistema presume
uma pena concreta — por padrão, a **pena mínima cominada** (hipótese do réu condenado no
mínimo legal, a mais favorável e a de uso corrente na pesquisa empírica). A base pode ser
trocada por pena máxima ou por um valor fixo aplicado a todos os tipos.
:::

## Benefícios processuais (pena em abstrato)

| Benefício | Fundamento | Critério objetivo |
|-----------|-----------|-------------------|
| **Transação penal** | Art. 76, Lei 9.099/95 | Pena máxima ≤ 2 anos (menor potencial ofensivo) |
| **Suspensão condicional do processo** | Art. 89, Lei 9.099/95 | Pena mínima ≤ 1 ano |
| **ANPP** | Art. 28-A, CPP | Pena mínima < 4 anos, sem violência/grave ameaça, confissão |
| **Colaboração premiada** | Art. 4º, Lei 12.850/13 | Redução de até 2/3 ou perdão judicial; até 1/2 se posterior à sentença |

## Aplicação da pena

| Benefício | Fundamento | Critério objetivo |
|-----------|-----------|-------------------|
| **Substituição por PRD** | Art. 44, CP | Pena ≤ 4 anos, sem violência/grave ameaça (doloso); culposo sempre |
| **Sursis da pena** | Art. 77, CP | Pena ≤ 2 anos (comum); ≤ 4 anos (etário/humanitário) |
| **Regime inicial** | Art. 33, §2º, CP | > 8 anos fechado; > 4 e ≤ 8 semiaberto; ≤ 4 aberto |
| **Perdão judicial** | Art. 107, IX, CP | Só nas hipóteses expressas em lei (em regra, culposas) |
| **Arrependimento posterior** | Art. 16, CP | Sem violência/grave ameaça + reparação até o recebimento da denúncia → redução de 1/3 a 2/3 |
| **Desistência voluntária e arrependimento eficaz** | Art. 15, CP | Tipo que admita tentativa; responde só pelos atos praticados |

## Execução penal

| Benefício | Fundamento | Critério |
|-----------|-----------|----------|
| **Progressão de regime** | Art. 112, LEP | Frações de 16% a 70% conforme reincidência/hediondez/resultado morte |
| **Livramento condicional** | Art. 83, CP | 1/3 (primário), 1/2 (reincidente), 2/3 (hediondo); vedado reincidente específico hediondo |
| **Prescrição** | Art. 109, CP | Tabela por pena (abstrata e concreta) |
| **Saída temporária** | Art. 122, LEP | Regime semiaberto; 1/6 (primário) ou 1/4 (reincidente); vedada em hediondo com resultado morte (Lei 14.843/2024) |
| **Detração** | Art. 42, CP | Desconto de prisão provisória (qualitativo) |
| **Remição** | Art. 126, LEP | Trabalho (1 dia/3) e estudo (1 dia/12h); +1/3 por conclusão de curso |
| **Prisão domiciliar** | Art. 117, LEP; art. 318, CPP | Hipóteses humanitárias; HC 143.641/SP (gestantes e mães) |
| **Monitoração eletrônica** | Art. 146-B, LEP; art. 319, IX, CPP | Saída temporária, domiciliar ou cautelar diversa da prisão |
| **Indulto coletivo** | Art. 84, XII, CF | Decreto anual; vedado a hediondos/equiparados |
| **Comutação de penas** | Art. 84, XII, CF; art. 192, LEP | Indulto parcial: reduz a pena remanescente |
| **Graça (indulto individual)** | Art. 84, XII, CF; art. 188, LEP | Clemência individual; vedada a hediondos/equiparados |
| **Unificação de penas** | Art. 75, CP | Teto de cumprimento de 40 anos; Súmula 715, STF |

## Frações da progressão de regime (Art. 112 LEP)

| Inciso | Situação | Fração |
|--------|----------|--------|
| I | Primário, sem violência/grave ameaça | 16% |
| II | Reincidente, sem violência/grave ameaça | 20% |
| III | Primário, com violência/grave ameaça | 25% |
| IV | Reincidente, com violência/grave ameaça | 30% |
| V | Primário, hediondo/equiparado | 40% |
| VI | Primário, hediondo com resultado morte (livramento vedado) | 50% |
| VII | Reincidente, hediondo | 60% |
| VIII | Reincidente específico, hediondo com resultado morte | 70% |

## Tabela de prescrição (Art. 109 CP)

| Pena | Prazo prescricional |
|------|--------------------|
| Superior a 12 anos | 20 anos |
| Superior a 8 e até 12 anos | 16 anos |
| Superior a 4 e até 8 anos | 12 anos |
| Superior a 2 e até 4 anos | 8 anos |
| De 1 a 2 anos | 4 anos |
| Inferior a 1 ano | 3 anos |

:::note
Reduções e aumentos (Art. 115 — metade para menor de 21 na data do fato ou maior de 70
na sentença; Art. 110 — aumento de 1/3 para reincidente na executória) são indicados nos
detalhes de cada resultado.
:::
