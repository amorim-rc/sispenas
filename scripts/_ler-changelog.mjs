// Lê todas as entradas de src/data/changelog/entries/**/*.ts e devolve o array
// ordenado (mais recentes primeiro). Sem dependências: usa só builtins do Node e
// o import nativo de TypeScript (Node >= 22.6 com type stripping; 24 por padrão).
//
// É o mesmo conjunto que o frontend agrega por require.context — os dois caminhos
// produzem o mesmo array de ChangelogEntry.

import {readdirSync} from 'node:fs';
import {join, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = join(AQUI, '..', 'src', 'data', 'changelog', 'entries');

function percorrer(dir) {
  const achados = [];
  for (const item of readdirSync(dir, {withFileTypes: true})) {
    const caminho = join(dir, item.name);
    if (item.isDirectory()) achados.push(...percorrer(caminho));
    else if (item.name.endsWith('.ts')) achados.push(caminho);
  }
  return achados;
}

export async function lerEntradas() {
  const arquivos = percorrer(RAIZ);
  const entradas = [];
  for (const arquivo of arquivos) {
    const mod = await import(pathToFileURL(arquivo).href);
    entradas.push(mod.default);
  }
  entradas.sort((a, b) =>
    a.date !== b.date ? (a.date < b.date ? 1 : -1) : a.id < b.id ? 1 : -1,
  );
  return entradas;
}
