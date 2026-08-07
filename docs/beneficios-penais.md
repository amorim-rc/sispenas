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

:::note[Pressuposto metodológico da busca reversa]
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
| **Progressão de regime** | Art. 112, LEP | Frações de 16% a 85% conforme reincidência/hediondez/resultado morte |
| **Livramento condicional** | Art. 83, CP | 1/3 (primário), 1/2 (reincidente), 2/3 (hediondo); vedado ao reincidente específico em hediondo e nas quatro hipóteses do art. 112 da LEP |
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
| *caput* | Regra geral — **1/6 da pena no regime anterior** | 16,67% |
| I | Primário, com violência/grave ameaça, **salvo Título XII** | 25% |
| II | Reincidente, com violência/grave ameaça, **salvo Título XII** | 30% |
| III | Reincidente em crime diverso dos dos incisos I e II | 20% |
| IV | Reincidente, com violência/grave ameaça — **sem** a ressalva do Título XII (redação de 2019; a nova foi vetada) | 30% |
| V | Primário, hediondo/equiparado | 70% |
| VI, "a" | Primário, hediondo com resultado morte (livramento vedado) | 75% |
| VI, "b" | Comando de organização criminosa **ultraviolenta** estruturada para crime hediondo (livramento vedado) | 75% |
| VI, "c" | Constituição de milícia privada | 75% |
| VI, "d" | Primário, feminicídio (livramento vedado) | 75% |
| VII | Reincidente, hediondo | 80% |
| VIII | Reincidente específico, hediondo com resultado morte (livramento vedado) | 85% |
| IX e X | *(vetados — nunca existiram)* | — |

Os incisos V a VIII vêm da **Lei 15.358/2026**, que também acrescentou a alínea "d", pôs
"ultraviolenta" e a vedação do livramento na alínea "b" e revogou o inciso VI-A. O *caput*
e os incisos I a III vêm da **Lei 15.402/2026**, de 08/05/2026.

**Quatro incisos vedam o livramento condicional na própria letra** — VI, "a", "b" e "d",
e VIII. A vedação é regra de cálculo do motor, não apenas texto de nota.

### Duas tabelas, com corte pela data do fato

A Lei 15.402/2026 não é uniformemente mais benéfica. Para o **primário condenado por
crime sem violência**, a hipótese saiu do inciso I (16%) e passou a cair no *caput*
(1/6 = **16,67%**): a lei nova é mais **gravosa** para esse grupo e, portanto, **não
retroage** (CF, art. 5º, XL; CP, art. 2º, parágrafo único). A retroatividade da lei mais
benéfica apura-se **por situação concreta**, não em bloco.

| Perfil | Fato até 07/05/2026 | Fato a partir de 08/05/2026 |
|---|---|---|
| Primário, sem violência | 16% da pena (inciso I de 2019) | 1/6 da pena no regime anterior (*caput*) |
| Reincidente, sem violência | 20% (inciso II de 2019) | 20% (inciso III) |
| Primário, com violência | 25% (inciso III de 2019) | 25% (inciso I) |
| Reincidente, com violência | 30% (inciso IV de 2019) | 30% (inciso II) |
| Título XII, primário | 25% ou 30% conforme violência | 1/6 pelo *caput* |

Marque **"fato anterior a 08/05/2026"** na simulação para calcular pela tabela do Pacote
Anticrime.

:::note[A base de cálculo do *caput* não é a dos incisos]
O *caput* conta **1/6 da pena no regime anterior**; os incisos contam percentual **da
pena total**. São operações distintas dentro do mesmo artigo. Na **primeira** progressão
as duas bases coincidem, e é ela que o sistema calcula; nas seguintes, a base do *caput*
é o remanescente. Progressão sucessiva não é modelada.
:::

:::note[Título XII — o critério é topográfico]
Os incisos I e II ressalvam "os crimes previstos no Título XII da Parte Especial do
Código Penal" — arts. 359-A a 359-T, contra o Estado Democrático de Direito. A ressalva
**não pergunta se houve violência**: o art. 359-L (abolição violenta) e o art. 359-M
(golpe de Estado) são violentos por definição típica e ainda assim entram. Para o
primário sobra o *caput*, por exclusão expressa.

Para o **reincidente** há duas leituras sustentáveis, e o sistema devolve o resultado
como *condicional*, com as duas escritas: pelo **inciso III** (20%), porque os crimes do
Título XII estão fora do alcance de I e II e são portanto "diversos" deles; ou pelo
***caput*** (16,67%), porque "crimes referidos nos incisos I e II" significaria crimes
violentos, categoria a que eles materialmente pertencem. A diferença é de 3,33 pontos, e
é matéria que os tribunais de execução vão fixar.
:::

:::warning[O inciso IV, e o que o veto fez com ele]
A Lei 15.402/2026 **propôs redação nova para os incisos IV a X** — e **todos os
sete foram vetados**. O que sobra, no texto consolidado, é: o inciso IV na redação
de 2019 (30% para o reincidente em crime com violência ou grave ameaça, **sem** a
ressalva do Título XII), os incisos V a VIII na redação da Lei 15.358/2026, e os
incisos IX e X como "(VETADO)".

Isso importa porque o inciso IV passou a repetir o conteúdo do novo inciso II — e
a sobrevivência dele **não é descuido de técnica legislativa**: é o resultado
deliberado do processo de veto. O argumento de revogação tácita, que essa
sobreposição sugeriria, fica enfraquecido, e abre-se uma terceira leitura para o
reincidente em crime violento do Título XII: ele cairia no inciso IV, que não o
ressalva, a 30%.

**O sistema não escolhe.** Para o reincidente em crime do Título XII o resultado
sai como *condicional*, com as leituras concorrentes escritas. A escolha depende
das razões do veto aos incisos IV a X e de pronunciamento do STJ ou do STF, e
enquanto não houver um nem outro, calcular pelo *caput* — o mais favorável ao
apenado — é o que o catálogo pode afirmar.
:::

:::note[Sob controle de constitucionalidade]
Contra a Lei 15.402/2026 tramitam as **ADIs 7966, 7967, 7968 e 7969**, por vício formal
na apreciação do veto e por inconstitucionalidade material. **Não há cautelar com eficácia
*erga omnes***: o que houve, em 09/05/2026, foi o afastamento pontual da lei em oito
Execuções Penais. A lei está em vigor e o catálogo a aplica — não aplicá-la estenderia ao
catálogo inteiro uma restrição que existe em oito processos. Reconferir o andamento das
quatro ações antes de citar o dado.
:::

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
