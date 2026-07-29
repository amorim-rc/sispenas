# Revisão de defasagem legislativa — estado e método

Documento de continuidade da **revisão do catálogo contra o texto compilado
oficial** (`planalto.gov.br`). Objetivo: encontrar e corrigir a defasagem do
catálogo frente às leis penais recentes (2023+). Atualizado em **2026-07-29**.

> Acuidade jurídica é o valor central: dado errado publicado é pior que dado
> ausente. Nada entra sem conferência contra o texto compilado.

## Método (validado ao longo de v1.2.2–v1.2.10)

**Revisar POR LEI-REFORMA, não diploma a diploma.** Poucas leis recentes explicam
quase toda a defasagem, e cada uma tocou vários diplomas.

1. **Ler a lei-reforma na fonte.** O texto da lei lista, em "A Lei X passa a
   vigorar…", **todos os diplomas que ela alterou**. Isso evita varrer 60 diplomas.
2. **Separar penal de não-penal.** Boa parte das alterações é processual (CPP,
   LEP, competência) — fora do catálogo, que só cataloga **tipos penais**.
3. **Cruzar com o catálogo casando por NÚMERO DE ARTIGO em TODOS os rótulos.**
4. **Classificar (rigor do art. 121):** o que fixa pena própria vira **linha**;
   o que "aumenta a respectiva pena" vira **modificador** de dosimetria; regras de
   concurso/procedimento não entram.
5. **Conferir no navegador**, nunca por cliente não interativo — o Planalto serve
   página desatualizada a `WebFetch`/curl.

### Armadilhas que já custaram erro

- **Rótulo pela lei criadora.** Artigos do CP inseridos por lei recente vêm com
  `lei="Lei 14.811/24"`, não `"CP"`. Casar por artigo em todos os rótulos, nunca
  filtrar `lei==CP`.
- **O `obs` dita a moldura.** `transform_data` deriva a moldura via
  `parse_pena_range(obs)`, que VENCE os campos `pena_min/max`. O `obs` deve
  liderar pela faixa correta e não conter faixa numérica secundária.
- **`jaEmbutida`** suprime modificador cujo dispositivo está no mesmo artigo do
  crime. Para aumentos que não são linha (org. criminosa), usar `ignora_embutida`.
- **Fração > 1** (dobro=1, triplo=2): a 3ª fase admite em aumentos; validador
  aceita até 3 quando `fase==3 && natureza=='aumento'`.
- **Rótulos divididos.** Escopo de modificador aceita UM rótulo. Se o diploma
  está sob dois (ex.: `Lei 7.716/89` e `... (atualiz.)`), unificar antes.

## O que já está FECHADO

| Escopo | Versões |
|---|---|
| **CP — Parte Especial** (completo, art. por art.) | v1.2.2 – v1.2.6 |
| **Lei 15.358/26** (org. criminosa) → Drogas, Desarmamento | v1.2.7 |
| **Lei 15.163/25** (exposição a perigo) → Idoso, PcD | v1.2.8 |
| **ECA** (leis 14.811/24 e 15.234/25) | v1.2.9 |
| **Lei de Racismo** (Lei 14.532/23, padrão CP) | v1.2.10 |
| **Ambiental** (Lei 9.605/98 — reformas 2024-2026) | v1.2.11 |
| **Abuso de autoridade** (Lei 13.869/19 — sem reforma 2023+; achado o art. 15-A) | v1.2.11 |
| **Sistema financeiro** (Lei 7.492/86 — triado, sem defasagem) | — (sem alteração) |
| **Ordem tributária** (Lei 8.137/90 — agravante do art. 12, LC 224/25) | v1.2.11 |
| **CTB** (Lei 9.503/97 — terminologia "sinistro", Lei 14.599/23) | v1.2.11 |
| **Esporte** (Lei 14.597/23 — triado, sem defasagem penal) | — (sem alteração) |
| **Organizações criminosas** (Lei 12.850/13 — obstrução, Lei 15.245/25) | v1.2.11 |
| **Henry Borel** (Lei 14.344/22 — art. 26 estava com crime/pena errados) | v1.2.11 |
| **Maria da Penha** (Lei 11.340/06 — art. 24-A: pena e §4º atualizados) | v1.2.11 |
| **CDC** (Lei 8.078/90 — sem reforma 2023+; erro de origem no art. 73) | v1.2.11 |
| **Falências** (Lei 11.101/05 — sem reforma 2023+; erros de origem nos arts. 171/173/177) | v1.2.11 |

> **Uma sessão = uma release.** Toda a revisão da cauda longa acima saiu numa
> **única release v1.2.11**, com uma entrada de changelog por diploma. Não abrir
> uma versão por diploma: acumular as entradas do lote sob a mesma `version` e só
> subir `package.json` uma vez, ao fechar a sessão.

> **Sistema financeiro (7.492/86):** triado e completo (arts. 2º–23 presentes).
> Sem reforma penal desde 2023. A única mudança recente (Lei 14.478/2022, ativos
> virtuais) só equiparou provedores de cripto a instituição financeira no art. 1º,
> §único — expande o sujeito, não cria tipo. Nada a fazer; sem release.

## O que FALTA (retomar aqui)

**Cauda longa de diplomas ainda não triados** (por lei-reforma ou por diploma),
na ordem de prioridade (mais consultados/prováveis primeiro):
CPM (DL 1.001/69, 352 tipos — militar, raramente alterado, pode ser sessão
própria), e ~40 diplomas pequenos/antigos (baixa probabilidade de alteração recente).

> **Achado da sessão (importante):** vários erros que NÃO eram defasagem, e sim
> registros errados desde a origem, só apareceram ao casar artigo a artigo contra
> o compilado — Henry Borel art. 26 (crime/pena/tipo trocados), Maria da Penha
> art. 24-A (pena antiga + aumento inexistente por "arma de fogo"), CDC art. 73
> (1-5 anos em vez de 1-6 meses) e falências arts. 171/173/177 (crime e/ou pena
> trocados). Reforça o método: conferir CADA rótulo contra o texto, não confiar no
> registro nem presumir que só as leis novas trazem defeito.

Sugestão de ordem: os mais consultados e mais prováveis de reforma recente
primeiro; deixar o CPM e os diplomas antigos de 1–2 tipos por último.

## Onde estão as coisas

- Fonte do catálogo: `data/crimes.json` (derivado em `static/data/crimes.json`).
- Modificadores de dosimetria: `data/modificadores.json`.
- Cada mudança vira uma entrada em `src/data/changelog/entries/<ano>/<id>.ts`
  (ver `src/data/changelog/create-changelog-entry.md`).
- Verificação: `python scripts/transform_data.py --estrito --max-contradicoes=0`,
  `python scripts/validar_modificadores.py`, `npm run typecheck`,
  `npm run verificar`, `npm run build`.
- Versionamento: correção de dado → patch (`1.2.Z`), fechado um lote por vez.
