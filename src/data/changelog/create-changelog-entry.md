# Como criar uma entrada do changelog

As Notas de atualizações (`/release-notes`) são um **feed de mudanças**: cada
alteração é uma entrada própria. Não há lista central — **adicionar uma nota é
criar um arquivo**. O feed no site e o corpo da Release no GitHub leem os mesmos
arquivos.

## Regras (valem também para uma IA gerar o arquivo)

1. **Um arquivo por mudança.** Local:
   `src/data/changelog/entries/<ano>/<id>.ts`, onde
   `<id> = AAAA-MM-DD-<slug>` (ex.: `2026-07-22-dosimetria-tres-fases-art-68`).
   O `<slug>` é curto, em minúsculas, sem acentos, palavras separadas por hífen.
   O nome do arquivo (sem `.ts`) **é** o `id`.

2. **O arquivo faz `export default` de um objeto `ChangelogEntry`** (contrato em
   `../../types.ts`). Modelo:

   ```ts
   import type {ChangelogEntry} from '../../types';

   const entrada: ChangelogEntry = {
     id: '2026-07-22-dosimetria-tres-fases-art-68',
     date: '2026-07-22',
     title: 'Dosimetria pelas três fases do art. 68',
     summary: 'Um parágrafo que resume a mudança para quem só lê o resumo.',
     body: [
       'Primeiro parágrafo de detalhe, texto puro.',
       'Segundo parágrafo. Cada string é um parágrafo, renderizado as-is.',
     ],
     tipo: 'novidade',
     areas: ['Dosimetria'],
     version: 'v1.2.0',
     links: [
       {label: 'Ver onde a mudança aparece', href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=1'},
     ],
   };

   export default entrada;
   ```

3. **`body` é TEXTO PURO** — sem markdown, sem backticks, sem listas, sem tabelas.
   Um item do array = um parágrafo. Se precisar enumerar, escreva em prosa.

4. **`tipo`** (a natureza da mudança, um só):
   - `novidade` — funcionalidade nova (fecha uma versão `1.Y.0`);
   - `melhoria` — aprimoramento que não muda dado do catálogo;
   - `correcao` — correção de dado ou de norma (`1.1.Z`);
   - `estrutural` — quebra de contrato dos dados abertos ou das URLs (`X.0.0`).

5. **`areas`** (uma ou mais): `Tipos penais`, `Benefícios`, `Dosimetria`,
   `Acervo histórico`, `Interface`, `Documentação`. Grafia exata, com acento.
   Use `Documentação` para mudanças nas páginas de Documentação, no Roadmap e na
   página inicial; `Interface` para a ferramenta de busca em si.

6. **`version`** é a versão que a mudança fecha (ex.: `v1.2.1`). Opcional só para
   algo fora de uma release.

7. **`links`** (opcional): o local exato onde a mudança aparece. É o que abre na
   seção de detalhes. Prefira URLs absolutas do site publicado.

## O que NÃO fazer

- Não editar uma lista central (não existe).
- Não reaproveitar um `id`/arquivo: `id` compõe a âncora e deve ser único.
- Não pôr markdown em `summary` nem em `body`.

## Como é consumido

- **Frontend**: `src/data/changelog/index.ts` agrega tudo por `require.context` e
  ordena por data (mais recentes primeiro).
- **CI / Release**: `scripts/montar-nota-release.mjs vX.Y.Z` concatena as entradas
  daquela versão para formar o corpo da Release no GitHub.
- **Paridade**: `scripts/gerar-changelog-json.mjs` emite `static/data/changelog.json`
  (o mesmo array), para que um backend futuro produza exatamente o mesmo formato.
