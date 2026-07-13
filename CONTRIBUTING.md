# Como contribuir — SISPENAS

## Visão geral

- **Fonte canônica do catálogo:** `data/crimes.json` (uma entrada por tipo penal).
- **Catálogo consumido pelo site:** `static/data/crimes.json` — **gerado** por
  `scripts/transform_data.py`. Não edite à mão; ele é regenerado a cada mudança da fonte.
- **Campos derivados** (`pena_privativa`, `tem_multa`, `multa_regime`,
  `infracao_menor_potencial`, `pena_min_meses`, `pena_max_meses`, rótulos de exibição)
  são produzidos pelo transformador a partir de `data/crimes.json`.

## Como o catálogo é atualizado

1. **Carga inicial (uma vez):** o catálogo é montado a partir de uma **planilha**. Uma
   **IA lê a planilha, faz o parser e escreve `data/crimes.json`** no schema abaixo.
2. **Manutenção contínua (depois disso):** as atualizações vêm de **duas** origens, não
   de digitação manual de tipos:
   - **Scraper do DOU** (ver roadmap): captura alterações legislativas e propõe o diff.
   - **IA entregando as informações a adicionar/alterar**, já no schema.
3. **Ajustes finos por humanos:** humanos fazem, no máximo, **pequenas correções a termo**
   (typo, reclassificação pontual), nunca adições manuais em escala.

> Em resumo: **planilha+IA (carga inicial) → depois scraper do DOU ou IA (manutenção)**.
> Humanos entram só para correções finas.

## Passos de uma atualização (PR)

1. Edite **apenas** `data/crimes.json` (a fonte) — direto na interface do GitHub ou local.
2. Regenere o derivado (duas opções):
   - **Automático (GitHub):** ao abrir/pushar a mudança em `data/crimes.json` na branch
     `main`, o workflow `Regenerar dados derivados` roda o transformador e **commita**
     `static/data/crimes.json` de volta. Não precisa rodar Python localmente.
   - **Local:** `python3 scripts/transform_data.py` e commit do `static/data/crimes.json`.
3. Abra um Pull Request. O CI valida `typecheck` e `build`.

### Correções finas (multa e afins)

Ajustes que a heurística não acerta devem ir em `CORRECOES`, dentro de
`scripts/transform_data.py` (chaveado por `id`), e **não** no JSON gerado.
Exemplo presente: Art. 227 do CP (a multa só incide na hipótese do §3º).

## Schema de `data/crimes.json`

| campo | tipo | observação |
|-------|------|------------|
| `id` | inteiro único | — |
| `lei` | texto | diploma (ex.: "CP", "Lei 11.343/06") |
| `artigo` | texto | ex.: "Art. 155, caput" |
| `crime` | texto | nome do tipo |
| `pena_min` | inteiro | **em meses** (compat.; a unidade real é derivada de `obs`) |
| `pena_max` | inteiro | **em meses** (compat.; a unidade real é derivada de `obs`) |
| `tipo_pena` | texto | Reclusão / Detenção / Prisão simples / Multa / — |
| `acao` | texto | ação penal |
| `hediondo` | Sim / Não / — | |
| `elemento` | texto | Doloso / Culposo / ... |
| `tentativa` | Sim / Não / — | |
| `violencia` | Sim / Não / — | |
| `grave_ameaca` | Sim / Não / — | |
| `obs` | texto | descrição / notas. **A faixa de pena é lida daqui** (ex.: "15 dias a 6 meses", "1-5 anos") |

### Unidades de pena (dias / meses / anos)

O transformador extrai a faixa de pena do texto de `obs` e converte tudo para uma
unidade canônica em **meses** (`pena_min_meses`/`pena_max_meses`, contando o mês como
30 dias — Art. 11 do CP), preservando a unidade natural para exibição
(`pena_min_rotulo`/`pena_max_rotulo`/`pena_faixa_rotulo`). Assim "15 dias a 6 meses"
aparece corretamente e é calculado sem inverter mínimo/máximo.

> Regra de consistência: `pena_min_meses <= pena_max_meses`. Se a faixa não puder ser lida
> de `obs`, o transformador cai para `pena_min`/`pena_max` (em meses) como fallback.

## Desenvolvimento

```bash
npm install
npm run start       # dev server
npm run typecheck
npm run build
python3 scripts/transform_data.py   # regenera static/data/crimes.json
```
