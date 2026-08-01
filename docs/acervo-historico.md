---
id: acervo-historico
title: Acervo histórico
sidebar_position: 3
---

{/* GERADO AUTOMATICAMENTE por scripts/gerar_completude.py — não edite à mão. */}

# Acervo histórico

Reunir **o que já foi crime no Brasil** — os tipos penais revogados, alterados e não recepcionados — é a [meta da v2.2.0](/docs/roadmap#v220--acervo-histórico), a ser executada **após** a completude dos tipos vigentes. A pergunta "o que deixou de ser crime, e quando?" é tão relevante para a pesquisa quanto "o que é crime hoje", e hoje nenhuma ferramenta a responde de forma estruturada.

A entrega será uma aba de pesquisa própria, separada da busca vigente para que nenhum tipo revogado contamine estatística de direito vigente, com uma tela por tipo mostrando o **texto original**, o que houve com ele (alteração, revogação ou não recepção), **quando** e por **qual dispositivo**.

## Diplomas revogados e não recepcionados já inventariados

Ponto de partida do acervo: os diplomas inteiros que saíram de vigência, registrados na [Fase 1](/docs/completude). Faltam ainda os tipos **revogados dentro de diplomas vigentes** (ex.: adultério, sedução, rapto no CP) e as **redações anteriores** alteradas.

| Diploma | Norma | O que houve |
|---|---|---|
| Agrotóxicos (antiga) | Lei nº 7.802, de 11 de julho de 1989 | revogado — Lei nº 14.785/2023, art. 65, I |
| Estatuto do Torcedor | Lei nº 10.671, de 15 de maio de 2003 | revogado — Lei nº 14.597/2023, art. 217, III |
| Lei de Segurança Nacional | Lei nº 7.170, de 14 de dezembro de 1983 | revogado — Lei nº 14.197/2021 (crimes contra o Estado Democrático, hoje CP arts. 359-I a 359-T) |
| Abuso de autoridade (antiga) | Lei nº 4.898, de 9 de dezembro de 1965 | revogado — Lei nº 13.869/2019 |
| Entorpecentes (antiga) | Lei nº 6.368, de 21 de outubro de 1976 | revogado — Lei nº 11.343/2006 |
| Lei de Imprensa | Lei nº 5.250, de 9 de fevereiro de 1967 | não recepcionado — ADPF 130 (STF, 2009) |
| Corrupção de menores (antiga) | Lei nº 2.252, de 1º de julho de 1954 | revogado — Lei nº 12.015/2009 (conduta hoje no ECA, art. 244-B) |
| Armas de fogo (antiga) | Lei nº 9.437, de 20 de fevereiro de 1997 | revogado — Lei nº 10.826/2003 |
| Licitações (antiga) | Lei nº 8.666, de 21 de junho de 1993 | revogado — Lei nº 14.133/2021 (crimes movidos para o CP, arts. 337-E a 337-P) |
| Falências (antiga) | Decreto-Lei nº 7.661, de 21 de junho de 1945 | revogado — Lei nº 11.101/2005 |
| Estatuto do Estrangeiro | Lei nº 6.815, de 19 de agosto de 1980 | revogado — Lei nº 13.445/2017, art. 124, I |

## Casos já identificados para o acervo

Dispositivos que saíram de vigência, foram alterados ou nunca vigoraram, encontrados durante a conferência do catálogo. São a semente do acervo — cada um receberá, na v2.2.0, uma entrada com o texto original e o histórico.

| Dispositivo | Categoria | O que houve |
|---|---|---|
| Lei 9.807/99, art. 19 (revelação de identidade de testemunha protegida) | vetado | Vetado na sanção da lei; nunca vigorou. O catálogo chegou a ter um registro indevido (id 1038), removido na v1.1.2. |
| CP, art. 240 (adultério) | revogado | Revogado pela Lei 11.106/2005. |
| CP, art. 217 (sedução) | revogado | Revogado pela Lei 12.015/2009. |
| CP, arts. 219 a 222 (rapto) | revogado | Revogados pela Lei 12.015/2009. |
| ECA, art. 233 (tortura de criança) | revogado | Revogado pela Lei 9.455/1997 (Lei de Tortura). **Constava como vigente no catálogo (id 742) até a v1.3.0.** |
| LCP, arts. 60 e 61 (mendicância e importunação ofensiva) | revogado | Revogados pelas Leis 11.983/2009 e 13.718/2018. |
| LCP, art. 27 (exploração da credulidade pública) | revogado | Revogado pela Lei 9.521/1997. |
| LCP, art. 39 (associação secreta) | revogado | Revogado pela Lei 14.197/2021. |
| LCP, art. 65 (perturbação da tranquilidade) | revogado | Revogado pela Lei 14.132/2021, que criou a perseguição (CP, art. 147-A). |
| LCP, art. 69 (atividade remunerada de estrangeiro) | revogado | Revogado pela Lei 6.815/1980. O compilado mantém o texto dos quatro artigos acima, com a revogação anotada ao lado — foi assim que a leva automática da v1.3.0 os tomou por vigentes. |

## Tipos retirados do catálogo por revogação

Estes eram crime, deixaram de ser, e ainda constavam entre os tipos vigentes — a conferência semanal contra o texto compilado os encontrou. Ficam aqui até que o acervo tenha estrutura própria (v2.2.0).

| Registro | id | Saiu em | Revogado por |
|---|---|---|---|
| CP, art. 150, §2º (violação de domicílio contra funcionário público) | 878 | v1.3.0 | Revogado pela Lei 13.869/2019 (Lei de Abuso de Autoridade). |
| CP, art. 185 (usurpação de nome ou pseudônimo alheio) | 159 | v1.3.0 | Revogado pela Lei 10.695/2003. |
| CP, art. 350 (exercício arbitrário ou abuso de poder) | 964 | v1.3.0 | Revogado pela Lei 13.869/2019 (Lei de Abuso de Autoridade). |
| ECA, art. 233 (tortura de criança ou adolescente) | 742 | v1.3.0 | Revogado pela Lei 9.455/1997 (Lei de Tortura). |
| LCP, arts. 27, 39, 65 e 69 (credulidade pública, associação secreta, perturbação da tranquilidade, atividade remunerada de estrangeiro) | 1649 a 1652 | v1.4.0 | Revogados pelas Leis 9.521/1997, 14.197/2021, 14.132/2021 e 6.815/1980. Os registros existiram por poucas horas, criados pela leva automática da v1.3.0. |

:::caution[As URLs desses registros deixaram de responder]
`id` é endereço público (`/pesquisa/tipos?tipo=N`), e esses saíram do ar com a remoção. Enquanto o acervo não tem página própria, esta tabela é o destino de quem chegar por um link antigo — e a v2.2.0 fará a rota apontar para o registro histórico, em vez de terminar em erro.
:::

:::note[Registro retirado por ERRO não entra no acervo]
O acervo reúne o que já foi crime no Brasil — é material de pesquisa sobre a lei, não a lista dos nossos enganos. Registro que saiu porque estava errado (duplicata, infração administrativa tomada por crime, texto de outro diploma transcrito) é descrito nas [notas da versão](/release-notes) em que saiu, e não aqui.
:::

