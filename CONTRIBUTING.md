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
3. Abra um Pull Request. O CI valida, nesta ordem:
   - `transform_data.py --estrito` — convenções C1, C2, C3 e o teto de contradições (C4);
   - se o derivado commitado corresponde à fonte;
   - `npm run typecheck`;
   - `npm run verificar` — invariantes do motor de benefícios e casos-âncora de direito
     penal contra o catálogo real;
   - `npm run build`.

### Correções finas (multa e afins)

Ajustes que a heurística não acerta devem ir em `CORRECOES`, dentro de
`scripts/transform_data.py` (chaveado por `id`), e **não** no JSON gerado.
Exemplo presente: Art. 227 do CP (a multa só incide na hipótese do §3º).

## Convenções do catálogo

**Estas regras valem para qualquer origem de atualização — IA, scraper do DOU ou
correção humana.** Várias são impostas por `scripts/transform_data.py`, que **falha o
build** quando violadas; as demais dependem de disciplina de quem escreve.

### C1. O catálogo contém APENAS tipos penais ⛔ imposta

Um registro = um tipo penal. **Não** entram no catálogo:

- notas de referência ("a LGPD não tipifica crimes específicos");
- agravantes e atenuantes (art. 61 a 66, CP);
- causas de aumento e diminuição (art. 141, CP; art. 258, CP);
- excludentes de ilicitude (art. 128, I e II, CP);
- causas de extinção da punibilidade em si (art. 121, §5º — o perdão judicial é
  atributo do tipo, campo `perdao_judicial_previsto`, não um tipo);
- regras de ação penal (art. 171, §5º, CP — isso é o campo `acao`).

21 registros assim foram removidos na v1.1.0: com pena zero, satisfaziam qualquer teto e
eram contados como "cabíveis" em transação penal, ANPP e sursis, inflando as estatísticas.

> Causas de aumento/diminuição voltarão como **entidade própria** na dosimetria por fases
> (roadmap, v3.0.0) — não como tipos penais.

### C2. Todo tipo declara uma sanção ⛔ imposta

Pena privativa em `pena_min`/`pena_max`, **ou** `sancoes_nao_privativas` quando o tipo não
comina prisão. Hoje o único caso é o art. 28 da Lei 11.343/06 (porte para consumo):

```json
"sancoes_nao_privativas": [
  {"inciso": "I", "sancao": "Advertência sobre os efeitos das drogas"},
  {"inciso": "II", "sancao": "Prestação de serviços à comunidade"},
  {"inciso": "III", "sancao": "Medida educativa de comparecimento a programa ou curso educativo"}
]
```

Sem um nem outro, o build falha — é sinal de que o registro não é tipo penal (C1) ou de
que falta dado.

### C3. `id` é append-only ⛔ imposta

O `id` é a **URL pública** de cada tipo (`/pesquisa/tipos?tipo=N`) e o site está publicado.

- Id novo = `max(id) + 1`. Nunca no meio, nunca renumerando.
- Id removido vira **buraco permanente**; jamais é reatribuído a outro dispositivo — um
  link antigo passaria a apontar para o crime errado, falha silenciosa.
- Os ids de 1 a 1061 já foram usados; 21 deles estão vagos e assim permanecem.

### C4. Um registro por dispositivo

A chave é `lei + artigo`. Repetir o mesmo dispositivo cria uma **duplicata**; se as cópias
divergirem em pena ou hediondez, cria uma **contradição** — o catálogo passa a afirmar
duas penas para o mesmo artigo.

Há **42 contradições** herdadas. A CI roda `--max-contradicoes=42`: o número pode cair,
nunca subir. Ao resolver uma, baixe o limite no `.github/workflows/ci.yml`.

Para distinguir incisos do mesmo parágrafo, use o inciso no `artigo`
(`Art. 121, §2º, I`), nunca dois registros com `Art. 121, §2º`.

### C5. O nome do tipo é dado, não rótulo

`crime` alimenta derivação automática. Em especial, **`resultado_morte` é derivado do
nome** (art. 112, VI e VIII, LEP → frações de 50% e 70%).

- Diga no nome quando o tipo for qualificado pela morte: *"Lesão corporal seguida de
  morte"*, *"Latrocínio"*, *"Extorsão com resultado morte"*.
- **Não** confie no `obs` para isso: ele descreve os demais parágrafos do artigo ("se
  resulta morte, triplica"), e por isso é ignorado nessa derivação — do contrário, o art.
  135 (omissão de socorro) seria marcado indevidamente.

### C6. `hediondo` inclui os equiparados

Tráfico, tortura e terrorismo entram como `hediondo: "Sim"` — é o que aciona as vedações
do art. 5º, XLIII, da CF (graça, indulto, anistia). Exceções consolidadas ficam como
`"Não"`: tráfico privilegiado (art. 33, §4º — STF, HC 118.533) e associação para o
tráfico (art. 35).

### C7. A faixa de pena vem do `obs`

Escreva a faixa em `obs` na unidade natural ("15 dias a 6 meses", "1-5 anos"); o
transformador converte para meses e preserva o rótulo. `pena_min`/`pena_max` (em meses)
são o fallback. Regra: `pena_min_meses <= pena_max_meses`.

**Tipo sem pena mínima.** Nem todo tipo comina os dois extremos. Vários só têm teto —
"detenção **até** 3 meses" (art. 32 da LCP; arts. 289, 290, 300, 301 e 309 do Código
Eleitoral). Nesses casos `pena_min` é `0` e o rótulo sai como "até 3 meses". **Zero na
mínima não é "sem pena"**: o tipo é punível, apenas não tem piso cominado — e, por isso,
os benefícios que dependem da pena mínima (ANPP, suspensão condicional do processo)
são-lhe os mais favoráveis possíveis. Não preencha a mínima com um chute.

Não confunda com o **tipo sem pena privativa** (C2), que não tem prisão alguma.

### C8. Perdão judicial é lista curada, não inferência

Não existe perdão judicial genérico e ele não se estende por analogia (art. 107, IX, CP).
Um tipo novo que o admita exige entrada em `PERDAO_JUDICIAL`, no
`scripts/transform_data.py`, **com revisão humana** — nenhuma automação deve inferi-lo do
elemento culposo.

---

## Schema de `data/crimes.json`

| campo | tipo | observação |
|-------|------|------------|
| `id` | inteiro único | append-only; é a URL pública (C3) |
| `lei` | texto | diploma (ex.: "CP", "Lei 11.343/06") |
| `artigo` | texto | ex.: "Art. 155, caput"; com inciso quando houver (C4) |
| `crime` | texto | nome do tipo — **alimenta `resultado_morte`** (C5) |
| `pena_min` | inteiro | **em meses** (compat.; a unidade real é derivada de `obs`) |
| `pena_max` | inteiro | **em meses** (compat.; a unidade real é derivada de `obs`) |
| `sancoes_nao_privativas` | lista | só quando não há pena privativa (C2) |
| `tipo_pena` | texto | Reclusão / Detenção / Prisão simples / Multa / — |
| `acao` | texto | ação penal |
| `hediondo` | Sim / Não / — | inclui equiparados (C6) |
| `elemento` | texto | Doloso / Culposo / Preterdoloso |
| `tentativa` | Sim / Não / — | pressuposto do art. 15 do CP |
| `violencia` | Sim / Não / — | |
| `grave_ameaca` | Sim / Não / — | |
| `obs` | texto | descrição / notas. **A faixa de pena é lida daqui** (ex.: "15 dias a 6 meses", "1-5 anos") |

Campos derivados (não escreva à mão): `pena_privativa`, `tem_multa`, `multa_regime`,
`pena_*_meses`, `pena_*_rotulo`, `pena_faixa_rotulo`, `infracao_menor_potencial`,
`tem_pena_privativa`, `resultado_morte`, `perdao_judicial_previsto`, `chave_dispositivo`,
`duplicata*`. Ver [Catálogo de tipos penais](docs/catalogo-tipos-penais.md).

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
npm run verificar   # motor de benefícios × catálogo real
npm run build
python3 scripts/transform_data.py   # regenera static/data/crimes.json + qualidade.json
python3 scripts/transform_data.py --estrito --max-contradicoes=42   # como na CI
```
